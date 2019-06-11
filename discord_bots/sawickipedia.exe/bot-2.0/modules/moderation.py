#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os



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
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    

def setup(bot):
    bot.add_cog(Moderation(bot))