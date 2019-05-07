#!/usr/bin/env python

#Imports
import discord
from discord.ext import commands
import pickle
import os
import random

class Misc():
    def __init__(self, bot):
        self.bot = bot

    def getUsers(self, ctx, arg="noArg"):
        #Creates lists
        userList = []
        userIDList = []
        userNickList = []
        for person in ctx.message.server.members:
            userList.append(person)
            userIDList.append(person.id)
            try:
                if len(person.display_name)>0:
                    userNickList.append(person.display_name)
                else:
                    userNickList.append(person)
            except:
                userNickList.append(person) 


        #Finds user
        findList = []
        findIDList = []
        pos = 0
        for thing in userList:
            if str(thing).lower().startswith(arg.lower()):
                findList.append(str(thing))
                findIDList.append(userIDList[pos])
            pos +=1
                                  
        pos = 0
        for thing in userNickList:
            if str(thing).lower().startswith(arg.lower()) and (str(userList[pos]) not in findList):
                findList.append(str(userList[pos]))
                findIDList.append(userIDList[pos])
            pos+=1

        return findList, findIDList

    @commands.command(description = 'Add two numbers together. Change "num1" and "num2" to the numbers you wish to add together.')
    async def add(self, num1 : int, num2 : int):
        """Adds stuff together."""
        await self.bot.say(num1 + num2)

    @commands.command(description='Use NdN format, with the first N the amount of rolls and the second the amount of sides on the die.')
    async def roll(self, dice : str):
        """Rolls dice."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return
        if rolls>100:
            await self.bot.say("Don't try and overload my CPU. I don't appreciate that.")
        elif limit>1000000:
            await self.bot.say("Do you *really* need to have over a million sides on this die? I mean, come *on*.")
        else:
            total = 0
            result = ""
            if rolls >1:
                for r in range(rolls):
                    myRoll = random.randint(1, limit)
                    if r == 0:
                        result = str(myRoll)
                    else:
                        result = result + ', ' + str(myRoll)
                    total = total + myRoll
                await self.bot.say(result)
                await self.bot.say("The total of your rolls is: " + str(total))
            else:
                await self.bot.say(random.randint(1, limit))

                
    @commands.command(description='Have as many options as you want after "?choose", with a space in between each one. One will be randomly chosen.')
    async def choose(*choices : str):
        """Chooses a random argument you give."""
        await self.bot.say(random.choice(choices))

    @commands.command(pass_context=True)
    async def admintest(self, ctx):
        """Checks if you have admin permissions in this server."""
        ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
        if ctx.message.author.id in ADMINS:
            await self.bot.say("You are an administrator/developer!")
        else:
            await self.bot.say("You are *not* an administrator/developer. How sad.")

    @commands.command(pass_context=True)
    async def mentionuser(self, ctx, *user : str):
        """Mentions the user based on input"""
        #USE THIS IN OTHER FUNCTIONS
        arg = ""
        for item in user:
            arg = arg + item + " "
        arg = arg[:len(arg)-1]
        findList, findIDList = self.getUsers(ctx, arg)
        theID = ""
        if len(findIDList)==1:
            theID = findIDList[0]
        else:
            await self.bot.say("Multiple people found. Pick someone specific next time.")
            userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
            aNum = 0
            for human in findList:
                userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                aNum += 1
            await self.bot.say(embed=userFindEmbed)
            return

        if theID != "":
            #PROGRAM STUFF HERE
            await self.bot.say("<@" + str(theID) + ">")                
                

    @commands.command(pass_context=True)
    async def findid(self, ctx, *user : str):
        """Returns server ID and user ID."""
        server = ctx.message.server.id
        member = ctx.message.author.id
        arg = ""
        for item in user:
            arg = arg + item + " "
        arg = arg[:len(arg)-1]
        theID = ""
        if arg != "":
            try:
                if arg[2] == "!":
                    member = arg[3:(len(arg)-1)]

                else:
                    member= arg[2:(len(arg)-1)]
            except IndexError:
                member= ""

            if self.bot.get_server(server).get_member(member) is None:
                findList, findIDList = self.getUsers(ctx, arg)
                theID = ""
                if len(findIDList)==1:
                    member = findIDList[0]
                else:
                    await self.bot.say("Multiple people found. Pick someone specific next time.")
                    userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
                    aNum = 0
                    for human in findList:
                        userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                        aNum += 1
                    await self.bot.say(embed=userFindEmbed)
                    return
            if self.bot.get_server(server).get_member(member) is None:
                await bot.say("Invalid user, try again.")
            else:
                theID = member
        else:
            theID = ctx.message.author.id
        await self.bot.say("Server: " + str(ctx.message.server.id))
        await self.bot.say("Member: " + str(theID))
        await self.bot.say("Channel: " + str(ctx.message.channel.id))



def setup(bot):
    bot.add_cog(Misc(bot))
