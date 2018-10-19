#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
from server import DEVS
import pickle
import os

class Moderation():
    def __init__(self, bot):
        self.bot = bot

    def check_dev_owner(ctx):
        global DEVS
        return ctx.author.id in DEVS or ctx.author.id == ctx.guild.owner.id
    
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
    
    
    
    
    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ownertest(self, ctx):
        """Checks if you're a developer, or the server's owner"""
        if ctx.author.id in DEVS:
            await ctx.send("The owner of this place is " + str(ctx.guild.owner) + ". *We'll see how long that lasts.*")
        else:
            await ctx.send("It appears that this is your realm. *For now, at least.*")



    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setcustomjoin(self, ctx, user, nickname, *roles):
        """Allows customized roles and nicknames to be given to a user who previously left and rejoined. The bot must have a higher role than the highest role it will give. Note: Please only use the name of the role, with out the `@`. Also, use quotes if a nickname/role has multiple words."""
        guild = ctx.guild.id
        member = user
        arg = user
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
        
        member = theID
        try:
            customJoin = []
            customJoin.append(nickname)
            for role in roles:
                roleExists = False
                for guildrole in ctx.guild.roles:
                    if role == guildrole.name:
                        customJoin.append(guildrole.id)
                        roleExists = True
                if not roleExists:
                    await ctx.send("Invalid role! Please try again!")
                    return
            pickle.dump(customJoin, open('servers' + os.sep + str(guild) + os.sep + str(member) + os.sep + 'customJoin.p', 'wb'))
        except:
            await ctx.send("An error occurred! Please try again, and use the right parameters!")
            return
        await ctx.send("Done!")

    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewcustomjoin(self, ctx, *, user : str):
        """Views the customized join for the given user."""
        guild = ctx.guild.id
        member = user
        arg = user
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
            
        member = theID
        try:
            customJoin = pickle.load(open('servers' + os.sep + str(guild) + os.sep + str(member) + os.sep + 'customJoin.p', 'rb'))
        except:
            customJoin = []
        
        if customJoin == []:
            await ctx.send("No Custom Join found!")
            return
        
        fmt = "**Nickname:** " + customJoin[0] + "\n**Roles:**\n"
        for role in customJoin[1:]:
            fmt = fmt + "<@&" + str(role) + ">\n"
        myEmbed=discord.Embed(title="Custom Join Settings:", description=fmt)
        myEmbed.set_author(name= str(ctx.guild.get_member(member)), icon_url= ctx.guild.get_member(member).avatar_url)
        await ctx.send(embed=myEmbed)
        
        
    
    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deletecustomjoin(self, ctx, *, user : str):
        """Deletes the customized join for the given user."""
        guild = ctx.guild.id
        member = user
        arg = user
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
        
        member = theID
        pickle.dump([], open('servers' + os.sep + str(guild) + os.sep + str(member) + os.sep + 'customJoin.p', 'wb'))
        await ctx.send("Removed Custom Join for: " + str(ctx.guild.get_member(member)))

    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewcustomjoinid(self, ctx, *, user : str):
        guild = ctx.guild.id
        member = int(user)
        try:
            customJoin = pickle.load(open('servers' + os.sep + str(guild) + os.sep + str(member) + os.sep + 'customJoin.p', 'rb'))
        except:
            await ctx.send("User ID not found, or Custom Join does not exist! Try again!")
            return
        if customJoin == []:
            await ctx.send("No Custom Join found!")
            return
        fmt = "**Nickname:** " + customJoin[0] + "\n**Roles:**\n"
        for role in customJoin[1:]:
            fmt = fmt + "<@&" + str(role) + ">\n"
        myEmbed=discord.Embed(title="Custom Join Settings:", description=fmt)
        myEmbed.set_author(name= user)
        await ctx.send(embed=myEmbed)
        
    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deletecustomjoinid(self, ctx, *, user : str):
        """Deletes the customized join for the given user ID."""
        guild = ctx.guild.id
        member = int(user)
        try:
            customJoin = pickle.load(open('servers' + os.sep + str(guild) + os.sep + str(member) + os.sep + 'customJoin.p', 'rb'))
        except:
            await ctx.send("User ID not found, or Custom Join does not exist! Try again!")
            return
        pickle.dump([], open('servers' + os.sep + str(guild) + os.sep + str(member) + os.sep + 'customJoin.p', 'wb'))
        await ctx.send("Removed Custom Join for: " + user)



def setup(bot):
    bot.add_cog(Moderation(bot))
