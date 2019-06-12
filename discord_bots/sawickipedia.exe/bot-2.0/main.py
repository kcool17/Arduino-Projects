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
                      "modules.economy",
                      "modules.minigames",
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
            
            
        #Moderation:
        for guild in bot.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.name == "Muted":
                        with open("serverdata" + os.sep + str(guild.id) + ".json") as guild_file:
                            guild_data = json.load(guild_file)
                        
                        try:
                            mute_data = guild_data['user_data'][str(member.id)]['mute_data']
                        except:
                            mute_data = {"time":"forever"}
                        
                        if mute_data['time'] == 'forever':
                            pass
                        elif int(mute_data['time']) <= 0:
                            mute_data = {}
                            for role in guild.roles:
                                if role.name == "Muted":
                                    mute_role = role
                            await member.remove_roles(mute_role)
                            await member.edit(speak = True)
                            try:
                                mute_old_channel = guild_data['user_data'][str(member.id)]['mute_old_channel']
                                for channel in guild.text_channels:
                                    mute_old_perm_obj = channel.overwrites_for(member)
                                    mute_old_perm_obj.send_messages = mute_old_channel[str(channel.id)][0]
                                    mute_old_perm_obj.add_reactions = mute_old_channel[str(channel.id)][1]
                                    await channel.set_permissions(member, overwrite=mute_old_perm_obj)
                                    if channel.overwrites_for(member).is_empty():
                                        await channel.set_permissions(member, overwrite=None)
                                        
                                for channel in ctx.guild.voice_channels:
                                    mute_old_perm_obj = channel.overwrites_for(member)
                                    mute_old_perm_obj.speak = mute_old_channel[str(channel.id)]
                                    await channel.set_permissions(member, overwrite=mute_old_perm_obj)
                                    if channel.overwrites_for(member).is_empty():
                                        await channel.set_permissions(member, overwrite=None)
                            except:
                                pass
                        else:
                            mute_data['time'] = str(int(mute_data['time']) - 1)
                        
                        guild_data['user_data'][str(member.id)]['mute_data'] = mute_data
                        with open("serverdata" + os.sep + str(guild.id) + ".json", "w") as guild_file:
                            json.dump(guild_data, guild_file, indent=4)
        
        #Other:
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
                role_list.append(member.guild.get_role(role))
            except Exception as e:
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
            
    
    
        
    #Continues Blackjack game:
    if message.content.lower() == "hit" or message.content.lower() == "h" or message.content.lower() == "stand" or message.content.lower() == "s" or message.content.lower() == "double" or message.content.lower() == "d":
        with open('serverdata' + os.sep + str(message.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        try:
            if guild_data['user_data'][str(message.author.id)]['playing_bj']: 
                bj_data = guild_data['user_data'][str(message.author.id)]['bj_data']
                if message.content.lower() == "double" or message.content.lower() == "d":
                    bj_data['done'] = True
                    guild_data['user_data'][str(message.author.id)]['money'] -= bj_data['bet']
                    bj_data['bet'] *= 2
                if message.content.lower() == "stand" or message.content.lower() == "s":
                    #stand
                    bj_data['done'] = True
                else:
                    #hit/double
                    bj_data['player_cards'].append(bj_data['deck'].pop())
                    
                #Totals up the cards 
                ace_found = False
                bj_data['player_total'] = 0
                result = -1 #-1 is not done, 0 is lose, 1 is tie, 2 is win
                for card in bj_data['player_cards']:
                    try:
                        bj_data['player_total'] += int(card)
                    except:
                        if card == 'A':
                            if ace_found:
                                bj_data['player_total'] += 1
                            else:
                                ace_found = True
                                bj_data['player_total'] += 11
                                bj_data['soft_ace'] = True
                        else:
                            bj_data['player_total'] += 10
                        
                    if bj_data['player_total'] > 21 and bj_data['soft_ace']:
                        bj_data['player_total'] -= 10
                        bj_data['soft_ace'] = False
                    elif bj_data['player_total'] > 21:
                        bj_data['done'] = True
                        result = 0
                    elif bj_data['player_total'] == 21:
                        bj_data['done'] = True
                
                
                soft_deal = False
                if bj_data['done']:
                    guild_data['user_data'][str(message.author.id)]['playing_bj'] = False
                    #Add dealer cards, and deal more to them
                    ace_found = False
                    bj_data['dealer_total'] = 0
                    x = 0
                    while x < len(bj_data['dealer_cards']):
                        card = bj_data['dealer_cards'][x]
                        try:
                            bj_data['dealer_total'] += int(card)
                        except:
                            if card == 'A':
                                if ace_found:
                                    bj_data['dealer_total'] += 1
                                else:
                                    ace_found = True
                                    bj_data['dealer_total'] += 11
                                    soft_deal = True
                            else:
                                bj_data['dealer_total'] += 10
                            
                        if bj_data['dealer_total'] > 21 and soft_deal:
                            bj_data['dealer_total'] -= 10
                            soft_deal = False
                        elif bj_data['dealer_total'] > 21:
                            result = 2
                        print(x)
                        print(bj_data['dealer_cards'])
                        print(bj_data['dealer_total'])
                        x += 1
                        if (x > 1):
                            if bj_data['dealer_total'] < 17 and result == -1:
                                card = bj_data['deck'].pop()
                                bj_data['dealer_cards'].append(card)
                            else:
                                break
                        
                        
                    
                    #Get results
                    if result == -1:
                        if bj_data['dealer_total'] > bj_data['player_total']:
                            result = 0
                        elif bj_data['dealer_total'] < bj_data['player_total']:
                            result = 2
                        else:
                            result = 1
                else:
                    bj_data['dealer_total'] = bj_data['dealer_cards'][0]
                
                
                
                #Formats result
                is_done = False
                if not bj_data['done']:
                    bj_embed = discord.Embed(title="Blackjack",description='Use `?bj hit` to draw another card, and `?bj stand` to end your turn.' 
                                     + 'Use `?bj double` to double down (draw one card more, and double your bet). This game is for ${:,}.'.format(bj_data['bet']), color=255)
                else:
                    bj_data['done'] = False
                    is_done = True
                    if result == 0:
                        bj_embed = discord.Embed(title="Blackjack", description='Player Loses $' + '{:,}'.format(int(bj_data['bet'])),color=16711680)
                    elif result == 1:
                        bj_embed = discord.Embed(title="Blackjack", description='Push, money back', color=16744448)
                        guild_data['user_data'][str(message.author.id)]['money'] += bj_data['bet']
                    else:
                        bj_embed = discord.Embed(title="Blackjack", description='Player Wins ${:,}'.format(int(bj_data['bet'])), color=65280)
                        guild_data['user_data'][str(message.author.id)]['money'] += int(bj_data['bet']) * 2
                        
                        
                        
                        
                #Saves data:
                guild_data['user_data'][str(message.author.id)]['bj_data'] = bj_data
                with open('serverdata' + os.sep + str(message.guild.id) + ".json", "w") as guild_file:
                    json.dump(guild_data, guild_file, indent=4)
                
                #Displays data
                player_card_str = ''
                dealer_card_str = ''
                for card in bj_data['player_cards']:
                    player_card_str = player_card_str + '|{}| '.format(str(card))
                dealer_card_string = ''
                if is_done:
                    for card in bj_data['dealer_cards']:
                        dealer_card_str = dealer_card_str + '|{}| '.format(str(card))
                else:
                    dealer_card_str = '|{}| |?|'.format(bj_data['dealer_cards'][0])
                
                if soft_deal:
                    dealer_total_str = "Soft " + str(bj_data['dealer_total'])
                elif int(bj_data['dealer_total']) > 21:
                    dealer_total_str = "Bust " + str(bj_data['dealer_total'])
                else:
                    dealer_total_str = str(bj_data['dealer_total'])
                
                if bj_data['soft_ace']:
                    player_total_str = "Soft " + str(bj_data['player_total'])
                elif int(bj_data['player_total']) > 21:
                    player_total_str = "Bust " + str(bj_data['player_total'])
                else:
                    player_total_str = str(bj_data['player_total'])
                    
                bj_embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
                bj_embed.add_field(name="Player's Hand ({})".format(player_total_str), value=player_card_str, inline=True)
                bj_embed.add_field(name="Dealer's Hand ({})".format(dealer_total_str), value=dealer_card_str, inline=True)
                await message.channel.send(embed=bj_embed)
        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            await message.channel.send("```css\n[{} | Line: {}]\n```".format(e, line))


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