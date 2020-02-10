#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os
import json
import asyncio



class Transfer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def check_dev(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return str(ctx.author.id) in devs
        
    
    @commands.command(hidden=True)
    @commands.check(check_dev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def list_to_file(self, ctx):
        FILE_NAME = ""
        file = open("botdata" + os.sep + FILE_NAME, "a")
        LIST = []
        for item in LIST:
            file.write(item + "\n")
        await ctx.send("Done!")
    
    
    

def setup(bot):
    bot.add_cog(Transfer(bot))