#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import pickle  
import os
import random
import re
import asyncio

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getUsers(self, ctx, arg='noArg'):
        userList = []
        userIDList = []
        userNickList = []
        #Creates lists
        for person in ctx.guild.members:
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

    @commands.command(description='Add two numbers together. Change "num1" and "num2" to the numbers you wish to add together.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add(self, ctx, num1: int, num2: int):
        '''Adds stuff together.'''
        await ctx.send(num1 + num2)

    @commands.command(description='Use NdN format, with the first N the amount of rolls and the second the amount of sides on the die.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roll(self, ctx, dice: str):
        '''Rolls dice.'''
        try:
            (rolls, limit) = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        if rolls > 100:
            await ctx.send("Don't try and overload my CPU. I don't appreciate that.")
        elif limit > 1000000:
            await ctx.send('Do you *really* need to have over a million sides on this die? I mean, come *on*.')
        else:
            total = 0
            result = ''
            if rolls > 1:
                for r in range(rolls):
                    myRoll = random.randint(1, limit)
                    if r == 0:
                        result = str(myRoll)
                    else:
                        result = (result + ', ') + str(myRoll)
                    total = total + myRoll
                await ctx.send(result)
                await ctx.send('The total of your rolls is: ' + str(total))
            else:
                await ctx.send(random.randint(1, limit))

    @commands.command(description='Have as many options as you want after "?choose", with a space in between each one. One will be randomly chosen.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def choose(self, ctx, *choices: str):
        '''Chooses a random argument you give.'''
        newChoice = random.choice(choices)
        choiceEmbed = discord.Embed(title=str(ctx.author) + "'s Choices", description = newChoice, color=0x00FF00)
        await ctx.send(embed=choiceEmbed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def admintest(self, ctx):
        '''Checks if you have admin permissions in this server.'''
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if str(ctx.author.id) in ADMINS:
            await ctx.send('You are an administrator/developer!')
        else:
            await ctx.send('You are *not* an administrator/developer. How sad.')

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mentionuser(self, ctx, *user: str):
        '''Mentions the user based on input'''
        #USE THIS IN OTHER FUNCTIONS
        arg = ''
        for item in user:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        (findList, findIDList) = self.getUsers(ctx, arg)
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
        #PROGRAM STUFF HERE
        if theID != '':
            await ctx.send(('<@' + str(theID)) + '>')

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def findid(self, ctx, *user: str):
        '''Returns server ID and user ID.'''
        guild = ctx.guild.id
        member = ctx.author.id
        arg = ''
        for item in user:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        theID = ''  
        if arg != '':
            try:
                if arg[2] == '!':
                    member = int(arg[3:len(arg) - 1])
                else:
                    member = int(arg[2:len(arg) - 1])
            except:
                member = ''
            if self.bot.get_guild(guild).get_member(member) is None:
                (findList, findIDList) = self.getUsers(ctx, arg)
                theID = ''
                if len(findIDList) == 1:
                    member = findIDList[0]
                else:
                    await ctx.send('Multiple people found. Pick someone specific next time.')
                    userFindEmbed = discord.Embed(title='Users Found:', color=16742144)
                    aNum = 0
                    for human in findList:
                        userFindEmbed.add_field(name=('#' + str(aNum + 1)) + ':', value=human, inline=True)
                        aNum += 1
                    await ctx.send(embed=userFindEmbed)
                    return
            if self.bot.get_guild(guild).get_member(member) is None:
                await ctx.send('Invalid user, try again.')
            else:
                theID = member
        else:
            theID = ctx.author.id
        await ctx.send('Server: ' + str(ctx.guild.id))
        await ctx.send('Member: ' + str(theID))
        await ctx.send('Channel: ' + str(ctx.channel.id))

    @commands.command(description="Make an Embed with the info given. Use RRRGGGBBB format for color (0-256 for R, 0-256 for G, etc.), and name::value format for fields.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def embed(self, ctx, myTitle = "", myDescription= "", myColor = 0x000000, *nameValue):
        """Creates an Embed with the info given."""
        myNames = []
        myValues = []
        for item in nameValue:
            try:
                (myName, myValue) = map(str, item.split('::'))
                myNames.append(myName)
                myValues.append(myValue)
            except:
                pass
                
        try:
            myEmbed=discord.Embed(title=myTitle, description=myDescription, color=myColor)
        except:
            myEmbed=discord.Embed(title=myTitle, description=myDescription, color=0x000000)
        x=0
        for item in myNames:
            myEmbed.add_field(name=item, value=myValues[x], inline=False)
            x+=1
        await ctx.send(embed=myEmbed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def help(self, ctx, *commands : str):
        """Shows this message."""
        await ctx.send("Sorry, the `help` command is disabled for the time being! You'll have to wait for an update for that. In the meantime, check my GitHub if you *really* have to know a command name. Or just ask me, and I'll check GitHub.") 
        """
        bot = self.bot
        destination = ctx.message.author if bot.dm_help else ctx.message.channel
        pageNum = 1
        if len(commands) == 1:
            try:
                pageNum = int(commands[0])
                commands = []
            except:
                pass
        pageNum -=1
        
        _mentions_transforms = {'@everyone': '@\u200beveryone','@here': '@\u200bhere'}
        _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

        def repl(obj):
            return _mentions_transforms.get(obj.group(0), '')

        # help by itself just lists our own commands.
        if len(commands) == 0:
            pages = await bot.formatter.format_help_for(ctx, bot)
        elif len(commands) == 1:
            # try to see if it is a cog name
            name = _mention_pattern.sub(repl, commands[0])
            command = None
            if name in bot.cogs:
                command = bot.cogs[name]
            else:
                command = bot.all_commands.get(name)
                if command is None:
                    await destination.send(bot.command_not_found.format(name))
                    return

            pages = await bot.formatter.format_help_for(ctx, command)
        else:
            name = _mention_pattern.sub(repl, commands[0])
            command = bot.all_commands.get(name)
            if command is None:
                await destination.send(bot.command_not_found.format(name))
                return

            for key in commands[1:]:
                try:
                    key = _mention_pattern.sub(repl, key)
                    command = command.all_commands.get(key)
                    if command is None:
                        await destination.send(bot.command_not_found.format(key))
                        return
                except AttributeError:
                    await destination.send(bot.command_has_no_subcommands.format(command, key))
                    return

            pages = await bot.formatter.format_help_for(ctx, command)

        if bot.dm_help is None:
            characters = sum(map(len, pages))
            # modify destination based on length of pages.
            if characters > 1000:
                destination = ctx.message.author


        myEmbed = discord.Embed(title="sawickipedia.exe Help", description=str(pages[pageNum]))
        myEmbed.set_footer(text="Page " + str(pageNum+1) + "/" + str(len(pages)))

        await ctx.send(embed=myEmbed)
        """

    @commands.command(name = "convert-to-owo", aliases = ["OWO", "OwO", "converttoowo", "convert-to-OwO", "converttoOwO", "owo"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def convertToOwo(self, ctx, *, toConvert : str):
        """A disgusting command. I don't even know why this needs to exist."""
        newStr = ''
        for letter in toConvert:
            if letter == 'a':
                newStr = newStr + 'awa'
            elif letter == 'e':
                newStr = newStr + 'ewe'
            elif letter == 'i':
                newStr = newStr + 'iwi'
            elif letter == 'o':
                newStr = newStr + 'owo'
            elif letter == 'u':
                newStr = newStr + 'uwu'
            elif letter == 'A':
                newStr = newStr + 'AWA'
            elif letter == 'E':
                newStr = newStr + 'EWE'
            elif letter == 'I':
                newStr = newStr + 'IWI'
            elif letter == 'O':
                newStr = newStr + 'OWO'
            elif letter == 'U':
                newStr = newStr + 'UWU'
            else:
                newStr = newStr + letter
        embed = discord.Embed(title=str(ctx.author) + "'s Horrible Translation", description = newStr, color=0xDC143C)
        await ctx.send(embed = embed)
    
    

        

def setup(bot):
    bot.add_cog(Misc(bot))