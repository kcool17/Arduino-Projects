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
            newStr = newStr.replace('{', '<')
            newStr = newStr.replace('}', '>')
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
                            newStr = newStr.replace('{', '<')
                            newStr = newStr.replace('}', '>')
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
        for guild in self.bot.guilds:
            await ctx.send((str(guild.name) + ' | ') + str(guild.id))

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def getchannels(self, ctx, guild):
        '''Gets channel IDs of a server'''
        for thing in self.bot.guilds:
            if (guild == str(thing.name)) or (guild == str(thing.id)):
                for item in thing.channels:
                    await ctx.send((str(item.name) + ' | ') + str(item.id))

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


def setup(bot):
    bot.add_cog(Developer(bot))
