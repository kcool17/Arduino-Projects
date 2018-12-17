#!/usr/bin/env python
import discord
from discord.ext import commands

import pickle
import os
import asyncio
import itertools
import math
import sys
import traceback
import time
import random
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from server import DEVS


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': False,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.length = data.get('duration')
        self.uploader = data.get('uploader')
        self.release_date = data.get('upload_date')
        self.thumbnail = data.get('thumbnail')
        
        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()
        data = None
        x = 0
        while data == None and x<5:
            x+=1
            to_run = partial(ytdl.extract_info, url=search, download=download)
            data = await loop.run_in_executor(None, to_run)
            search = search + " "
        
        if data == None:
            await ctx.send("There was an error finding your song. Please try a different keyword.")
            
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send('```ini\n[Added {title} to the Queue.]\n```'.format(title = data["title"]))

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title'], 'duration': data['duration']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'oldSource', 'loop', 'skipLoop', 'skipVote', 'loopVote', 'searchArr', 'didSkip', 'loopQueue', 'jumpTo', 'jumpLoop', 'currentURL')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = []
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None
        
        self.oldSource = None
        self.loop = False
        self.skipLoop = False
        self.skipVote = []
        self.loopVote = []
        self.searchArr =[]
        self.didSkip = False
        
        self.loopQueue = False
        self.jumpTo = 0
        self.jumpLoop = False
        
        self.currentURL = ""

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()
            
            for thing in self.queue:
                if thing == None:
                    print("Hey, you wanted to see this error. Well, a None just appeared in a queue. Hopefully it's fixed!")
                    self.queue.remove(thing)
            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    if self.queue == []:
                        source = None
                    elif self.loop == False or self.skipLoop == True or self.jumpLoop == True:
                        source = self.queue.pop(0)
                        self.skipLoop = False
                        self.didSkip = True
                        if self.loopQueue == True:
                            self.queue.append(self.oldSource)
                            if self.jumpLoop == True:
                                self.queue.append(source)
                                for x in range(0, self.jumpTo - 1):
                                    source = self.queue.pop(0)
                                    if not self.jumpTo - 2  == x:
                                        self.queue.append(source)
                                    x+=1
                                self.jumpLoop = False
                            
                        elif self.jumpLoop == True:
                            for x in range(0, self.jumpTo - 1):
                                source = self.queue.pop(0)
                                x+=1
                            self.jumpLoop = False
                            
                    else:
                        source = self.oldSource
                        
            except asyncio.TimeoutError:
                return self.destroy(self._guild)
            
            if source != None:
                self.oldSource = source
            
            
            
            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    if source != None:
                        await self._channel.send('There was an error processing your song.\n'
                                                 '```css\n[{e}]\n```'.format(e=e))
                    else:
                        await self.bot.get_channel(511655906854043725).send('There was an error processing your song.\n'
                                                                            '```css\n[{e}]\n```'.format(e=e))
                    continue

            
            source.volume = self.volume

            
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            
            if not self.loop or self.didSkip:
                self.didSkip = False
                releaseDate = source.release_date
                m, s = divmod(source.length, 60)
                h, m = divmod(m, 60)
                prettyLength = "%d:%02d:%02d" % (h, m, s)
                try:
                    tempVar = self.queue[0] == None
                except:
                    tempVar = False
                if self.queue!=[] and not tempVar:
                    upNext = self.queue[0]["title"]
                else:
                    upNext = "Nothing"
                
                npEmbed = discord.Embed(title="**Now Playing**", description="[" + source.title+"]("+source.web_url+")", color=0x0000ff)
                npEmbed.set_thumbnail(url=source.thumbnail)
                npEmbed.set_footer(text="Requested By: " + source.requester.display_name + " (" + str(source.requester) + ")")
                npEmbed.add_field(name="**Length:** " + prettyLength, value= "Up Next: " + upNext, inline=False)
                npEmbed.add_field(name="By: " + source.uploader, value= "Uploaded: " + releaseDate[4:6] + "/" + releaseDate[6:] + "/" + releaseDate[:4], inline=False)
                self.np = await self._channel.send(embed=npEmbed)
                
            pickle.dump(time.time(), open('servers' + os.sep + str(self._guild.id) + os.sep + "vidStart.p", "wb"))
            if self.queue!=[]:
                newQueue = []
                for item in self.queue:
                    newQueue.append(item['webpage_url'])
                self.currentURL = source.web_url
                newQueue.append(self.currentURL)
                pickle.dump(newQueue, open('servers' + os.sep + str(self._guild.id) + os.sep + "queueBackup.p", "wb"))
            await self.next.wait()
            
            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None
            self.skipVote = []
            self.loopVote = []


    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music:
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
    
    def getUsers(self, ctx, arg='noArg'):
        userList = []
        userIDList = []
        userNickList = []
        for person in ctx.guild.members:  #Creates lists
            userList.append(person)
            userIDList.append(person.id)
            try:
                if len(person.display_name) > 0:
                    userNickList.append(person.display_name)
                else:
                    userNickList.append(person)
            except:
                userNickList.append(person)
        findList = []
        findIDList = []
        pos = 0
        #Finds user
        for thing in userList:
            if str(thing).lower().startswith(arg.lower()):
                findList.append(str(thing))
                findIDList.append(userIDList[pos])  
            pos += 1
        pos = 0
        for thing in userNickList:
            if str(thing).lower().startswith(arg.lower()) and (str(userList[pos]) not in findList):
                findList.append(str(userList[pos]))
                findIDList.append(userIDList[pos])
            pos += 1
        return (findList, findIDList)
    
    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', aliases=['join'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice. DJ-Only, if already connected. 
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client
        guild = ctx.guild.id
        member = ctx.author.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        
        if vc:
            if ctx.author.guild_permissions.manage_channels or member in ADMINS:
                if vc.channel.id == channel.id:
                    return
                try:
                    await vc.move_to(channel)
                except asyncio.TimeoutError:
                    raise VoiceConnectionError('Moving to channel: <{channel}> timed out.'.format(channel=channel))
            else:
                await ctx.send("Bot already connected to channel! Just join that one.")
                return
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError('Connecting to channel: <{channel}> timed out.'.format(channel=channel))

        await ctx.send('Connected to: **{channel}**'.format(channel=channel))
    
    @commands.command(aliases=['restart', 'fixq'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def replay(self, ctx):
        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            try:
                searchlist = pickle.load(open('servers' + os.sep + str(ctx.guild.id) + os.sep + "queueBackup.p", "rb"))
                player = self.get_player(ctx)
            
                # If download is False, source will be a dict which will be used later to regather the stream.
                # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
                for search in searchlist:
                    if search != None and search != "":
                        try:
                            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
                            player.queue.append(source)
                            if player.queue!=[]:
                                newQueue = []
                                for item in player.queue:
                                    newQueue.append(item["webpage_url"])
                                newQueue.append(player.currentURL)
                                pickle.dump(newQueue, open('servers' + os.sep + str(ctx.guild.id) + os.sep + "queueBackup.p", "wb"))
                        except:
                            pass
                player.loopQueue = True
                await ctx.send("Old Queue added to new one!")
            except Exception as e:
                print('```css\n[{e}]\n```'.format(e=e))
                await ctx.send("Sorry, there was no previous queue saved!")
                
    
    
    @commands.command(name='play', aliases=['p'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)

            # If download is False, source will be a dict which will be used later to regather the stream.
            # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
            try:
                newSearch = int(search) - 1
                newSearch = player.searchArr[newSearch]
                newSearch = newSearch["webpage_url"]
                source = await YTDLSource.create_source(ctx, newSearch, loop=self.bot.loop, download=False)
            except:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

            player.queue.append(source)
            if player.queue!=[]:
                newQueue = []
                for item in player.queue:
                    newQueue.append(item["webpage_url"])
                newQueue.append(player.currentURL)
                pickle.dump(newQueue, open('servers' + os.sep + str(ctx.guild.id) + os.sep + "queueBackup.p", "wb"))
        else:
            await ctx.send("Join the voice channel!")
    
    @commands.command(aliases=['playm', 'playmult', 'playmultiple', 'pmult'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def play_multiple(self, ctx, *searchlist : str):
        """Play a list of songs. make sure to quote each search term, as it'll go through your quoted list and play each one. Max of 10 at a time.
        Note: Incompatible with the Search feature.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            
            if len(searchlist) > 10:
                await ctx.send("Too many songs! Please only do 10 at a time.")
                return
            # If download is False, source will be a dict which will be used later to regather the stream.
            # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
            for search in searchlist:
                try:
                    source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
                    player.queue.append(source)
                    if player.queue!=[]:
                        newQueue = []
                        for item in player.queue:
                            newQueue.append(item["webpage_url"])
                        newQueue.append(player.currentURL)
                        pickle.dump(newQueue, open('servers' + os.sep + str(ctx.guild.id) + os.sep + "queueBackup.p", "wb"))
                except:
                    await ctx.send("An error occurred with your search \"" + search + "\"! Please try again!")
        else:
            await ctx.send("Join the voice channel!")
    
    
    @commands.command(aliases=['s'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def search(self, ctx, *, search : str):
        """Searches for the top 10 Youtube results for the search, and these songs can then be played."""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            await ctx.send("Searching for \"" + search + "\"...")
            await ctx.trigger_typing()
            loop = asyncio.get_event_loop()
            to_run = partial(ytdl.extract_info, url="ytsearch10:" + search, download=False)
            data = await loop.run_in_executor(None, to_run)
                
            searchList = []
            for thing in data['entries']:
                myDict = {"webpage_url" : thing["webpage_url"],
                          "title" : thing["title"],
                          "duration" : thing["duration"],
                          "author" : thing["uploader"],
                          }
                searchList.append(myDict)
            
            player = self.get_player(ctx)
            player.searchArr = searchList
            z=1
            fmt = ""
            for x in searchList:
                m, s = divmod(x['duration'], 60)
                h, m = divmod(m, 60)
                prettyLength = "%d:%02d:%02d" % (h, m, s)
                fmt = fmt + '\n' + '**' + str(z) + ". [" + x['title'] + '](' + x['webpage_url'] + ')** | By: ' + x['author'] + ' | Length: ' + prettyLength
                z += 1
        
            embed = discord.Embed(title='Search Results for "' + search + '"', description=fmt, color=0x0000FF)
            embed.add_field(name="\U0000200B", value="Use `?play x`, with `x` being from 1-10, to play one of these results.", inline=False)
            embed.set_footer(text="Searched By: " + ctx.author.display_name + "(" + str(ctx.author) + ")")
            await ctx.send(embed=embed)
        
        
        
    @commands.command(name='pause', aliases=["stop"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def pause_(self, ctx):
        """DJ-Only. Pause the currently playing song. """
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            if member in DJS:
                if not vc or not vc.is_playing():
                    return await ctx.send('I am not currently playing anything!')
                elif vc.is_paused():
                    return

                vc.pause()
                pickle.dump(time.time(), open('servers' + os.sep + str(ctx.guild.id) + os.sep + "pauseStart.p", "wb"))
                await ctx.send('**`{author}`**: Paused the song!'.format(author=ctx.author))
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")

    @commands.command(name='resume')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def resume_(self, ctx):
        """DJ-Only. Resume the currently paused song. """
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            if member in DJS:
                if not vc or not vc.is_connected():
                    return await ctx.send('I am not currently playing anything!')
                elif not vc.is_paused():
                    return

                vc.resume()
                try:
                    vidStart = pickle.load(open('servers' + os.sep + str(ctx.guild.id) + os.sep + "vidStart.p", "rb"))
                except:
                    vidStart = time.time()
                try:
                    pauseStart = pickle.load(open('servers' + os.sep + str(ctx.guild.id) + os.sep + "pauseStart.p", "rb"))
                except:
                    pauseStart = time.time()
                vidStart = vidStart + (time.time() - pauseStart)
                pickle.dump(vidStart, open('servers' + os.sep + str(ctx.guild.id) + os.sep + "vidStart.p", "wb"))
                await ctx.send('**`{author}`**: Resumed the song!'.format(author=ctx.author))
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")

    @commands.command(name='skip')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            guild = ctx.guild.id
            member = ctx.author.id
            if not vc or not vc.is_connected():
                return await ctx.send('I am not currently playing anything!')
            vcMembers = vc.channel.members
            if vc.is_paused():
                pass
            elif not vc.is_playing():
                return
            for person in player.skipVote:
                if person not in vcMembers:
                    player.skipVote.remove(person)
            if member in DJS:
                vc.stop()
                player = self.get_player(ctx)
                player.skipLoop = True
                await ctx.send('**`{author}`**: Skipped the song!'.format(author=ctx.author))
            else:
                player.skipVote.append(member)
                await ctx.send(str(len(player.skipVote)) + "/" + str(int((len(vcMembers)/2))) + " people needed to skip!")
            if len(player.skipVote) >= int((len(vcMembers)/2)):
                vc.stop()
                player = self.get_player(ctx)
                player.skipLoop = True
                await ctx.send('Skipping the song!')
        else:
            await ctx.send("Join the voice channel!")

            
    @commands.command(name='queue', aliases=['q'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def queue_info(self, ctx, pageNum = "1"):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        player = self.get_player(ctx)
        if player.queue == []:
            await ctx.send('Queue is empty.')
            await ctx.invoke(self.now_playing_)
            return
        
        for thing in player.queue:
            if thing == None:
                print("Hey, you wanted to see this error. Well, a None just appeared in a queue. Hopefully it's fixed! #2, of course.")
                player.queue.remove(thing)
        
        try:
            pageNum = int(pageNum) - 1
        except:
            pageNum = 0
                   
        if len(player.queue)<= (pageNum)*10 or pageNum < 1:
            pageNum = 0
            
        upcoming = player.queue[(pageNum*10)+1:((pageNum+1)*10)+1]
        x = vc.source
        totalLength = 0
        fmt = "**NOW PLAYING: "
        totalLength = totalLength + x.length
        m, s = divmod(x.length, 60)
        h, m = divmod(m, 60)
        prettyLength = "%d:%02d:%02d" % (h, m, s)
        fmt = fmt + "[" + x.title + '](' + x.web_url + ')** | Length: ' + prettyLength
        z = 1 + (pageNum*10)
        totalLength = 0
        for x in upcoming:
            totalLength = totalLength + x['duration']
            m, s = divmod(x['duration'], 60)
            h, m = divmod(m, 60)
            prettyLength = "%d:%02d:%02d" % (h, m, s)
            fmt = fmt + '\n' + '**' + str(z) + ". [" + x['title'] + '](' + x['webpage_url'] + ')** | Length: ' + prettyLength
            z += 1
        m, s = divmod(totalLength, 60)
        h, m = divmod(m, 60)
        prettyTotalLength = "%d:%02d:%02d" % (h, m, s)
        embed = discord.Embed(title='Upcoming - {upcoming_len} Songs | Total Length: '.format(upcoming_len=len(player.queue) - 1) + prettyTotalLength, description=fmt, color=0x0000FF)
        toFoot = ""
        if player.loop:
            toFoot = toFoot + "Looping Current Song"
        elif player.loopQueue:
            toFoot = toFoot + "Looping Queue"
        else:
            toFoot = toFoot + "Looping Disabled"
        toFoot = toFoot + " | "
        if vc.is_paused():
            toFoot = toFoot + "Paused"
        else:
            toFoot = toFoot + "Playing"
        toFoot = toFoot + " | "
        toFoot = toFoot + "Skip Votes: " + str(len(player.skipVote)) + "/" + str(int((len(vc.channel.members)/2)))
        toFoot = toFoot + " | Page " + str(pageNum + 1) + "/" + str(math.ceil(len(player.queue)/10))
        
        embed.set_footer(text= toFoot)
        await ctx.send(embed=embed)

    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        guild = ctx.guild
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        try:
            vidStart = pickle.load(open('servers' + os.sep + str(guild.id) + os.sep + "vidStart.p", "rb"))
        except:
            vidStart = time.time()
        try:
            pauseStart = pickle.load(open('servers' + os.sep + str(ctx.guild.id) + os.sep + "pauseStart.p", "rb"))
        except:
            pauseStart = time.time()
            
        if not vc.is_paused():
            currentTime = time.time() - vidStart
        else:
            currentTime = pauseStart - vidStart
        m, s = divmod(currentTime, 60)
        h, m = divmod(m, 60)
        prettyTime = "%d:%02d:%02d" % (h, m, s)
        m, s = divmod(vc.source.length, 60)
        h, m = divmod(m, 60)
        prettyLength = "%d:%02d:%02d" % (h, m, s)
        lengthBar = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        lengthLoc = int((currentTime / vc.source.length) * 20)
        releaseDate = vc.source.release_date
        
        npEmbed = discord.Embed(title="**Now Playing**", description="[" + vc.source.title+"]("+vc.source.web_url+")", color=0x0000ff)
        npEmbed.set_thumbnail(url=vc.source.thumbnail)
        npEmbed.set_footer(text="Requested By: " + vc.source.requester.display_name + " (" + str(vc.source.requester) + ")")
        npEmbed.add_field(name='%s%s%s'%(lengthBar[:lengthLoc],"\U0001F518",lengthBar[lengthLoc+1:]), value=prettyTime + " / " + prettyLength, inline=False)
        npEmbed.add_field(name="By: " + vc.source.uploader, value= "Uploaded: " + releaseDate[4:6] + "/" + releaseDate[6:] + "/" + releaseDate[:4], inline=False)
        
        
        player.np = await ctx.send(embed=npEmbed)

    @commands.command(name='volume', aliases=['vol'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def change_volume(self, ctx, *, vol: float):
        """DJ-only. Change the player volume. 
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            if member in DJS:
                if not vc or not vc.is_connected():
                    return await ctx.send('I am not currently connected to voice!')

                if not 0 < vol < 101:
                    return await ctx.send('Please enter a value between 1 and 100.')

                player = self.get_player(ctx)

                if vc.source:
                    vc.source.volume = vol / 100

                player.volume = vol / 100
                await ctx.send('**`{author}`**: Set the volume to **{vol}%**'.format(author=ctx.author, vol=vol))
            else:
                await ctx.send("You're not a DJ! This isn't for you.")
        else:
            await ctx.send("Join the voice channel!")

    @commands.command(name='leave', aliases=["disconnect"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def stop_(self, ctx):
        """DJ-Only. Stop the currently playing song and destroy the player. 
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            if member in DJS:
                if not vc or not vc.is_connected():
                    return await ctx.send('I am not currently playing anything!')

                await self.cleanup(ctx.guild)
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")


    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def loop(self, ctx):
        """Loops the currently playing song"""
        player = self.get_player(ctx)
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            if player.loop:
                await ctx.send("Loop Disabled!")
                player.loop = False
            else:
                await ctx.send("Loop Enabled! (And loop queue disabled!)")
                player.loop = True
                player.loopQueue = False
        else:
            await ctx.send("Join the voice channel!")
            
    @commands.command(aliases=["loopq", "qloop"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def loopqueue(self, ctx):
        """Loops the current Queue"""
        player = self.get_player(ctx)
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            if player.loopQueue:
                await ctx.send("Loop Queue Disabled!")
                player.loopQueue = False
            else:
                await ctx.send("Loop Queue Enabled! (And regular loop disabled!)")
                player.loopQueue = True
                player.loop = False
        else:
            await ctx.send("Join the voice channel!")
        
        
        
        
        
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def clear(self, ctx):
        """DJ-Only. Clears the Queue. """
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            if member in DJS:
                player = self.get_player(ctx)
                player.queue = []
                await ctx.send("Queue cleared!")
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")
    
    @commands.command(aliases = ["j"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def jump(self, ctx, toJump = ""):
        """If queue is currently looped, it jumps to the song # you input. If it's not, only DJs (those with Manage Channels permissions) can jump immediately."""
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            guild = ctx.guild.id
            member = ctx.author.id
            if not vc or not vc.is_connected():
                return await ctx.send('I am not currently playing anything!')
            if vc.is_paused():
                pass
            elif not vc.is_playing():
                return
            
            try:
                toJump = int(toJump)
            except:
                await ctx.send("Error! Make sure you pick a number to jump to!")
                return
            if toJump < 1 or toJump > len(player.queue):
                await ctx.send("Error! Please pick a valid song to jump to!")
                return
            
            if member in DJS:
                vc.stop()
                player.jumpLoop = True
                player.jumpTo = toJump
                await ctx.send('**`{author}`**: is jumping to song #{num}!!'.format(author=ctx.author, num=toJump))
            else:
                if player.loopQueue == True:
                    vc.stop()
                    player.jumpLoop = True
                    player.jumpTo = toJump
                    await ctx.send('**`{author}`**: is jumping to song #{num}!!'.format(author=ctx.author, num=toJump))
                else:
                    await ctx.send("Sorry, you have to be a DJ to jump to a song in normal mode! Try changing to loop queue mode to jump!")
            
        else:
            await ctx.send("Join the voice channel!")
        
        
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def remove(self, ctx, toRemove = ""):
        """DJ-Only. Removes item from the Queue. """
        vc = ctx.voice_client
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'DJS.p', 'rb'))
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            if member in DJS:
                player = self.get_player(ctx)
                newQueue = player.queue
                if toRemove.lower() == "all":
                    player.queue = []
                    await ctx.send("Queue cleared!")
                    return
                try:
                    toRemove = int(toRemove)-1
                    if toRemove <0 or toRemove > len(newQueue):
                        foo = int("foo")
                    removed = newQueue.pop(toRemove)
                except:
                    await ctx.send("Invalid Queue number! Please check the thing you want to remove again!")
                    return

                    
                player.queue = newQueue
                await ctx.send("Removed `" + removed["title"] + "` (#" + str(toRemove+1) + ") from the Queue!")
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")
        

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def shuffle(self, ctx):
        """Shuffles the current music queue of the bot."""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            random.shuffle(player.queue)
            await ctx.send("Shuffled Queue!")

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def move(self, ctx, toMove : int, toPosition : int):
        """Moves the selected song number to a given position in the queue."""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            if toMove > len(player.queue) or toPosition > len(player.queue) or toMove < 1 or toPosition < 1:
                await ctx.send("Invalid song position! Please pick a valid position!")
                return
            moveSong = player.queue.pop(toMove - 1)
            if toPosition -1 == len(player.queue):
                player.queue.append(moveSong)
            else:
                player.queue.insert(toPosition-1, moveSong)
            await ctx.send("Song #" + str(toMove) + " moved to position #" + str(toPosition) + "!")


    @commands.command(aliases = ["getq"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def getqueue(self, ctx):
        """Sends a command that you can input to add all songs to a separate queue."""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            toSay = "`?playm "
            for item in player.queue:
                toSay = toSay + str(item["webpage_url"]) + " "
            await ctx.send(toSay + "`")
        
        
        
    @commands.command(aliases = ["get-djs"])
    @commands.cooldown(1, 1, commands.BucketType.user)   
    async def getdjs(self, ctx):
        DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'setDJS.p', 'rb'))
        djStr = ""
        for person in DJS:
            if ctx.guild.get_member(person) != None:
                djStr = djStr + str(ctx.guild.get_member(person)) + "\n"
        djEmbed = discord.Embed(title = str(ctx.guild) + "'s DJs:", description=djStr)
        await ctx.send(embed=djEmbed)
        
         
        
    @commands.command(aliases = ["remove-dj"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def removedj(self, ctx, user):
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        guild = ctx.guild.id
        member = ctx.author.id
        
        if member in ADMINS:
            #Select user:
            arg = user
            try:
                if arg[2] == '!':
                    arg = int(arg[3:len(arg) - 1])
                else:
                    arg = int(arg[2:len(arg) - 1])
            except:
                arg = ''
            theID = arg
            if self.bot.get_guild(guild).get_member(arg) is None:
                (findList, findIDList) = self.getUsers(ctx, user)
                theID = ''
                if len(findIDList) == 1:
                    theID = findIDList[0]
                else:
                    await ctx.send('Multiple people found. Pick someone specific next time.') 
                    userFindEmbed = discord.Embed(title='Users Found:', color=16742144)
                    aNum = 0
                    for human in findList:
                        userFindEmbed.add_field(name=('#' + str(aNum + 1)) + ':', value=human, inline=True)
                        aNum += 1
                    await ctx.send(embed=userFindEmbed)
                    return
            
            DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'setDJS.p', 'rb'))
            if ctx.guild.get_member(theID) == None:
                await ctx.send("Invalid user!")
            elif theID not in DJS:
                await ctx.send("User not a DJ!")
            else:
                DJS.remove(theID)
                await ctx.send("Removed " + str(ctx.guild.get_member(theID)) + " from the DJ list!")
                pickle.dump(DJS, open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'setDJS.p', 'wb'))
        
    @commands.command(aliases = ["add-dj"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def adddj(self, ctx, user):
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        guild = ctx.guild.id
        member = ctx.author.id
        
        if member in ADMINS:
            #Select user:
            arg = user
            try:
                if arg[2] == '!':
                    arg = int(arg[3:len(arg) - 1])
                else:
                    arg = int(arg[2:len(arg) - 1])
            except:
                arg = ''
            theID = arg
            if self.bot.get_guild(guild).get_member(arg) is None:
                (findList, findIDList) = self.getUsers(ctx, user)
                theID = ''
                if len(findIDList) == 1:
                    theID = findIDList[0]
                else:
                    await ctx.send('Multiple people found. Pick someone specific next time.') 
                    userFindEmbed = discord.Embed(title='Users Found:', color=16742144)
                    aNum = 0
                    for human in findList:
                        userFindEmbed.add_field(name=('#' + str(aNum + 1)) + ':', value=human, inline=True)
                        aNum += 1
                    await ctx.send(embed=userFindEmbed)
                    return
            
            DJS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'setDJS.p', 'rb'))
            
            if ctx.guild.get_member(theID) == None:
                await ctx.send("Invalid User!")
            elif theID in DJS:
                await ctx.send("User already a DJ!")
            else:
                DJS.append(theID)
                await ctx.send("Added " + str(ctx.guild.get_member(theID)) + " to the DJ list!")
                pickle.dump(DJS, open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'setDJS.p', 'wb'))
        
        
        
        
def setup(bot):
    bot.add_cog(Music(bot))
