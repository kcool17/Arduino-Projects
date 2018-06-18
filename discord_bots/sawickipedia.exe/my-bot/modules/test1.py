#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands



class Test1():
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def cool(self, ctx):
        'Says if a user is cool.\n        In reality this just checks if a subcommand is being invoked.\n        '
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

    @cool.command(name='bot')
    async def _bot(self, ctx):
        'Is the bot cool?'
        await ctx.send('Yes, the bot is cool.')


def setup(bot):
    bot.add_cog(Test1(bot))
