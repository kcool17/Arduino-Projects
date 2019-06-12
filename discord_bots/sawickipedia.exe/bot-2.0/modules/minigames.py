#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os
import json
import asyncio
import random
import html.parser



class Minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.triv_URL = 'https://opentdb.com/api.php?amount=1'
        self.html_parser = html.parser.HTMLParser()
        
    def check_dev(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return str(ctx.author.id) in devs
    
    @asyncio.coroutine
    async def get_users(self, ctx, user):
        try:
            if user[0] == "<":
                if user[0:3] == "<@!":
                    member = ctx.guild.get_member(int(user[3:len(user)-1]))
                else:
                    member = ctx.guild.get_member(int(user[2:len(user)-1]))
                if member is not None:
                    return member
        except:
            pass #Too short of a string given
        
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
    
    
    @commands.command(aliases=['bj'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def blackjack(self, ctx, bet = "current"):
        '''Blackjack! Use "?blackjack about" for details.'''
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        
        try:
            bj_data = guild_data['user_data'][str(ctx.author.id)]['bj_data']
        except:
            bj_data = {}
        try:
            current_money = guild_data['user_data'][str(ctx.author.id)]['money']
        except:
            current_money = 0
                
        if bet == "about": 
            bj_embed = discord.Embed(title='Blackjack Rules', color=255)
            bj_embed.add_field(name='This is Blackjack! Try and beat the dealer!',value='Use the format `?blackjack bet` for your first bet.',inline=False)
            bj_embed.add_field(name='Say "hit" to draw another card, and "stand" to end your turn.',value='Also, say "double" to draw one more card and double your bet.',inline=False)
            bj_embed.add_field(name="Don't go over 21, or you'll bust and lose!", value='Try and beat the dealer!', inline=False)
            await ctx.send(embed=bj_embed)
            return
        
        elif bet == "current": #Displays current blackjack game
            try:
                if not guild_data['user_data'][str(ctx.author.id)]['playing_bj']:
                    await ctx.send("No game currently in progess! Please start a game with `?blackjack bet`")
                    return
            except:
                await ctx.send("No game currently in progess! Please start a game with `?blackjack bet`")
                return
            bj_embed = discord.Embed(title="Blackjack",description='Say "hit" to draw another card, and "stand" to end your turn.' 
                                     + 'Say "double" to double down (draw one card more, and double your bet). This game is for ${:,}.'.format(bj_data['bet']), color=255)

        else: #Creates a new blackjack game, if one isn't in progress
            #Checks
            try:
                bet = int(bet)
            except:
                await ctx.send('Please use the format `?bj bet`.') 
                return
            if bet <= 0:
                await ctx.send("Bet a positive amount, please.")
                return
            if bet > current_money:
                await ctx.send("You don't even have that much on hand, you poor peasant. Try again when you have money.")
                return
            
            in_progress = False
            try:
                if guild_data['user_data'][str(ctx.author.id)]['playing_bj']:
                    await ctx.send("A game of Blackjack is already in progress! Please finish that one first! If you forget what the game looked like, here it is:")
                    in_progress = True
                else:
                    guild_data['user_data'][str(ctx.author.id)]['playing_bj'] = True
            except:
                guild_data['user_data'][str(ctx.author.id)]['playing_bj'] = True
            
            if not in_progress:
                #Actual game
                current_money -=  bet
                
                bj_data['bet'] = bet
                bj_data['done'] = False
                bj_data['soft_ace'] = False
                
                deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
                random.shuffle(deck)
                
                bj_data['player_cards'] = []
                bj_data['dealer_cards'] = []
                bj_data['player_cards'].append(deck.pop())
                bj_data['player_cards'].append(deck.pop())
                bj_data['dealer_cards'].append(deck.pop())
                bj_data['dealer_cards'].append(deck.pop())
                bj_data['deck'] = deck
                
                bj_data['player_total'] = 0
                try:
                    bj_data['dealer_total'] = int(bj_data['dealer_cards'][0])
                except:
                    if bj_data['dealer_cards'][0] == 'A':
                        bj_data['dealer_total'] = 11
                    else:
                        bj_data['dealer_total'] = 10
                ace_found = False
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
                        
                
                if 'A' in bj_data['player_cards'] and ('10' in bj_data['player_cards'] or 'J' in bj_data['player_cards'] or 'Q' in bj_data['player_cards'] or 'K' in bj_data['player_cards']):
                    bj_data['player_total'] = "Blackjack"    
                if 'A' in bj_data['dealer_cards'] and ('10' in bj_data['dealer_cards'] or 'J' in bj_data['dealer_cards'] or 'Q' in bj_data['dealer_cards'] or 'K' in bj_data['dealer_cards']):
                    bj_data['dealer_total'] = "Blackjack"
                
                if bj_data['player_total'] == "Blackjack":
                    if bj_data['dealer_total'] == "Blackjack":
                        #Tie
                        bj_data['done'] = True
                        bj_embed = discord.Embed(title="Blackjack", description='Push, money back', color=16744448)
                        current_money += bet        
                    else:
                        #Win
                        bj_data['done'] = True
                        bj_embed = discord.Embed(title="Blackjack", description='Player Wins ${:,}'.format(int(1.5 * bet)), color=65280)
                        current_money += (bet + int(bet*1.5))
                        
                elif bj_data['dealer_total'] == "Blackjack":
                    #Loss
                    bj_data['done'] = True
                    bj_embed = discord.Embed(title="Blackjack", description='Player Loses $' + '{:,}'.format(int(bet)),color=16711680)
                
                else:
                    bj_embed = discord.Embed(title="Blackjack",description='Use `?bj hit` to draw another card, and `?bj stand` to end your turn.' 
                                         + 'Use `?bj double` to double down (draw one card more, and double your bet). This game is for ${:,}.'.format(bj_data['bet']), color=255)
                
                
    
        if bj_data['done']:
            bj_data['playing_bj'] = False
            
        #Saves blackjack data
        guild_data['user_data'][str(ctx.author.id)]['money'] = current_money
        guild_data['user_data'][str(ctx.author.id)]['bj_data'] = bj_data
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
            
        #Sends the blackjack data
        player_card_str = ''
        dealer_card_str = ''
        for card in bj_data['player_cards']:
            player_card_str = player_card_str + '|{}| '.format(str(card))
        dealer_card_string = ''
        if bj_data['done']:
            for card in bj_data['dealer_cards']:
                dealer_card_str = dealer_card_str + '|{}| '.format(str(card))
        else:
            dealer_card_str = '|{}| |?|'.format(bj_data['dealer_cards'][0])
        
        if bj_data['dealer_total'] == "Blackjack":
            dealer_total_str = "Blackjack"
        elif bj_data['dealer_cards'][0] == 'A':
            dealer_total_str = "Soft 11"
        else:
            try:
                dealer_total_str = str(int(bj_data['dealer_total']))
            except:
                dealer_total_str = "10"
        
        if bj_data['player_total'] == "Blackjack":
            player_total_str = "Blackjack"
        elif bj_data['soft_ace']:
            player_total_str = "Soft " + str(bj_data['player_total'])
        else:
            player_total_str = str(bj_data['player_total'])
            
        bj_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        bj_embed.add_field(name="Player's Hand ({})".format(player_total_str), value=player_card_str, inline=True)
        bj_embed.add_field(name="Dealer's Hand ({})".format(dealer_total_str), value=dealer_card_str, inline=True)
        await ctx.send(embed=bj_embed)
    
    
    
    @commands.command(aliases=['triv'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def trivia(self, ctx, bet = "", *, user: str):
        '''A Trivia Game! Use "?trivia about" for details.'''
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            triv_data = guild_data['user_data'][str(member.id)]['triv_data']
        except:
            triv_data = {}
    
    
    
    
    

def setup(bot):
    bot.add_cog(Minigames(bot))