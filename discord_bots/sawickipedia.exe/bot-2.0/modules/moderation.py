#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os
import json
import asyncio



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
    
    @asyncio.coroutine
    async def get_users(self, ctx, user):
        if user[0] == "<":
            if user[0:3] == "<@!":
                member = ctx.guild.get_member(int(user[3:len(user)-1]))
            else:
                member = ctx.guild.get_member(int(user[2:len(user)-1]))
            if member is not None:
                return member
        
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
        """Allows customized roles and nicknames to be given to a user who previously left and rejoined. The bot must have a higher role than the highest role it will give. Note: Please only use the name of the role, with out the `@`. Also, use quotes if a nickname/role has multiple words."""
        member = await self.get_users(ctx, user)
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
            guild_data['userdata'][str(member.id)]['custom_join'] = custom_join
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                json.dump(guild_data, guild_file, indent=4)
        except:
            await ctx.send("An error occurred! Please try again, and use the right parameters!")
            return
        await ctx.send("Done!")
    
    
    @commands.command()
    @commands.check(check_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewcustomjoin(self, ctx, *, user : str = 'list'):
        """Views the customized join for the given user. If no user input, or the input is "list", it returns a list of all users with customized joins."""
        if user == 'list':
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
                guild_data = json.load(guild_file)
                
            custom_join_users = []
            for user, data in guild_data['user_data'].items():
                try:
                    if data['custom_join'] != []:
                        custom_join_users.append[int(user)]
                except KeyError:
                    pass #No custom join exists
            
            custom_join_str = ""
            for item in custom_join_users:
                pass # NOT DONE FIX THIS
            
            
            return
        
        
        member = await self.get_users(ctx, user)
        
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
        my_embed.set_author(name= str(ctx.guild.get_member(member)), icon_url= ctx.guild.get_member(member).avatar_url)
        await ctx.send(embed=my_embed)
    
    
    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deletecustomjoin(self, ctx, *, user : str):
        """Deletes the customized join for the given user."""
        member = await self.get_users(ctx, user)
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        guild_data["user_data"][str(member.id)]["custom_join"] = []
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
                
        await ctx.send("Removed Custom Join for: " + str(ctx.guild.get_member(member)))
    
    
    @commands.command()
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def viewcustomjoinid(self, ctx, *, user : str):
        '''View the customized join for the given user ID.'''
        member = int(user)
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            custom_join = guild_data['server_data'][str(member)]['custom_join']
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
    @commands.check(check_dev_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deletecustomjoinid(self, ctx, *, user : str):
        """Deletes the customized join for the given user ID."""
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            custom_join = guild_data['server_data'][str(member)]['custom_join']
        except:
            custom_join = []
            
        if custom_join == []:
            await ctx.send("User ID not found, or Custom Join does not exist! Try again!")
            return
        
        guild_data['server_data'][str(member)]['custom_join'] = []
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
            
        await ctx.send("Removed Custom Join for: " + user)
    

    
    

def setup(bot):
    bot.add_cog(Moderation(bot))