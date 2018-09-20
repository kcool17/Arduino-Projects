#!/usr/bin/env python
import discord
from discord.ext import commands

import pickle
import os
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from server import DEVS


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
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

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send('```ini\n[Added {title} to the Queue.]\n```'.format(title = data["title"]))

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

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

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'loop', 'skipLoop', 'skipVote', 'loopVote')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None
        
        self.loop = False
        self.skipLoop = False
        self.skipVote = []
        self.loopVote = []

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            
            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    if self.loop == False or self.skipLoop == True:
                        source = await self.queue.get()
                        oldSource = source
                        self.skipLoop = False
                    else:
                        source = oldSource
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send('There was an error processing your song.\n'
                                             '```css\n[{e}]\n```'.format(e=e))
                    continue

            source.volume = self.volume

            
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            if not self.loop:
                self.np = await self._channel.send('**Now Playing:** `{title}` requested by '
                                               '`{requester}`'.format(title = source.title, requester = source.requester))

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
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice. DJ-Only, if already connected. (Note: DJ is someone with Manage Channels permissions)
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

    @commands.command(name='play', aliases=['sing'])
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
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

            await player.queue.put(source)
        else:
            await ctx.send("Join the voice channel!")

    @commands.command(name='pause')
    async def pause_(self, ctx):
        """DJ-Only. Pause the currently playing song. (Note: DJ is someone with Manage Channels permissions)"""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
            if ctx.author.guild_permissions.manage_channels or member in ADMINS:
                if not vc or not vc.is_playing():
                    return await ctx.send('I am not currently playing anything!')
                elif vc.is_paused():
                    return

                vc.pause()
                await ctx.send('**`{author}`**: Paused the song!'.format(author=ctx.author))
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")

    @commands.command(name='resume')
    async def resume_(self, ctx):
        """DJ-Only. Resume the currently paused song. (Note: DJ is someone with Manage Channels permissions)"""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
            if ctx.author.guild_permissions.manage_channels or member in ADMINS:
                if not vc or not vc.is_connected():
                    return await ctx.send('I am not currently playing anything!')
                elif not vc.is_paused():
                    return

                vc.resume()
                await ctx.send('**`{author}`**: Resumed the song!'.format(author=ctx.author))
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")

    @commands.command(name='skip')
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            player = self.get_player(ctx)
            guild = ctx.guild.id
            member = ctx.author.id
            ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
            if not vc or not vc.is_connected():
                return await ctx.send('I am not currently playing anything!')
            vcMembers = vc.channel.members
            if vc.is_paused():
                pass
            elif not vc.is_playing():
                return
            for person in vcMembers:
                if person.id in player.skipVote:
                    player.skipVote.remove(person.id)
            if ctx.author.guild_permissions.manage_channels or member in ADMINS:
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
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')

        upcoming = list(player.queue._queue)
        fmt = ""
        z = 1
        for x in upcoming:
            fmt = fmt + '\n' + '**' + str(z) + ". " + x['title'] + '**'
            z += 1
        embed = discord.Embed(title='Upcoming - Next {upcoming_len}'.format(upcoming_len=len(upcoming)), description=fmt, color=0x0000FF)

        await ctx.send(embed=embed)

    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')


        player.np = await ctx.send('**Now Playing:** `{title}` '
                                   'requested by `{requester}`'.format(title=vc.source.title, requester=vc.source.requester))

    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        """DJ-only. Change the player volume. (Note: DJ is someone with Manage Channels permissions)
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
            if ctx.author.guild_permissions.manage_channels or member in ADMINS:
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
    async def stop_(self, ctx):
        """DJ-Only. Stop the currently playing song and destroy the player. (Note: DJ is someone with Manage Channels permissions)
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
            if ctx.author.guild_permissions.manage_channels or member in ADMINS:
                if not vc or not vc.is_connected():
                    return await ctx.send('I am not currently playing anything!')

                await self.cleanup(ctx.guild)
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")


    @commands.command()
    async def loop(self, ctx):
        """Loops the currently playing song"""
        player = self.get_player(ctx)
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            if player.loop:
                await ctx.send("Loop Disabled!")
                player.loop = False
            else:
                await ctx.send("Loop Enabled!")
                player.loop = True
        else:
            await ctx.send("Join the voice channel!")

    @commands.command()
    async def clear(self, ctx):
        """DJ-Only. Clears the Queue. (Note: DJ is someone with Manage Channels permissions)"""
        vc = ctx.voice_client
        if ctx.author in vc.channel.members or ctx.author.id in DEVS:
            guild = ctx.guild.id
            member = ctx.author.id
            ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
            if ctx.author.guild_permissions.manage_channels or member in ADMINS:
                player = self.get_player(ctx)
                player.queue = asyncio.Queue()
                await ctx.send("Queue cleared!")
            else:
                await ctx.send("You're not a DJ! This isn't for you!")
        else:
            await ctx.send("Join the voice channel!")

def setup(bot):
    bot.add_cog(Music(bot))
