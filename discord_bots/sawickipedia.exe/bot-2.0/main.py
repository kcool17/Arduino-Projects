#!/usr/bin/env python

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


#Prefix
def get_prefix(bot, message):
    '''A callable Prefix for our bot. This could be edited to allow per server prefixes.'''
    try:
        prefix = '?'
    except:
        prefix = '?'
    if (not message.guild):  #Check to see if we are outside of a guild. e.g DM's etc.
        return '?' #Only allow ? to be used in DMs
    return commands.when_mentioned_or(prefix)(bot, message)

description = 'A bot that can do things.'
startup_extensions = ["modules.transfer"
                      
                      
                    ]
bot = commands.Bot(command_prefix=get_prefix, description=description)

#Logging
logging.basicConfig(format='%(asctime)s -%(levelname)s- %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

async def background_task(): #Runs every 1 second, constantly.
    await bot.wait_until_ready()
    while (not bot.is_closed()):
        #Logging
        
        gc.collect()
        await asyncio.sleep(1)
            
async def slow_background_task(): #Runs every 30 seconds, constantly.
    await bot.wait_until_ready()
    while (not bot.is_closed()):
        
        
        await asyncio.sleep(30)
    
    
#Events:
@bot.event  
async def on_ready():
    startup_extensions = []
    logging.info('**______----------------------------STARTING----------------------------______**\n'
                +'Logged in as\n'
                +bot.user.name + "\n"
                +str(bot.user.id) + "\n"
                +"**Date:** " + str(datetime.datetime.now()) + "\n"
                +'------')
    await bot.change_presence(activity=discord.Game(name='with Startup Caches'))


@bot.event
async def on_message(message):
     
    #Send all DMs to owner
    if isinstance(message.channel, discord.abc.PrivateChannel)and (message.author.id != 357953549738573835):
        to_channel = await bot.fetch_user(357953549738573835)
        await to_channel.send((((('**Message from ' + str(message.author)) + '[*') + str(message.author.id)) + '*]:** ') +str(message.content))
        print(message.attachments)
        if message.attachments != []:
            to_say = "**Attachments**: "
            for thing in message.attachments:
                to_say = to_say + thing.url + "\n"
            await to_channel.send(to_say)
    





  
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.loop.create_task(background_task())
    bot.loop.create_task(slow_background_task())
    bot.run("NTExNjQ5NDA4MTE1NDA4OTM4.XNHeuA.WgX2N2QmKZ82Z15LcLgnVvUU_DI")