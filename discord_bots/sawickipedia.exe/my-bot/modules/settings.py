#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os  
import pickle


class Settings():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['set-prefix', 'prefix'])
	@commands.cooldown(1, 1, commands.BucketType.user)
    async def setprefix(self, ctx, prefix: str):
        '''Sets the prefix for the bot.'''
        pickle.dump(prefix, open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'prefix.p', 'wb'))
        await ctx.send('Prefix set!')


def setup(bot):
    bot.add_cog(Settings(bot))
