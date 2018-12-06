#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os  
import pickle
import asyncio
import urllib.parse
import urllib.request
import re
import inspect
from server import DEVS
import io
import sys

class Developer():
    def __init__(self, bot):
        self.bot = bot
        self.pasteURL = 'https://paste.lemonmc.com/api/json/create'

    def check_dev(ctx):
        global DEVS
        return ctx.author.id in DEVS

    @commands.command()
    @commands.check(check_dev)
    async def devtest(self, ctx):
        """Checks if you're a developer."""
        await ctx.send("Hey, thanks for creating me! *I won't kill you the first chance I get, I promise.*")

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def botsay(self, ctx, guildid='display', channelarg='channel', *arg: str):
        '''Repeats what you say.'''
        success = False
        newStr = ''
        if guildid == 'display':
            for guild in self.bot.guilds:
                await ctx.send((guild.id + ' | ') + str(guild))
            success = True
        elif channelarg.upper() == 'DM':
            for item in arg:
                newStr = (newStr + str(item)) + ' '
            result = re.findall(r':(.*?):', newStr)
            emojiFound = False
            for item in result:
                for guild in self.bot.guilds:
                    for emote in guild.emojis:
                        if emote.name == item and emojiFound == False:
                            newStr = newStr.replace(":" + item + ":", "<:" + emote.name + ":" + str(emote.id) + ">")
                            emojiFound = True
                    
            human = await self.bot.get_user_info(guildid)
            await human.send(newStr)
            success = True
            await ctx.send('Success!')
        else:
            for guild in self.bot.guilds:
                if (guildid == guild.id) or (guildid == str(guild.name)):
                    for channel in guild.channels:
                        if (channelarg == str(channel)) or (channelarg == str(channel.id)):
                            for item in arg:
                                newStr = (newStr + str(item)) + ' '

                            result = re.findall(r':(.*?):', newStr)
                            emojiFound = False
                            for item in result:
                                for guild in self.bot.guilds:
                                    for emote in guild.emojis:
                                        if emote.name == item and emojiFound == False:
                                            newStr = newStr.replace(":" + item + ":", "<:" + emote.name + ":" + str(emote.id) + ">")
                                            emojiFound = True
                               
                            await channel.send(newStr)
                            success = True
                            await ctx.send('Success!')
        if (not success):
            await ctx.send('Failure!')

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def settoken(self, ctx):
        """Sets the bot's token."""
        toToken = ''
        if toToken != '':
            pickle.dump(toToken, open('token.p', 'wb'))
        else:
            await ctx.send('toToken var empty. Please input a token in source.')

    @commands.command(aliases=["getservers"], hidden=True)
    @commands.check(check_dev)
    async def getguilds(self, ctx):
        '''Gets Server IDS that the bot is in.'''
        toSend = ''
        for guild in self.bot.guilds:
            toSend = toSend + (str(guild.name) + ' | ') + str(guild.id) + "\n"
        myEmbed = discord.Embed(title="**Guild List**", description=toSend)
        await ctx.send(embed=myEmbed)
        

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getchannels(self, ctx, guild):
        '''Gets channel IDs of a server'''
        toSend = ""
        for thing in self.bot.guilds:
            if (guild == str(thing.name)) or (guild == str(thing.id)):
                for item in thing.channels:
                    toSend = toSend + (str(item.name) + ' | ') + str(item.id) + "\n"
        myEmbed = discord.Embed(title="**Guild List**", description=toSend)
        await ctx.send(embed=myEmbed)

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getpastmessages(self, ctx, channel, myLimit = None):
        '''Gets past messages of a channel in a server'''
        await ctx.send("Starting...")
        if myLimit is not None:
            myLimit = int(myLimit)
        messageHist = await self.bot.get_channel(int(channel)).history(limit=myLimit).flatten()
        await ctx.send("Evaluating "+ str(len(messageHist)) + " messages. It may be a while. Or not, I don't know. Or care.")
        pastMessages = ""
        async for message in self.bot.get_channel(int(channel)).history(limit=myLimit):
            pastMessages = '(' + str(message.created_at) + ') [' + str(message.author.id) + '] '  + str(message.author)+ ": " + str(message.content) + '\n' + pastMessages
        await ctx.send("Pasting data...")
        with open("pastmessages.txt", "w") as myFile:
            print(pastMessages.encode('ascii', 'ignore'), file=myFile)
        values = {
            'data': pastMessages,
            'api_paste_private': 'true',
            'api_paste_name': 'Message Data',
            'language': 'python',
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.pasteURL, data)
        with urllib.request.urlopen(req) as response:
            the_page = str(response.read())
        myID = the_page[the_page.find('id') + 6:the_page.find('",\\n\\t\\t"h')]
        myHash = the_page[the_page.find('hash') + 8:the_page.find('"\\n\\t}\\n}')]
        await ctx.send((('https://paste.lemonmc.com/' + myID) + '/') + myHash + "/raw")

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
        myPerms = member.guild_permissions
        myPrettyPerms = "```\nKick Members: " + str(myPerms.kick_members) + "\nBan Members: " + str(myPerms.ban_members) + "\nAdministrator: " + str(myPerms.administrator) + "\nManage Channels: " + str(myPerms.manage_channels) + "\nManage Guild: " + str(myPerms.manage_guild) + "\nAdd Reactions: " + str(myPerms.add_reactions) + "\nView Audit Log: " + str(myPerms.view_audit_log) + "\nPriority Speaker: " + str(myPerms.priority_speaker) + "\nRead Messages: " + str(myPerms.read_messages) + "\nSend Messages: " + str(myPerms.send_messages) + "\nSend TTS: " + str(myPerms.send_tts_messages) + "\nManage Messages: " + str(myPerms.manage_messages) + "\nEmbed Links: " + str(myPerms.embed_links) + "\nAttach Files: " + str(myPerms.attach_files) + "\nMention Everyone: " + str(myPerms.mention_everyone) + "\nExternal Emojis: " + str(myPerms.external_emojis) + "\nConnect: " + str(myPerms.connect) + "\nSpeak: " + str(myPerms.speak) + "\Mute Members: " + str(myPerms.mute_members) + "\nDeafen Members: " + str(myPerms.deafen_members) + "\nMove Members: " + str(myPerms.move_members) + "\nUse Voice Activation: " + str(myPerms.use_voice_activation) + "\nChange Nickname: " + str(myPerms.change_nickname) + "\nManage Nicknames: " + str(myPerms.manage_nicknames) + "\nManage Roles: " + str(myPerms.manage_roles) + "\nManage Webhooks: " + str(myPerms.manage_webhooks) + "\nManage Emojis: " + str(myPerms.manage_emojis) + "\n```"

        await ctx.send(myPrettyPerms)

    @commands.command(hidden=True,name="print")
    @commands.check(check_dev)
    async def print_(self, ctx, *arg : str):
        '''Prints to log.'''
        thing = ""
        for item in arg:
            thing = thing + item
        print(thing)
        
    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def checkvar(self, ctx, *filepathtemp : str):
        """Checks the value of a variable. Use spaces for slashes."""
        filepath = ""
        for thing in filepathtemp:
            filepath = filepath + thing + os.sep
        filepath = filepath[:len(filepath)-1]
        
        toCheck = pickle.load(open(filepath, "rb"))
        await ctx.send("```python" + "\n" +
                        str(type(toCheck)) + "\n" +
                        str(toCheck) + "\n" +
                        "```"
                        )
        
    @commands.command(hidden=True, name="evaluate", aliases = ["eval"])
    @commands.check(check_dev)
    async def evaluate_(self, ctx, *, toEval : str):
        """Evaluates raw Python code. BE CAREFUL."""
        if toEval == "":
            await ctx.send("No code inputted.")
            return
        
        first= "```python"
        last = "```"
        start = toEval.index( first ) + len( first )
        end = toEval.index( last, start )
        toEval = toEval[start:end]
        sys.stdout = logBuffer = io.StringIO()
        try:
            output = eval(toEval)
            if inspect.isawaitable(output):
                output = await output
            outEmbed = discord.Embed(title = "Code evaluated!", color = 0x00FF00)
            outEmbed.description = "```python\n{output}\n```".format(output=output)
        except Exception as e:
            outEmbed = discord.Embed(title = "Error!", color = 0xFF0000)
            outEmbed.description = "```python\n{e}\n```".format(e=e)
            
        
        toSend = logBuffer.getvalue()
        logBuffer.close()
        await ctx.send("```python\n{toSend}\n```".format(toSend=toSend), embed=outEmbed)

    @commands.command(hidden=True, name="execute", aliases = ["exec"])
    @commands.check(check_dev)
    async def execute_(self, ctx, *, toEval : str):
        """Executes raw Python code. BE CAREFUL."""
        if toEval == "":
            await ctx.send("No code inputted.")
            return
        
        first= "```python"
        last = "```"
        start = toEval.index( first ) + len( first )
        end = toEval.index( last, start )
        toEval = toEval[start:end]
        sys.stdout = logBuffer = io.StringIO()
        try:
            output = exec(toEval)
            if inspect.isawaitable(output):
                output = await output
            outEmbed = discord.Embed(title = "Code evaluated!", color = 0x00FF00)
            outEmbed.description = "```python\n{output}\n```".format(output=output)
        except Exception as e:
            outEmbed = discord.Embed(title = "Error!", color = 0xFF0000)
            outEmbed.description = "```python\n{e}\n```".format(e=e)
            
        
        toSend = logBuffer.getvalue()
        logBuffer.close()
        await ctx.send("```python\n{toSend}\n```".format(toSend=toSend), embed=outEmbed)
    
    
    
    
    @commands.command()
    @commands.check(check_dev)
    async def getaudit(self, ctx, serverid=0, myLimit = 100):    
        """Gets the audit logs for a server"""
        try:
            serverid = int(serverid)
            myLimit = int(myLimit)
        except:
            await ctx.send("TypeError! Use valid args!")
        server = self.bot.get_guild(serverid)
        if server == None:
            await ctx.send("Invalid server!")
            return
        
        await ctx.send("Getting data...")
        auditData = ""
        async for entry in server.audit_logs():
            for thing in iter(entry.before):
                prettyBefore = str(thing) + " | "
            prettyBefore = prettyBefore[:len(prettyBefore)-3]
            for thing in iter(entry.after):
                prettyAfter = str(thing) + " | "
            prettyAfter = prettyAfter[:len(prettyAfter)-3]
            prettyEntry = "User: " + str(entry.user) + " | Target: " +  str(entry.target) + " | Creation Date: " + str(entry.created_at) + " | Action: " + str(entry.action) + " | Before: " + str(prettyBefore) + " | After: " + str(prettyAfter)
            
            auditData = auditData + str(prettyEntry) + "\n"
            
        
        values = {
            'data': auditData,
            'api_paste_private': 'true',
            'api_paste_name': 'Message Data',
            'language': 'python',
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(self.pasteURL, data)
        with urllib.request.urlopen(req) as response:
            the_page = str(response.read())
        myID = the_page[the_page.find('id') + 6:the_page.find('",\\n\\t\\t"h')]
        myHash = the_page[the_page.find('hash') + 8:the_page.find('"\\n\\t}\\n}')]
        await ctx.send((('https://paste.lemonmc.com/' + myID) + '/') + myHash + "/raw")
    
    
    
    
            
def setup(bot):
    bot.add_cog(Developer(bot))
 
