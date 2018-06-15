#!/usr/bin/env python

#Imports
import discord
from discord.ext import commands
import os
import pickle
import asyncio
from run import DEVS

class Developer():
    def __init__(self, bot):
        self.bot = bot

    def check_dev(ctx):
        global DEVS
        return ctx.message.author.id in DEVS
    
    @commands.command()
    @commands.check(check_dev)
    async def devtest(self):
        """Checks if you're a developer."""
        await self.bot.say("Hey, thanks for creating me! *I won't kill you the first chance I get, I promise.*")

    @commands.command(pass_context = True, hidden=True)
    @commands.check(check_dev)
    async def botsay(self, ctx, serverid = "display", channelarg = "channel", *arg : str):
        """Repeats what you say."""
        success = False
        newStr = ""
        if ctx.message.channel.is_private:
            if serverid == "display":
                for server in self.bot.servers:
                    await self.bot.say(server.id + " | " +str(server))
            elif channelarg.upper() == "DM":
                for item in arg:
                    newStr = newStr  + str(item) + " "
                newStr = newStr.replace("{", "<")
                newStr = newStr.replace("}", ">")
                human = await self.bot.get_user_info(serverid)
                await self.bot.send_message(human, newStr)
                await self.bot.say("Success!")
            else:
                for server in self.bot.servers:
                    if serverid == server.id:
                        for channel in server.channels:
                            if channelarg == str(channel):
                                for item in arg:
                                    newStr = newStr  + str(item) + " "
                                newStr = newStr.replace("{", "<")
                                newStr = newStr.replace("}", ">")
                                await self.bot.send_message(channel, newStr)
                                success = True
                                await self.bot.say("Success!")
                       

                if not success:
                    await self.bot.say("Failure!")
        
        else:
            if not ctx.message.channel.is_private:
                await self.bot.say('This is in public. Don\'t try that here.')

    @commands.command(hidden=True)
    @commands.check(check_dev)
    async def settoken(self):
        """Sets the bot's token."""
        toToken = ""
        if toToken != "":
            pickle.dump(toToken, open("token.p", "wb"))
        else:
            await bot.say("toToken var empty. Please input a token in source.")



def setup(bot):
    bot.add_cog(Developer(bot))
