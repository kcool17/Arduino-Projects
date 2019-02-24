#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
from server import DEVS
import datetime
import pickle
import os

class Moderation(commands.Cog)):
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


    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mute(self, ctx, user : str, timeStr = "forever", *, reason = "None"):
        """Admin-only. Mutes a person. Use the syntax ?mute @user time reason. @user is the person to mute, time is how long you want to do it, and the reason for muting.
        To mute someone for a specific amount of time, use the format hours:minutes:seconds. If you want it to be permanent, say "forever"."""
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
            if self.bot.get_guild(guild).get_member(member) is None:
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
            #Check muted status
            try:
                muteDat = pickle.load(open('servers' + os.sep + str(guild) + os.sep + str(theID) + os.sep + 'muteDat.p', "rb"))
            except:
                muteDat = {}
                
            
            if muteDat != {} and (timeStr != "forever" or muteDat["time"] == "forever"):
                if muteDat["reason"] == "None":
                    theReason = ""
                else:
                    theReason = "Reason: " + muteDat["reason"]
                if muteDat["time"] == "forever":
                    theTime = "∞"
                else:
                    theTime = str(datetime.timedelta(seconds=int(muteDat["time"])))
                    
                await ctx.send("User already muted! If you want to mute them forever, please use `?mute @user forever`! Here is the previous mute information:")
                muteEmbed = discord.Embed(title = ctx.guild.get_member(theID).name, description = theReason, color = 0xFF0000)
                muteEmbed.add_field(name = "Mute Time Remaining:", value = theTime)
                muteEmbed.set_footer(text = "Person who Muted: " + str(ctx.guild.get_member(muteDat["muter"])))
                await ctx.send(embed = muteEmbed)
                return
            
            #Create muted role and set it up
            roleFound = False
            for role in ctx.guild.roles:
                if role.name == "Muted":
                    roleFound = True
                    
            if not roleFound:
                await ctx.guild.create_role(name="Muted")
            
            muteRole = None
            for role in ctx.guild.roles:
                if role.name == "Muted":
                    muteRole = role
                    
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muteRole, send_messages = False, add_reactions = False)
            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(muteRole, speak = False)
            
            
            muteOldChannel = {}
            for channel in ctx.guild.text_channels:
                muteOldPermObj = channel.overwrites_for(ctx.guild.get_member(theID))
                muteOldPerm = [muteOldPermObj.send_messages, muteOldPermObj.add_reactions]
                muteOldChannel[str(channel.id)] = muteOldPerm
                await channel.set_permissions(ctx.guild.get_member(theID), send_messages = False, add_reactions = False)
            for channel in ctx.guild.voice_channels:
                muteOldPermObj = channel.overwrites_for(ctx.guild.get_member(theID))
                muteOldChannel[str(channel.id)] = muteOldPermObj.speak
                await channel.set_permissions(ctx.guild.get_member(theID), speak = False)
            
            pickle.dump(muteOldChannel, open('servers' + os.sep + str(guild) + os.sep + str(theID) + os.sep + 'muteOldChannel.p',"wb"))
                
            #Set up muteDat
            try:
                if timeStr == "forever":
                    newTime = "forever"
                else:
                    tempTime = timeStr.split(":")
                    newTime = str(int(tempTime[0]) *3600 + int(tempTime[1]) *60 + int(tempTime[2]))
            except:
                await ctx.send("Time entered incorrectly! Please use the format `hours:minutes:seconds`!")
                return
               
            muteDat = {"muter": member, "time" : newTime, "reason" : reason}    
            
            

            #Mute user
            await ctx.guild.get_member(theID).edit(speak = False)
            await ctx.guild.get_member(theID).add_roles(muteRole)
            pickle.dump(muteDat, open('servers' + os.sep + str(guild) + os.sep + str(theID) + os.sep + 'muteDat.p',"wb"))
            muteEmbed = discord.Embed(description = "<@!" + str(theID) + "> **has been muted!**", color = 0x0000FF)
            await ctx.send(embed=muteEmbed)


    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewmute(self, ctx, user : str):
        """Views the mute status of a person"""
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
            if self.bot.get_guild(guild).get_member(member) is None:
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
            #Check muted status
            try:
                muteDat = pickle.load(open('servers' + os.sep + str(guild) + os.sep + str(theID) + os.sep + 'muteDat.p', "rb"))
            except:
                muteDat = {}
                
            if muteDat == {}:
                await ctx.send("User not muted!")
            else:
                if muteDat["reason"] == "None":
                    theReason = ""
                else:
                    theReason = "Reason: " + muteDat["reason"]
                if muteDat["time"] == "forever":
                    theTime = "∞"
                else:
                    theTime = str(datetime.timedelta(seconds=int(muteDat["time"])))
                    
                muteEmbed = discord.Embed(title = ctx.guild.get_member(theID).name, description = theReason, color = 0xFF0000)
                muteEmbed.add_field(name = "Mute Time Remaining:", value = theTime)
                muteEmbed.set_footer(text= "Person who Muted: " + str(ctx.guild.get_member(muteDat["muter"])))
                await ctx.send(embed = muteEmbed)

            
            
            

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unmute(self, ctx, user : str):
        """Unmutes a user"""
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
            if self.bot.get_guild(guild).get_member(member) is None:
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
            #Check muted status
            try:
                muteDat = pickle.load(open('servers' + os.sep + str(guild) + os.sep + str(theID) + os.sep + 'muteDat.p', "rb"))
            except:
                muteDat = {}
                
            if muteDat == {}:
                await ctx.send("User not muted!")
            else:
                muteDat = {}
                for role in ctx.guild.roles:
                    if role.name == "Muted":
                        muteRole = role
                await ctx.guild.get_member(theID).remove_roles(muteRole)
                await ctx.guild.get_member(theID).edit(speak = True)
                try:
                    muteOldChannel = pickle.load(open('servers' + os.sep + str(guild) + os.sep + str(theID) + os.sep + 'muteOldChannel.p',"rb"))
                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(ctx.guild.get_member(theID), send_messages = muteOldChannel[str(channel.id)][0], add_reactions = muteOldChannel[str(channel.id)][1])
                        if channel.overwrites_for(ctx.guild.get_member(theID)).is_empty():
                            await channel.set_permissions(ctx.guild.get_member(theID), overwrite=None)
                            
                    for channel in ctx.guild.voice_channels:
                        await channel.set_permissions(ctx.guild.get_member(theID), speak = muteOldChannel[str(channel.id)])
                        if channel.overwrites_for(ctx.guild.get_member(theID)).is_empty():
                            await channel.set_permissions(ctx.guild.get_member(theID), overwrite=None)
                except:
                    pass
                pickle.dump(muteDat, open('servers' + os.sep + str(guild) + os.sep + str(theID) + os.sep + 'muteDat.p',"wb"))
                muteEmbed = discord.Embed(description = "<@!" + str(theID) + "> **has been unmuted!**", color = 0x0000FF)
                await ctx.send(embed = muteEmbed)
                
     
                
                
                
                
                
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def purge(self, ctx, amount : int, *, user = ""):
        """Admin-only. Purges a certain number of messages from the channel you're in (Max 100 at a time). Can also be use to purge from a specific person. Syntax is ?purge amount @user."""
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        guild = ctx.guild.id
        member = ctx.author.id
        
        if member in ADMINS:
            await ctx.message.delete()
            if amount > 100:
                await ctx.send(content = "Too many messages! Please only delete 100 at a time!", delete_after = 4)
                return
            elif amount < 1:
                await ctx.send(content = "Please input a valid number of messages to delete. 0 and negative numbers do not work.", delete_after = 3)
                return
    
            if user == "" or user == None:
                await ctx.channel.purge(limit=amount)
                purgeEmbed = discord.Embed(description = "**Deleted " + str(amount) + " message(s)!**", color = 0x0000FF)
                purgeEmbed.set_footer(text = "Purged by: " + str(ctx.author))
                await ctx.send(embed=purgeEmbed, delete_after = 4)
            else:
                theID = ""
                arg = user
                try:
                    if arg[2] == '!':
                        member = int(arg[3:len(arg) - 1])
                    else:
                        member = int(arg[2:len(arg) - 1])
                except:
                    member = ''
                theID = member
                if self.bot.get_guild(guild).get_member(member) is None:
                    (findList, findIDList) = self.getUsers(ctx, arg)
                    theID = ''
                    if len(findIDList) == 1:
                        theID = findIDList[0]
                    elif len(findIDList) == 0:
                        await ctx.send('No users found. Type it correctly next time.')
                        return
                    else:
                        await ctx.send('Multiple people found. Pick someone specific next time.')
                        userFindEmbed = discord.Embed(title='Users Found:', color=16742144)
                        aNum = 0
                        for human in findList:
                            userFindEmbed.add_field(name=('#' + str(aNum + 1)) + ':', value=human, inline=True)
                            aNum += 1
                        await ctx.send(embed=userFindEmbed)
                        return
                
                messages = []
                async for message in ctx.channel.history(limit=amount):
                    if message.author.id == theID:
                        messages.append(message)
                await ctx.channel.delete_messages(messages)
                purgeEmbed = discord.Embed(description = "**Deleted " + str(len(messages)) + " message(s) from user <@!" + str(theID) + ">, out of the past " + str(amount) + " message(s)!**", color = 0x0000FF)
                purgeEmbed.set_footer(text = "Purged by: " + str(ctx.author))
                await ctx.send(embed=purgeEmbed, delete_after = 4)
                
    
    
    
    
            
            
            
            
            
            
            
            
            
            
            
               
                
                
                
    

def setup(bot):
    bot.add_cog(Moderation(bot))
