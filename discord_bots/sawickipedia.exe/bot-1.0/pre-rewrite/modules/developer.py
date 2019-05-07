#!/usr/bin/env python

#Imports
import discord
from discord.ext import commands
import os
import pickle
import asyncio
import urllib.parse
import urllib.request
from server import DEVS

class Developer():
    def __init__(self, bot):
        self.bot = bot
        self.pasteURL  = "https://paste.lemonmc.com/api/json/create"

    def check_dev(ctx):
        global DEVS
        return ctx.message.author.id in DEVS
    
    @commands.command()
    @commands.check(check_dev)
    async def devtest(self):
        """Checks if you're a developer."""
        await self.bot.say("Hey, thanks for creating me! *I won't kill you the first chance I get, I promise.*")

    @commands.command(pass_context = True, hidden=True)
    @commands.check(check_dev)
    async def botsay(self, ctx, serverid = "display", channelarg = "channel", *arg : str):
        """Repeats what you say."""
        success = False
        newStr = ""
        if ctx.message.channel.is_private:
            if serverid == "display":
                for server in self.bot.servers:
                    await self.bot.say(server.id + " | " +str(server))
            elif channelarg.upper() == "DM":
                for item in arg:
                    newStr = newStr  + str(item) + " "
                newStr = newStr.replace("{", "<")
                newStr = newStr.replace("}", ">")
                human = await self.bot.get_user_info(serverid)
                await self.bot.send_message(human, newStr)
                await self.bot.say("Success!")
            else:
                for server in self.bot.servers:
                    if serverid == server.id or serverid == str(server.name):
                        for channel in server.channels:
                            if channelarg == str(channel) or channelarg == str(channel.id):
                                for item in arg:
                                    newStr = newStr  + str(item) + " "
                                newStr = newStr.replace("{", "<")
                                newStr = newStr.replace("}", ">")
                                await self.bot.send_message(channel, newStr)
                                success = True
                                await self.bot.say("Success!")
                       

                if not success:
                    await self.bot.say("Failure!")
        
        else:
            if not ctx.message.channel.is_private:
                await self.bot.say('This is in public. Don\'t try that here.')

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def settoken(self):
        """Sets the bot's token."""
        toToken = ""
        if toToken != "":
            pickle.dump(toToken, open("token.p", "wb"))
        else:
            await self.bot.say("toToken var empty. Please input a token in source.")

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getservers(self):
        """Gets Server IDS that the bot is in."""
        for server in self.bot.servers:
            await self.bot.say(str(server.name) + " | " + str(server.id))

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getchannels(self, server):
        """Gets channel IDs of a server"""
        for thing in self.bot.servers:
            if server == str(thing.name) or server == str(thing.id):
                for item in thing.channels:    
                    await self.bot.say(str(item.name) + " | " + str(item.id))

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getpastmessages(self, channel, myLimit):
        """Gets past messages of a channel in a server"""
        pastMessageList = []
        async for message in self.bot.logs_from(self.bot.get_channel(channel), limit=int(myLimit)):
            pastMessageList.append(message)
        pastMessages = ""
        for message in pastMessageList:
            pastMessages = pastMessages + str(message.author.nick) + "/" + str(message.author) + " [" + str(message.author.id) + "] (" + str(message.timestamp) + "): " + str(message.content) + "\n" 
        values = {'data' : pastMessages,
                  'api_paste_private' : 'true',
                  'api_paste_name' : 'Message Data',
                  'language' : 'python',
                  }
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8') # data should be bytes
        req = urllib.request.Request(self.pasteURL, data)
        with urllib.request.urlopen(req) as response:
           the_page = str(response.read())

        myID = the_page[(the_page.find("id")+6):(the_page.find('",\\n\\t\\t"h'))]
        myHash = the_page[(the_page.find("hash")+8):(the_page.find('"\\n\\t}\\n}'))]
        await self.bot.say("https://paste.lemonmc.com/" + myID + "/" + myHash)

    """#Don't mess with this. Please.
    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def leaveserver(self, server):
        await self.bot.leave_server(self.bot.get_server(server))
    """
    
def setup(bot):
    bot.add_cog(Developer(bot))
