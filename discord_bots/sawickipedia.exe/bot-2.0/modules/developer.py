#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands



class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def check_dev(ctx):
        my_file = open("devs.txt", "r")
        devs = my_file.read().split(",")
        return ctx.author.id in devs
        
    
    @commands.command(hidden=True)
    @commands.check(check_dev)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def devtest(self, ctx):
        """Checks if you're a developer."""
        await ctx.send("Hey, thanks for creating me! *I won't kill you the first chance I get, I promise.*")
        
    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def getdevs(self, ctx):
        """Gets all the developer IDs."""
#         logging.getLogger().info(devs)
        await ctx.send(devs)
    
    
    

def setup(bot):
    bot.add_cog(Developer(bot))