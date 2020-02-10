#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os
import json
import asyncio
import datetime



class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def check_dev(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return str(ctx.author.id) in devs
    
    def check_owner(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return ctx.author == ctx.guild.owner or str(ctx.author.id) in devs
    
    def check_admin(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return ctx.author.guild_permissions.administrator or str(ctx.author.id) in devs
    
    @asyncio.coroutine
    async def get_users(self, ctx, user):
        try:
            if user[0] == "<":
                if user[0:3] == "<@!":
                    member = ctx.guild.get_member(int(user[3:len(user)-1]))
                else:
                    member = ctx.guild.get_member(int(user[2:len(user)-1]))
                if member is not None:
                    return member
        except:
            pass #Too short of a string given
        
        user_list = []
        user_ID_list = []
        user_nick_list = []
        #Creates lists
        for person in ctx.guild.members:
            user_list.append(person)
            user_ID_list.append(person.id)
            try:
                if len(person.display_name) > 0:
                    user_nick_list.append(person.display_name)
                else:
                    user_nick_list.append(person)
            except:
                user_nick_list.append(person)
        find_list = []
        find_ID_list = []
        pos = 0
        #Finds user
        for thing in user_list:
            if str(thing).lower().startswith(user.lower()):
                find_list.append(str(thing))  
                find_ID_list.append(user_ID_list[pos])
            pos += 1
        pos = 0
        for thing in user_nick_list:
            if str(thing).lower().startswith(user.lower()) and (str(user_list[pos]) not in find_list):
                find_list.append(str(user_list[pos]))
                find_ID_list.append(user_ID_list[pos])
            pos += 1
            
        the_ID = 0
        if len(find_ID_list) == 1:
            the_ID = int(find_ID_list[0])
        elif len(find_ID_list) == 0:
            await ctx.send("No users found. Please try again.")
        else:
            await ctx.send('Multiple people found. Pick someone specific next time.') 
            user_find_embed = discord.Embed(title='Users Found:', color=16742144)
            num = 0
            for human in find_list:
                user_find_embed.add_field(name=('#' + str(num + 1)) + ':', value=human, inline=True)
                num += 1
            await ctx.send(embed=user_find_embed)
        return ctx.guild.get_member(the_ID)
    
    
    
    @commands.command()
    @commands.check(check_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setcustomjoin(self, ctx, user, nickname, *roles):
        """Owner-only. Allows customized roles and nicknames to be given to a user who previously left and rejoined. The bot must have a higher role than the highest role it will give. Note: Please only use the name of the role, with out the `@`. Also, use quotes if a nickname/role has multiple words."""
        member = await self.get_users(ctx, user)
        if member == None:
            return
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            custom_join = []
            custom_join.append(nickname)
            for role in roles:
                role_exists = False
                for guildrole in ctx.guild.roles:
                    if role == guildrole.name:
                        custom_join.append(guildrole.id)
                        role_exists = True
                if not role_exists:
                    await ctx.send("Invalid role! Please try again!")
                    return
            guild_data['user_data'][str(member.id)]['custom_join'] = custom_join
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                json.dump(guild_data, guild_file, indent=4)
        except:
            await ctx.send("An error occurred! Please try again, and use the right parameters!")
            return
        await ctx.send("Done!")
    
    
    @commands.command(aliases=['getcustomjoins', 'getcustomjoin', 'viewcustomjoins'])
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewcustomjoin(self, ctx, *, user : str = 'list'):
        """Admin-only. Views the customized join for the given user. If no user input, or the input is "list", it returns a list of all users with customized joins."""
        if user == 'list':
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
                guild_data = json.load(guild_file)
                
            custom_join_users = []
            for user, data in guild_data['user_data'].items():
                try:
                    if data['custom_join'] != []:
                        custom_join_users.append(int(user))
                except KeyError:
                    pass #No custom join exists
            
            custom_join_str = ""
            for item in custom_join_users:
                custom_join_str = custom_join_str + "<@!{}>\n".format(item)
            
            my_embed=discord.Embed(title="Custom Joins:", description=custom_join_str)
            my_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            await ctx.send(embed=my_embed)
            
            return
        
        
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            custom_join = guild_data['user_data'][str(member.id)]['custom_join']
        except:
            custom_join = []
        
        if custom_join == []:
            await ctx.send("No Custom Join found!")
            return
        
        fmt = "**Nickname:** " + custom_join[0] + "\n**Roles:**\n"
        for role in custom_join[1:]:
            fmt = fmt + "<@&" + str(role) + ">\n"
        my_embed=discord.Embed(title="Custom Join Settings:", description=fmt)
        my_embed.set_author(name= str(member), icon_url= member.avatar_url)
        await ctx.send(embed=my_embed)
    
    
    @commands.command()
    @commands.check(check_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deletecustomjoin(self, ctx, *, user : str):
        """Owner-only. Deletes the customized join for the given user."""
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        guild_data["user_data"][str(member.id)]["custom_join"] = []
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
                
        await ctx.send("Removed Custom Join for: " + str(member))
    
    
    @commands.command(aliases=['getcustomjoinsid', 'getcustomjoinid', 'viewcustomjoinsid'])
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewcustomjoinid(self, ctx, *, user : str):
        '''Admin-only. View the customized join for the given user ID.'''
        member = int(user)
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            custom_join = guild_data['user_data'][str(member)]['custom_join']
        except:
            custom_join = []
            
        if custom_join == []:
            await ctx.send("User ID not found, or Custom Join does not exist! Try again!")
            return
        
        fmt = "**Nickname:** " + custom_join[0] + "\n**Roles:**\n"
        for role in custom_join[1:]:
            fmt = fmt + "<@&" + str(role) + ">\n"
        my_embed=discord.Embed(title="Custom Join Settings:", description=fmt)
        my_embed.set_author(name= user)
        await ctx.send(embed=my_embed)
        
    @commands.command()
    @commands.check(check_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deletecustomjoinid(self, ctx, *, user : str):
        """Owner-only. Deletes the customized join for the given user ID."""
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            custom_join = guild_data['user_data'][user]['custom_join']
        except:
            custom_join = []
            
        if custom_join == []:
            await ctx.send("User ID not found, or Custom Join does not exist! Try again!")
            return
        
        guild_data['user_data'][user]['custom_join'] = []
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
            
        await ctx.send("Removed Custom Join for: " + user)
    

    @commands.command()
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mute(self, ctx, user : str, time_str = "forever", *, reason = "None"):
        """Admin-only. Mutes a person. Use the syntax ?mute @user time reason. @user is the person to mute, time is how long you want to do it, and the reason for muting.
        To mute someone for a specific amount of time, use the format hours:minutes:seconds. If you want it to be permanent, say "forever"."""
        
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            mute_data = guild_data['user_data'][str(member.id)]['mute_data']
        except:
            mute_data = {}
    
        
        #User already muted
        if mute_data != {}:
            if mute_data["reason"] == "None":
                the_reason = ""
            else:
                the_reason = "Reason: " + mute_dat["reason"]
            if mute_data["time"] == "forever":
                the_time = "∞"
            else:
                the_time = str(datetime.timedelta(seconds=int(mute_data["time"])))
                
            mute_embed = discord.Embed(title = member.name, description = the_reason, color = 0xFF0000)
            mute_embed.add_field(name = "Mute Time Remaining:", value = the_time)
            mute_embed.set_footer(text = "Person who Muted: " + str(ctx.guild.get_member(muteDat["muter"])))
            if time_str != "forever" or mute_data["time"] == "forever":
                await ctx.send("User already muted! If you want to mute them forever, please use `?mute @user forever`! Here is the previous mute information:", embed = mute_embed)
            else:
                await ctx.send("User already muted! Here is the previous mute information:", embed = mute_embed)
            return
        
        #Makes sure time is entered correctly:
        try:
            if time_str == "forever":
                new_time = "forever"
            else:
                temp_time = time_str.split(":")
                new_time = str(int(temp_time[0]) *3600 + int(temp_time[1]) *60 + int(temp_time[2]))
        except:
            await ctx.send("Time entered incorrectly! Please use the format `hours:minutes:seconds`!")
            return
        
        async with ctx.channel.typing():
            #Create muted role and sets it up
            role_found = False
            for role in ctx.guild.roles:
                if role.name == "Muted":
                    role_found = True
                    
            if not role_found:
                await ctx.guild.create_role(name="Muted")
            
            mute_role = None
            for role in ctx.guild.roles:
                if role.name == "Muted":
                    mute_role = role
                    
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages = False, add_reactions = False)
            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(mute_role, speak = False)
                
                
            #Ensures previous channel permissions don't get messed up after unmuting, and mutes the user
            mute_old_channel = {}
            for channel in ctx.guild.text_channels:
                mute_old_perm_obj = channel.overwrites_for(member)
                mute_old_perm = [mute_old_perm_obj.send_messages, mute_old_perm_obj.add_reactions]
                mute_old_channel[str(channel.id)] = mute_old_perm
                mute_old_perm_obj.send_messages = False
                mute_old_perm_obj.add_reactions = False
                await channel.set_permissions(member, overwrite=mute_old_perm_obj)
            for channel in ctx.guild.voice_channels:
                mute_old_perm_obj = channel.overwrites_for(member)
                mute_old_channel[str(channel.id)] = mute_old_perm_obj.speak
                mute_old_perm_obj.speak = False
                await channel.set_permissions(member, overwrite=mute_old_perm_obj)
            guild_data['user_data'][str(member.id)]['mute_old_channel'] = mute_old_channel   
                   
            mute_data = {"muter": ctx.author.id, "time" : new_time, "reason" : reason}  
            await member.edit(speak = False)
            await member.add_roles(mute_role)
            guild_data['user_data'][str(member.id)]['mute_data'] = mute_data
            
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                json.dump(guild_data, guild_file, indent=4)
                
                
            mute_embed = discord.Embed(description = member.mention +  " **has been muted!**", color = 0x0000FF)
            await ctx.send(embed=mute_embed)
        
    @commands.command(aliases = ['viewmutes'])
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewmute(self, ctx, user : str = "list"):
        """Admin-only. Views the mute status of a person. You can also use "?viewmute list" to see all mutes."""
        
        if user == 'list':
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
                guild_data = json.load(guild_file)
                
            mute_users = []
            for user, data in guild_data['user_data'].items():
                try:
                    if data['mute_data'] != {}:
                        mute_users.append(int(user))
                except KeyError:
                    pass #No mute exists
            
            mute_str = ""
            for item in mute_users:
                mute_str = mute_str + "<@!{}>\n".format(item)
            
            my_embed=discord.Embed(title="Mutes:", description=mute_str)
            my_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            await ctx.send(embed=my_embed)
            
            return
        
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            mute_data = guild_data['user_data'][str(member.id)]['mute_data']
        except:
            mute_data = {}
        
        
        if mute_data != {}:
            if mute_data["reason"] == "None":
                the_reason = ""
            else:
                the_reason = "Reason: " + mute_data["reason"]
            if mute_data["time"] == "forever":
                the_time = "∞"
            else:
                the_time = str(datetime.timedelta(seconds=int(mute_data["time"])))
                
            mute_embed = discord.Embed(title = member.name, description = the_reason, color = 0xFF0000)
            mute_embed.add_field(name = "Mute Time Remaining:", value = the_time)
            mute_embed.set_footer(text = "Person who Muted: " + str(ctx.guild.get_member(mute_data["muter"])))
            await ctx.send(embed=mute_embed)
        else:
            await ctx.send("User not muted!")
        
        
        
    @commands.command()
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unmute(self, ctx, user : str):
        """Admin-only. Unmutes a user"""
        
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            mute_data = guild_data['user_data'][str(member.id)]['mute_data']
        except:
            mute_data = {}
        
        if mute_data == {}:
            await ctx.send("User not muted!")
        else:
            async with ctx.channel.typing():
                mute_data = {}
                for role in ctx.guild.roles:
                    if role.name == "Muted":
                        mute_role = role
                await member.remove_roles(mute_role)
                await member.edit(speak = True)
                try:
                    mute_old_channel = guild_data['user_data'][str(member.id)]['mute_old_channel']
                    for channel in ctx.guild.text_channels:
                        mute_old_perm_obj = channel.overwrites_for(member)
                        mute_old_perm_obj.send_messages = mute_old_channel[str(channel.id)][0]
                        mute_old_perm_obj.add_reactions = mute_old_channel[str(channel.id)][1]
                        await channel.set_permissions(member, overwrite=mute_old_perm_obj)
                        if channel.overwrites_for(member).is_empty():
                            await channel.set_permissions(member, overwrite=None)
                            
                    for channel in ctx.guild.voice_channels:
                        mute_old_perm_obj = channel.overwrites_for(member)
                        mute_old_perm_obj.speak = mute_old_channel[str(channel.id)]
                        await channel.set_permissions(member, overwrite=mute_old_perm_obj)
                        if channel.overwrites_for(member).is_empty():
                            await channel.set_permissions(member, overwrite=None)
                except:
                    pass
                guild_data['user_data'][str(member.id)]['mute_data'] = mute_data
            
                with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                    json.dump(guild_data, guild_file, indent=4)
                    
                mute_embed = discord.Embed(description = member.mention + " **has been unmuted!**", color = 0x0000FF)
                await ctx.send(embed = mute_embed)
                
                
    @commands.command()
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def purge(self, ctx, amount : int, *, user = ""):
        """Admin-only. Purges a certain number of messages from the channel you're in (Max 100 at a time). Can also be use to purge from a specific person. Syntax is ?purge amount @user."""
        await ctx.message.delete()
        if amount > 100:
            await ctx.send(content = "Too many messages! Please only delete 100 at a time!", delete_after = 4)
            return
        elif amount < 1:
            await ctx.send(content = "Please input a valid number of messages to delete. 0 and negative numbers do not work.", delete_after = 3)
            return
        
        async with ctx.channel.typing():
            if user == "" or user == None:
                await ctx.channel.purge(limit=amount)
                purge_embed = discord.Embed(description = "**Deleted " + str(amount) + " message(s)!**", color = 0x0000FF)
                purge_embed.set_footer(text = "Purged by: " + str(ctx.author))
                await ctx.send(embed=purge_embed, delete_after = 4)
            else:
                member = await self.get_users(ctx, user)
                if member == None:
                    return
                messages = []
                async for message in ctx.channel.history(limit=amount):
                    if message.author == member:
                        messages.append(message)
                        
                purge_embed = discord.Embed(description = "**Deleted " + str(len(messages)) + " message(s) from user <@!" + str(member.id) + ">, out of the past " + str(amount) + " message(s)!**", color = 0x0000FF)
                purge_embed.set_footer(text = "Purged by: " + str(ctx.author))
                await ctx.send(embed=purge_embed, delete_after = 4)

def setup(bot):
    bot.add_cog(Moderation(bot))