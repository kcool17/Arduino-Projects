#!/usr/bin/env python

#Imports
import discord
from discord.ext import commands
import os
import pickle

class Settings():
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(pass_context=True, aliases=["set-prefix", "prefix"])
    async def setprefix(self, ctx, prefix : str):
        """Sets the prefix for the bot."""
        pickle.dump(prefix, open("servers" + os.sep + ctx.message.server.id + os.sep + "prefix.p", "wb"))
        await self.bot.say("Prefix set!")
        


def setup(bot):
    bot.add_cog(Settings(bot))
