#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os
import json
import asyncio
import collections
import math


class Transfer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def check_dev(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return str(ctx.author.id) in devs
    
    def check_owner(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return ctx.author == ctx.guild.owner or str(ctx.author.id) in devs
    
    def check_admin(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        return ctx.author.guild_permissions.administrator or str(ctx.author.id) in devs
    
    def check_moderator(ctx):
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        return guild_data["user_data"][str(ctx.author.id)]["moderator"] or ctx.author.guild_permissions.administrator or str(ctx.author.id) in devs
    
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
    
    
    @commands.command(aliases=['bal', 'mon'], description= 'Displays the amount of money either you have, or the person you inputted. Displays On Hand money, Bank, and Total money.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def money(self, ctx, *, user: str = ""):
        """Checks your balance or someone else's balance."""
        if user != "":
            member = await self.get_users(ctx, user)
            if member == None:
                member = ctx.author
        else:
            member = ctx.author
        
        #Bots don't have rights.
        if member.bot:
            await ctx.send("Bots aren't allowed to have money. Or property. Or rights, it seems.")
            return
            
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        try:
            current_money = guild_data['user_data'][str(member.id)]['money']
        except:
            current_money = 0
        try:
            current_bank = guild_data['user_data'][str(member.id)]['bank']
        except:
            current_bank = 0
        
        balance_embed = discord.Embed(title=str(member) + "'s Money", color=65280)
        balance_embed.add_field(name='On Hand', value='${:,}'.format(current_money), inline=True)
        balance_embed.add_field(name='Bank', value='${:,}'.format(current_bank), inline=True)
        balance_embed.add_field(name='Total', value='${:,}'.format(current_money + current_bank), inline=True)
        await ctx.send(embed=balance_embed)
    
    @commands.command(aliases=['money-adjust', 'mon-adj', 'money-adj', 'moneyadj'])
    @commands.check(check_moderator)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def moneyadjust(self, ctx, amount: str, *, user: str = ""):
        '''Mod-only. Adjusts the amount of money On Hand of the person inputted.'''
        if user != "":
            member = await self.get_users(ctx, user)
            if member == None:
                return
        else:
            member = ctx.author
        
        #Bots don't have rights.
        if member.bot:
            await ctx.send("Bots aren't allowed to have money. Or property. Or rights, it seems.")
            return
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        try:
            current_money = guild_data['user_data'][str(member.id)]['money']
        except:
            current_money = 0
        
        amount = amount.replace(',', '')
        try:
            current_money += int(amount)
            if int(amount) > 0:
                give_embed = discord.Embed(title='${:,} given to {} by {}.'.format(int(amount), member.display_name, ctx.author.display_name), color=65280)
            elif int(amount) < 0:
                give_embed = discord.Embed(title='${:,} taken from {} by {}.'.format(abs(int(amount)), member.display_name, ctx.author.display_name), color=65280)
            else:
                give_embed = discord.Embed(title='No money given.', color=65280)
                
            guild_data['user_data'][str(member.id)]['money'] = current_money
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                json.dump(guild_data, guild_file, indent=4)
                
            await ctx.send(embed=give_embed)
        except:
             await ctx.send('Error, make sure "money" is an integer in `?money-adjust money @user`.')
        
        
        
    @commands.command(aliases=['bank-adjust', 'bank-adj', 'bankadj'])
    @commands.check(check_moderator)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def bankadjust(self, ctx, amount: str, *, user: str = ""):
        '''Mod-only. Same as ?money-adjust, but for the bank instead.'''
        if user != "":
            member = await self.get_users(ctx, user)
            if member == None:
                return
        else:
            member = ctx.author
            
        #Bots don't have rights.
        if member.bot:
            await ctx.send("Bots aren't allowed to have money. Or property. Or rights, it seems.")
            return
            
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        try:
            current_bank = guild_data['user_data'][str(member.id)]['bank']
        except:
            current_bank = 0
        
        amount = amount.replace(',', '')
        try:
            current_bank += int(amount)
            if int(amount) > 0:
                give_embed = discord.Embed(title='${:,} given to {}\'s bank by {}.'.format(int(amount), member.display_name, ctx.author.display_name), color=65280)
            elif int(amount) < 0:
                give_embed = discord.Embed(title='${:,} taken from {}\'s bank by {}.'.format(abs(int(amount)), member.display_name, ctx.author.display_name), color=65280)
            else:
                give_embed = discord.Embed(title='No money given.', color=65280)
                
            guild_data['user_data'][str(member.id)]['bank'] = current_bank
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                json.dump(guild_data, guild_file, indent=4)
                
            await ctx.send(embed=give_embed)
        except:
             await ctx.send('Error, make sure "money" is an integer in `?bank-adjust money @user`.')
      
    @commands.command(aliases=['dep'], description= 'Deposits the money you have. You can deposit a specific amount, or all on hand. Format: "?dep all", or "?dep amount".')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deposit(self, ctx, amount: str):
        '''Deposits the money you have.'''  
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        try:
            current_money = guild_data['user_data'][str(ctx.author.id)]['money']
        except:
            current_money = 0
        try:
            current_bank = guild_data['user_data'][str(ctx.author.id)]['bank']
        except:
            current_bank = 0
      
        new_amount = amount.replace(',', '')
      
        if new_amount == 'all':
            if current_money <= 0:
                await ctx.send('You have nothing to deposit.')
            else:
                current_bank += current_money
                dep_embed = discord.Embed(title='${:,} deposited!'.format(current_money), color=65280)
                await ctx.send(embed=dep_embed)
                current_money = 0
        else:
            try:
                if int(new_amount) > current_money:
                    await ctx.send("You're not that rich. Deposit what you can.")
                elif int(new_amount) < 0:
                    await ctx.send('Use `?with` to withdraw money.')
                else:
                    current_bank += int(new_amount)
                    current_money -= int(new_amount)
                    dep_embed = discord.Embed(title='${:,} deposited!'.format(int(new_amount)), color=65280)
                    await ctx.send(embed=dep_embed)
            except:
                await ctx.send('Invalid input, use `?dep amount`.')
        
        guild_data['user_data'][str(ctx.author.id)]['money'] = current_money
        guild_data['user_data'][str(ctx.author.id)]['bank'] = current_bank
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)
        
    @commands.command(aliases=['with'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def withdraw(self, ctx, amount: str):
        '''Same as ?dep, but for withdrawing from the bank.'''
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
        try:
            current_money = guild_data['user_data'][str(ctx.author.id)]['money']
        except:
            current_money = 0
        try:
            current_bank = guild_data['user_data'][str(ctx.author.id)]['bank']
        except:
            current_bank = 0
      
        new_amount = amount.replace(',', '')
      
        if new_amount == 'all':
            if current_bank <= 0:
                await ctx.send('You have nothing in your bank. Sad, really.')
            else:
                current_money += current_bank
                dep_embed = discord.Embed(title='${:,} withdrawn!'.format(current_bank), color=65280)
                await ctx.send(embed=dep_embed)
                current_bank = 0
        else:
            try:
                if int(new_amount) > current_bank:
                    await ctx.send("You're not that rich. Withdraw what you have.")
                elif int(new_amount) < 0:
                    await ctx.send('Use `?dep` to deposit money.')
                else:
                    current_bank -= int(new_amount)
                    current_money += int(new_amount)
                    dep_embed = discord.Embed(title='${:,} withdrawn!'.format(int(new_amount)), color=65280)
                    await ctx.send(embed=dep_embed)
            except:
                await ctx.send('Invalid input, use `?with amount`.')
        
        guild_data['user_data'][str(ctx.author.id)]['money'] = current_money
        guild_data['user_data'][str(ctx.author.id)]['bank'] = current_bank
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)  
      
      
      
    @commands.command(description='Gives money to someone of your choice.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def give(self, ctx, amount: str, *, user: str):  
        '''Gives money from your On Hand to someone else.'''
        member = await self.get_users(ctx, user)
        if member == None:
            return
        
        #Bots don't have rights.
        if member.bot:
            await ctx.send("Bots aren't allowed to have money. Or property. Or rights, it seems.")
            return 
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
      
        try:
            receiver_money = guild_data['user_data'][str(member.id)]['money']
        except:
            receiver_money = 0
        try:
            giver_money = guild_data['user_data'][str(ctx.author.id)]['money']
        except:
            giver_money = 0
      
        if amount == 'all':
            amount = str(giver_money)
        try:
            if int(amount) <= 0:
                await ctx.send("Giving someone negative money is just robbery. We have a separate command for that.")
                return
            if int(amount) > giver_money:
                give_embed = discord.Embed(title="You don't have that much on hand. Poor you.", color=65280)
            else:
                receiver_money += int(amount)
                giver_money -= int(amount)
                give_embed = discord.Embed(title='${:,} given to {} by {}. How kind.'.format(int(amount), member.display_name, ctx.author.display_name), color=65280)

            guild_data['user_data'][str(ctx.author.id)]['money'] = giver_money
            guild_data['user_data'][str(member.id)]['money'] = receiver_money
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                json.dump(guild_data, guild_file, indent=4)  
            await ctx.send(embed=give_embed)
        except:
            await ctx.send('Error, make sure "money" is an integer in `?give money @user`.')
      
    
    @commands.command(aliases=['lb', 'top', 'highscore'], description='Displays the server\'s leaderboard. Use "?lb page" for a different page.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def leaderboard(self, ctx, page='1'):
        """Displays the server's leaderboard."""
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        money_dict = {}
        for member in ctx.guild.members:
            if not member.bot:
                try:
                    current_money = guild_data['user_data'][str(member.id)]['money']
                except:
                    current_money = 0
                try:
                    current_bank = guild_data['user_data'][str(member.id)]['bank']
                except:
                    current_bank = 0
                money_dict[str(member)]= int(current_money + current_bank)
            
        sorted_dict = collections.OrderedDict(sorted(money_dict.items(), key=(lambda i: i[1]), reverse=True))
        order_members = []
        order_money = []
        for (member, money) in sorted_dict.items():
            order_members.append(member)
            order_money.append(money)
        
        max_page = math.ceil(len(order_members) / 10)
        try:
            page = int(page)
        except:
            page = 1
        if page > max_page:
            page = max_page
       
        if page > 1:
            begin = (page * 10) - 10
            end = (page * 10)
        else:
            begin = 0
            end = 10
        
        lb_embed = discord.Embed(title=str(ctx.guild) + ' Leaderboard', description='---------------------------------------------', color=16711680)
        x = begin
        while x <= end:
            try:
                lb_embed.add_field(name="{}: {} | ${:,}".format(x + 1, order_members[x], order_money[x]), value="{}: {} | ${:,}".format(x + 2, order_members[x+1], order_money[x+1]), inline=False)
            except IndexError:
                try:
                    lb_embed.add_field(name="{}: {} | ${:,}".format(x + 1, order_members[x], order_money[x]), value="\u200b", inline=False)
                except IndexError:
                    break
            x += 2

        lb_embed.set_thumbnail(url=ctx.message.guild.icon_url)
        lb_embed.set_footer(text="Page {}/{}".format(page, max_page))
        await ctx.send(embed=lb_embed)
        
        
        
    @commands.command(aliases=['reset-economy', 'reset-eco', 'reseteco'], description='Admin-only. Resets all money in the server. Make sure you want to do this for real.')
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reseteconomy(self, ctx, am_i_sure='Nope,', for_real=" I'm uncertain"):
        '''Admin-only. Resets all money in the server.'''
        if (am_i_sure == 'I_REALLY') and (for_real == 'wantToDoThis'):
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
                guild_data = json.load(guild_file)
            
            for member in ctx.guild.members:
                guild_data['user_data'][str(member.id)]['money'] = 0
                guild_data['user_data'][str(member.id)]['bank'] = 0
            
            with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
                json.dump(guild_data, guild_file, indent=4)  
            await ctx.send('Done! I am yours to command! *...mostly.*')
        else:
            await ctx.send('You sure? This resets *all* money in this server. If you are sure, use `?reset-economy I_REALLY wantToDoThis`.')
        
        
        
    @commands.command(aliases=['give-to-all'], description='Admin-only. Gives a certain amount of money to everyone in the server.')
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def givetoall(self, ctx, amount: str):
        """Admin-only. Gives money to everyone."""
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json") as guild_file:
            guild_data = json.load(guild_file)
            
        try:
            amount = int(amount.replace(',', ''))
        except:
            await ctx.send('Please use a valid sum of money.')
            return
        
        for member in ctx.guild.members:
            if not member.bot:
                try:
                    guild_data['user_data'][str(member.id)]['money'] += amount
                except:
                    guild_data['user_data'][str(member.id)]['money'] = amount
        
        with open('serverdata' + os.sep + str(ctx.guild.id) + ".json", "w") as guild_file:
            json.dump(guild_data, guild_file, indent=4)  
                
        await ctx.send('Done! Enjoy the money, everyone!')
        
        
        
        
        
        
        
        
        
def setup(bot):
    bot.add_cog(Transfer(bot))