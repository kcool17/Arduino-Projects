#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import json
import os
import asyncio


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def check_dev(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return str(ctx.author.id) in devs
    
    def check_admin(ctx):
        return ctx.author.guild_permissions.administrator or check_dev(ctx)
        
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
    
    
    @commands.command(aliases=['add-moderator', 'add-mod', 'addmod'])
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def addmoderator(self, ctx, *, user : str):
        '''Makes a user a bot moderator'''
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            is_mod = guild_data["user_data"][str(member.id)]["moderator"]
        except:
            guild_data["user_data"][str(member.id)]["moderator"] = False
            is_mod = False
        
        if is_mod:
            await ctx.send("{} already a moderator!".format(member.name))
            return
        else:
            guild_data["user_data"][str(member.id)]["moderator"] = True
            
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
        
        await ctx.send("Made {} a moderator!".format(member.name))
        
    @commands.command(aliases=['remove-moderator', 'remove-mod', 'removemod'])
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def removemoderator(self, ctx, *, user : str):
        '''Makes a user no longer a bot moderator'''
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        
        try:
            is_mod = guild_data["user_data"][str(member.id)]["moderator"]
        except:
            guild_data["user_data"][str(member.id)]["moderator"] = False
            is_mod = False
        
        if not is_mod:
            await ctx.send("{} not a moderator!".format(member.name))
            return
        else:
            guild_data["user_data"][str(member.id)]["moderator"] = False
            
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
        
        await ctx.send("Made {} no longer a moderator!".format(member.name))
    
    @commands.command(aliases=['get-moderators', 'get-mods', 'getmods'])
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def getmoderators(self, ctx):
        '''Returns a list of bot moderators'''
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        mod_list = []
        for user, data in guild_data["user_data"].items():
            try:
                if data["moderator"]:
                    mod_list.append(ctx.guild.get_member(int(user)))
            except KeyError:
                pass #Not a moderator
        
        mod_str = "Any administrators, along with: \n"
        if mod_list == []:
            mod_str = mod_str + "No one else :("
        for user in mod_list:
            mod_str = mod_str + user.mention + "\n"
        mod_embed = discord.Embed(title="Moderators", description=mod_str, color=0x0000FF)
        mod_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=mod_embed)
        
    
    @commands.command(aliases=['set-prefix', 'prefix'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setprefix(self, ctx, *, prefix : str):
        '''Sets the prefix for the bot.'''
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        guild_data["server_data"]["prefix"] = prefix
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
        await ctx.send('Prefix set!')
    
    
    

def setup(bot):
    bot.add_cog(Settings(bot))