#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os
import re
import json
import urllib.parse
import urllib.request
import io
import sys
import inspect


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.paste_URL = 'https://paste.lemonmc.com/api/json/create'
        
    def check_dev(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return str(ctx.author.id) in devs
        
    
    @commands.command(hidden=True)
    @commands.check(check_dev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def devtest(self, ctx):
        """Checks if you're a developer."""
        #USEFUL INFO HERE IN COMMENTS BTW
        """
        Use this to have except statements print the exception:
            await ctx.send("```css\n[{}]\n```".format(e))
            
        """
        await ctx.send("Hey, thanks for creating me! *I won't kill you the first chance I get, I promise.*")
        
    @commands.command(hidden=True)
    @commands.check(check_dev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def getdevs(self, ctx):
        """Gets all the developer IDs."""
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        await ctx.send(devs)
    
    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def botsay(self, ctx, guildid='display', channelarg='channel', *arg: str):
        success = False
        new_str = ''
        if guildid == 'display':
            to_send = ''
            for guild in self.bot.guilds:
                to_send = to_send + (str(guild.name) + ' | ') + str(guild.id) + "\n"
                my_embed = discord.Embed(title="**Guild List**", description=to_send)
            await ctx.send(embed=my_embed)  
            success = True
        elif channelarg.upper() == 'DM':
            for item in arg:
                new_str = (new_str + str(item)) + ' '
            result = re.findall(r':(.*?):', new_str)
            emoji_found = False
            for item in result:
                for guild in self.bot.guilds:
                    for emote in guild.emojis:
                        if emote.name == item and emoji_found == False:
                            new_str = new_str.replace(":" + item + ":", "<:" + emote.name + ":" + str(emote.id) + ">")
                            emoji_found = True
                    
            human = await self.bot.fetch_user(guildid)
            await human.send(new_str)
            success = True
            await ctx.send('Success!')
        else:
            for guild in self.bot.guilds:
                if (guildid == guild.id) or (guildid == str(guild.name)):
                    for channel in guild.channels:
                        if (channelarg == str(channel)) or (channelarg == str(channel.id)):
                            for item in arg:
                                new_str = (new_str + str(item)) + ' '

                            result = re.findall(r':(.*?):', new_str)
                            emoji_found = False
                            for item in result:
                                for guild in self.bot.guilds:
                                    for emote in guild.emojis:
                                        if emote.name == item and emojiFound == False:
                                            new_str = new_str.replace(":" + item + ":", "<:" + emote.name + ":" + str(emote.id) + ">")
                                            emoji_found = True
                               
                            await channel.send(new_str)
                            success = True
                            await ctx.send('Success!')
        if (not success):
            await ctx.send('Failure!')
            
            
    @commands.command(aliases=["getservers"], hidden=True)
    @commands.check(check_dev)
    async def getguilds(self, ctx):
        '''Gets Server IDs that the bot is in.'''
        to_send = ''
        for guild in self.bot.guilds:
            to_send = to_send + (str(guild.name) + ' | ') + str(guild.id) + "\n"
        my_embed = discord.Embed(title="**Guild List**", description=to_send)
        await ctx.send(embed=my_embed)        
            
            
    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getchannels(self, ctx, guild):
        '''Gets channel IDs of a server'''
        to_send = ""
        for thing in self.bot.guilds:
            if (guild == str(thing.name)) or (guild == str(thing.id)):
                for item in thing.channels:
                    to_send = to_send + (str(item.name) + ' | ') + str(item.id) + "\n"
        my_embed = discord.Embed(title="**Guild List**", description=to_send)
        await ctx.send(embed=my_embed)        
            
            
    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getpastmessages(self, ctx, channel = "here", my_limit = None):
        '''Gets past messages of a channel in a server. Use "?getpastmessages here" to use this channel.'''
        if channel == "here":
            channel = ctx.channel.id
        await ctx.send("Starting...")
        if my_limit is not None:
            my_limit = int(my_limit)
        message_hist = await self.bot.get_channel(int(channel)).history(limit=my_limit).flatten()
        await ctx.send("Evaluating "+ str(len(message_hist)) + " messages. It may be a while. Or not, I don't know. Or care.")
        past_messages = ""
        async for message in self.bot.get_channel(int(channel)).history(limit=my_limit):
            if message.attachments == []:
                past_messages = '({}) [{}] {}: {}\n'.format(str(message.created_at), str(message.author.id), str(message.author), str(message.content)) + past_messages
            else:
                attach_string = ""
                for attachment in message.attachments:
                    attach_string = attachment.url + ", " + attachString
                past_messages = '({}) [{}] {}: {} | Attachments: {}\n'.format(str(message.created_at), str(message.author.id), str(message.author), str(message.content), attach_string) + past_messages
        await ctx.send("Pasting data...")
        with open("pastmessages.txt", "w") as my_file:
            print(past_messages.encode('ascii', 'ignore'), file=my_file)
        values = {
            'data': past_messages,
            'api_paste_private': 'true',
            'api_paste_name': 'Message Data',
            'language': 'python',
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.paste_URL, data)
        with urllib.request.urlopen(req) as response:
            the_page = str(response.read())
        my_ID = the_page[the_page.find('id') + 6:the_page.find('",\\n\\t\\t"h')]
        my_hash = the_page[the_page.find('hash') + 8:the_page.find('"\\n\\t}\\n}')]
        await ctx.send((('https://paste.lemonmc.com/{}/{}/raw'.format(my_ID, my_hash))))
            
            
    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getperms(self, ctx, serverid=0, userid=421015092830666754):
        '''Checks permission levels in a server'''
        try:
            serverid = int(serverid)
            userid = int(userid)
        except:
            await ctx.send("TypeError! Use valid args!")
        server = self.bot.get_guild(serverid)
        if server == None:
            await ctx.send("Invalid server!")
            return
        member = server.get_member(userid)
        if member == None:
            await ctx.send("Invalid member!")
            return
        my_perms = member.guild_permissions
        my_pretty_perms = "```\nKick Members: " + str(my_perms.kick_members) + "\nBan Members: " + str(my_perms.ban_members) + "\nAdministrator: " + str(my_perms.administrator) + "\nManage Channels: " + str(my_perms.manage_channels) + "\nManage Guild: " + str(my_perms.manage_guild) + "\nAdd Reactions: " + str(my_perms.add_reactions) + "\nView Audit Log: " + str(my_perms.view_audit_log) + "\nPriority Speaker: " + str(my_perms.priority_speaker) + "\nRead Messages: " + str(my_perms.read_messages) + "\nSend Messages: " + str(my_perms.send_messages) + "\nSend TTS: " + str(my_perms.send_tts_messages) + "\nManage Messages: " + str(my_perms.manage_messages) + "\nEmbed Links: " + str(my_perms.embed_links) + "\nAttach Files: " + str(my_perms.attach_files) + "\nMention Everyone: " + str(my_perms.mention_everyone) + "\nExternal Emojis: " + str(my_perms.external_emojis) + "\nConnect: " + str(my_perms.connect) + "\nSpeak: " + str(my_perms.speak) + "\Mute Members: " + str(my_perms.mute_members) + "\nDeafen Members: " + str(my_perms.deafen_members) + "\nMove Members: " + str(my_perms.move_members) + "\nUse Voice Activation: " + str(my_perms.use_voice_activation) + "\nChange Nickname: " + str(my_perms.change_nickname) + "\nManage Nicknames: " + str(my_perms.manage_nicknames) + "\nManage Roles: " + str(my_perms.manage_roles) + "\nManage Webhooks: " + str(my_perms.manage_webhooks) + "\nManage Emojis: " + str(my_perms.manage_emojis) + "\n```"

        await ctx.send(my_pretty_perms)
        
    @commands.command(hidden=True,name="print")
    @commands.check(check_dev)
    async def print_(self, ctx, *, arg : str):
        '''Prints to log.'''
        print(arg)
                
            
    @commands.command(hidden=True, name="evaluate", aliases = ["eval"])
    @commands.check(check_dev)
    async def evaluate_(self, ctx, *, to_eval : str):
        """Evaluates raw Python code. BE CAREFUL."""
        if to_eval == "":
            await ctx.send("No code inputted.")
            return
        
        first= "```python"
        last = "```"
        start = to_eval.index( first ) + len( first )
        end = to_eval.index( last, start )
        to_eval = to_eval[start:end]
        sys.stdout = log_buffer = io.StringIO()
        try:
            output = eval(to_eval)
            if inspect.isawaitable(output):
                output = await output
            out_embed = discord.Embed(title = "Code evaluated!", color = 0x00FF00)
            out_embed.description = "```python\n{output}\n```".format(output=output)
        except Exception as e:
            out_embed = discord.Embed(title = "Error!", color = 0xFF0000)
            out_embed.description = "```python\n{e}\n```".format(e=e)
            
        
        to_send = log_buffer.getvalue()
        log_buffer.close()
        await ctx.send("```python\n{}\n```".format(to_send), embed=out_embed)

    @commands.command(hidden=True, name="execute", aliases = ["exec"])
    @commands.check(check_dev)
    async def execute_(self, ctx, *, to_eval : str):
        """Executes raw Python code. BE CAREFUL."""
        if to_eval == "":
            await ctx.send("No code inputted.")
            return
        
        first= "```python"
        last = "```"
        start = to_eval.index( first ) + len( first )
        end = to_eval.index( last, start )
        to_eval = to_eval[start:end]
        sys.stdout = log_buffer = io.StringIO()
        try:
            output = exec(to_eval)
            if inspect.isawaitable(output):
                output = await output
            out_embed = discord.Embed(title = "Code evaluated!", color = 0x00FF00)
            out_embed.description = "```python\n{output}\n```".format(output=output)
        except Exception as e:
            out_embed = discord.Embed(title = "Error!", color = 0xFF0000)
            out_embed.description = "```python\n{e}\n```".format(e=e)
            
        
        to_send = log_buffer.getvalue()
        log_buffer.close()
        await ctx.send("```python\n{}\n```".format(to_send), embed=out_embed)        
            

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getaudit(self, ctx, serverid=0, my_limit = 100):    
        """Gets the audit logs for a server"""
        try:
            serverid = int(serverid)
            my_limit = int(my_limit)
        except:
            await ctx.send("TypeError! Use valid args!")
            return
        server = self.bot.get_guild(serverid)
        if server == None:
            await ctx.send("Invalid server!")
            return
        
        await ctx.send("Getting data...")
        audit_data = ""
        async for entry in server.audit_logs():
            for thing in iter(entry.before):
                pretty_before = str(thing) + " | "
            pretty_before = pretty_before[:len(pretty_before)-3]
            for thing in iter(entry.after):
                pretty_after = str(thing) + " | "
            pretty_after = pretty_after[:len(pretty_after)-3]
            pretty_entry = "User: " + str(entry.user) + " | Target: " +  str(entry.target) + " | Creation Date: " + str(entry.created_at) + " | Action: " + str(entry.action) + " | Before: " + str(pretty_before) + " | After: " + str(pretty_after)
            
            audit_data = audit_data + str(pretty_entry) + "\n"
            
        
        values = {
            'data': audit_data,
            'api_paste_private': 'true',
            'api_paste_name': 'Message Data',
            'language': 'python',
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.paste_URL, data)
        with urllib.request.urlopen(req) as response:
            the_page = str(response.read())
        my_ID = the_page[the_page.find('id') + 6:the_page.find('",\\n\\t\\t"h')]
        my_hash = the_page[the_page.find('hash') + 8:the_page.find('"\\n\\t}\\n}')]
        await ctx.send((('https://paste.lemonmc.com/{}/{}/raw'.format(my_ID, my_hash))))


    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getstats(self, ctx, serverid=0, *, ignorechannels : str = "none"):
        if ignorechannels[0].lower() == "none":
            ignorechannels = []
        try:
            serverid = int(serverid)
        except:
            await ctx.send("TypeError! Use valid args!")
            return
        if serverid == 0:
            serverid = ctx.guild.id
        server = self.bot.get_guild(serverid)
        if server == None:
            await ctx.send("Invalid server!")
            return
        
        total_messages = 0
        user_message_dict = {}
        channel_message_dict = {}
        await ctx.send("Getting data...")
        for channel in server.channels:
            if isinstance(channel, discord.TextChannel):
                if str(channel.id) in ignorechannels:
                    pass
                else:
                    channel_message_dict[channel.name] = 0
                    async for message in channel.history(limit=None):
                        total_messages += 1
                        channel_message_dict[channel.name] += 1
                        try:
                            user_message_dict[message.author] += 1
                        except:
                            user_message_dict[message.author] = 0
        
        channel_str = "```\nCHANNELS:\n"
        member_str = "```\nUSERS:\n"
        user_message_dict_sorted = sorted(user_message_dict.items(), key=lambda kv: kv[1], reverse=True)
        channel_message_dict_sorted = sorted(channel_message_dict.items(), key=lambda kv: kv[1], reverse=True)
        x = 1
        
        await ctx.send("```\nTotal Messages: " + str(total_messages) + "\n```")
        for key, value in channel_message_dict_sorted:
            channel_str = channel_str + str(x) + ") #" + str(key) + "'s Messages: " + str(value) + "\n"
            x+=1
        x = 1
        for key, value in user_message_dict_sorted:
            member_str = member_str + str(x) + ") " + str(key) + "'s Messages: " + str(value) + "\n"
            x+=1
            
        if len(channel_str) < 1800:
            await ctx.send(channel_str[:1500] + "```")
        else:
            await ctx.send(channel_str[:1500] + "```")
            for x in range (0, len(channel_str) // 1500):
                if (len(channel_str) < (2+x) * 1500):
                    await ctx.send("```\n" + channel_str[1500 * (1+x): 1500 * (2+x)] + "```")
                else:
                    await ctx.send("```\n" + channel_str[1500 * (1+x):] + "```")
                    
        if len(member_str) < 1800:
            await ctx.send(member_str[:1500] + "```")
        else:
            await ctx.send(member_str[:1500] + "```")
            for x in range (0, len(member_str) // 1500):
                if (len(member_str) < (2+x) * 1500):
                    await ctx.send("```\n" + member_str[1500 * (1+x): 1500 * (2+x)] + "```")
                else:
                    await ctx.send("```\n" + member_str[1500 * (1+x):] + "```")
        await ctx.send("Done!")
















def setup(bot):
    bot.add_cog(Developer(bot))