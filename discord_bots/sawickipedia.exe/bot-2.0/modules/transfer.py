#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os



class Transfer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    async def list_to_games(self, bot):
        games_file = open("botdata" + os.sep + "games.txt", "a")
        GAMES = ['with Snowden', 'the NSA', 'with Lizard-People', 'with The Zucc', 'with Element 94', 'with the Doctor','the Doctor', 'with Space-Time', 'on the Death Star', 'God', 'with Nightmares', 'with Lucifer', 'Crap(s)','with Test Monkeys', 'Society', 'with Logs', 'at 88 MPH', 'you all for fools', 'with the One Ring', 'in Mordor','with my Palantir', 'with Myself', 'with Pythons', 'in CMD', 'as Root', 'Hang Man', 'with your passwords','with your money', 'with your existence', 'you', 'with Just Monika', 'with Explosives', 'with Lives','with your Life', 'on a Good Christian Minecraft Server', 'a Game.', 'with You...', 'in the Meth Lab','with your S.O.', 'with Death', 'with Lightsabers', 'with your Heart', 'Jedi Mind-tricks', 'Mind-games']
        for item in GAMES:
            games_file.write(item)
    
    
    

def setup(bot):
    bot.add_cog(Transfer(bot))