#!/usr/bin/env python
"""
SAWICKIPEDIA.EXE
main.py
@author: Kyle Sawicki
----------------------------------------
Main startup module for the bot
"""
#Imports
import discord  
from discord.ext import commands
import asyncio
import datetime
import io
import sys
import os
import gc
import logging
import random
import json
from json.decoder import JSONDecodeError
import io
import sys

#Constants
DEBUG = True

#Logging
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.INFO)
#  
# log_formatter = logging.Formatter("%(asctime)s -%(levelname)s- %(message)s", datefmt="%d-%b-%y %H:%M:%S")
#  
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setFormatter(log_formatter)
# root_logger.addHandler(console_handler)

#Prefix
def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    try:
        with open('serverdata' + os.sep + str(message.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        prefix = guild_data["server_data"]["prefix"]
    except:
        prefix = "?"
    if (not message.guild):  #Check to see if we are outside of a guild. e.g DM's etc.
        return "?" #Only allow ? to be used in DMs
    return commands.when_mentioned_or(prefix)(bot, message)

#Bot Instantiation
description = "A bot that can do things."
startup_extensions = ["modules.developer",
                      "modules.misc",
                      "modules.moderation",
                      "modules.transfer",
                      "modules.settings"
                    ]
bot = commands.Bot(command_prefix=get_prefix, description=description)


async def background_task(): #Runs every 1 second, constantly.
    await bot.wait_until_ready()
    #Main loop
    while (not bot.is_closed()):
        #Adds data to files for each server:
        for guild in bot.guilds:
            try:
                with open("serverdata" + os.sep + str(guild.id) + ".json") as guild_file:
                    guild_data = json.load(guild_file)
                    for user in guild.members:
                        if str(user.id) not in guild_data["user_data"].keys():
                            guild_data["user_data"][user.id] = {}
                with open("serverdata" + os.sep + str(guild.id) + ".json", "w") as guild_file:
                    json.dump(guild_data, guild_file, indent=4)
            except JSONDecodeError:
                pass
            except FileNotFoundError:
                pass
        #Logging
        global log_buffer
        global err_buffer
        if bot.user.id == 421015092830666754:
            to_channel=bot.get_channel(496780822553034752)
        else:
            to_channel=bot.get_channel(496794388689584146)
        to_send = log_buffer.getvalue()
        to_send2 = err_buffer.getvalue()
        log_buffer.close()
        err_buffer.close()
        sys.stdout = log_buffer = io.StringIO()
        sys.stderr = err_buffer = io.StringIO()
        
        if to_send != "":
            await to_channel.send(to_send)
        if to_send2 != "":
            await to_channel.send(to_send2)
        gc.collect()
        await asyncio.sleep(1)
            
async def slow_background_task(): #Runs every 30 seconds, constantly.
    await bot.wait_until_ready()
    games_file = open("botdata" + os.sep + "games.txt", "r")
    GAMES = games_file.read().split("\n")
    while (not bot.is_closed()):
        
        await asyncio.sleep(30)
        #Change playing status
        await bot.change_presence(activity=discord.Game(name=str(random.choice(GAMES))))
    
    
#Events:
@bot.event  
async def on_ready():
    #Create files for each server
    for guild in bot.guilds:
        try:
            my_file = open("serverdata" + os.sep + str(guild.id) + ".json", "x")
            json.dump({"server_data" : {}, "user_data": {}}, my_file, indent=4)
        except:
            pass #File exists, so no need to do anything
        
    #Main bot startup
    ready_str = ("\n**______----------------------------STARTING----------------------------______**\n"
                "Logged in as\n" +bot.user.name+ "\n"
                +str(bot.user.id)+ "\n"
                "**Date:** " +str(datetime.datetime.now())+ "\n"
                "------")
    print(ready_str)
    await bot.change_presence(activity=discord.Game(name="with Startup Caches"))

@bot.event
async def on_guild_join(guild):
    #Creates file for new guild
    try:
        my_file = open("serverdata" + os.sep + str(guild.id) + ".json", "x")
        json.dump({"server_data" : {}, "user_data": {}}, my_file, indent=4)
    except:
        pass #File exists, so no need to do anything

@bot.event
async def on_member_join(member):
    #Automatically adds roles/nicknames for Custom Join
    with open('serverdata' + os.sep + str(member.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
    
    try:
        custom_join = guild_data['user_data'][str(member.id)]['custom_join']
    except:
        custom_join = []
    
    if custom_join != []:
        role_list = []
        for role in custom_join[1:]:
            try:
                role_list.append(get(guild.roles, id=role))
            except:
                pass
        await member.edit(nick=custom_join[0], roles = role_list)
      
    
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user: #Make sure bot doesn't respond to itself
        return
    #Send all DMs to owner
    if isinstance(message.channel, discord.abc.PrivateChannel)and (message.author.id != 357953549738573835):
        to_channel = bot.get_user(357953549738573835).dm_channel
        if to_channel == None:
            to_channel = await bot.get_user(357953549738573835).create_dm()
        await to_channel.send("**Message from {}[*{}*]:** {}".format(str(message.author), str(message.author.id), str(message.content)))
        if message.attachments != []:
            to_say = "**Attachments**: "
            for thing in message.attachments:
                to_say = to_say + thing.url + "\n"
            await to_channel.send(to_say)


#Main  
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load extension {}\n{}".format(extension, exc))
    sys.stdout = log_buffer = io.StringIO()
    sys.stderr = err_buffer = io.StringIO()
    bot.loop.create_task(background_task())
    bot.loop.create_task(slow_background_task())
    bot.run(open("botdata" + os.sep + "secret.txt").readline())