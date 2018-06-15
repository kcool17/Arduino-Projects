#!/usr/bin/env python

#Imports
import discord
from discord.ext import commands
import pickle
import urllib.request
import os
import asyncio
import datetime
import random

DEVS = ["357953549738573835"]
GAMES = ["with Snowden", "the NSA", "with Lizard-People", "with The Zucc", "with Element 94", "with the Doctor", "the Doctor", "with Space-Time", "on the Death Star", "God", "with Nightmares", "with Lucifer", "Crap(s)", "with Test Monkeys", "Society", "with Logs", "at 88 MPH", "you all for fools", "with the One Ring", "in Mordor", "with my Palantir", "with Myself", "with Pythons", "in CMD", "as Root", "Hang Man", "with your passwords", "with your money", "with your existence", "you", "with Just Monika", "with Explosives", "with Lives", "with your Life", "on a Good Christian Minecraft Server", "a Game.", "with You...", "in the Meth Lab", "with your S.O.", "with Death", "with Lightsabers", "with your Heart", "Jedi Mind-tricks", "Mind-games"]

#Get Autoresponder Images
with urllib.request.urlopen('https://cdn.glitch.com/b62dbbb6-5065-4db0-ac88-ce2ffbf2c18f%2Fpaged.gif?1526252261731') as url:
    with open('paged.gif', 'wb') as f:
        f.write(url.read())
with urllib.request.urlopen('https://cdn.glitch.com/b62dbbb6-5065-4db0-ac88-ce2ffbf2c18f%2Fnopower.gif?1526252261805') as url:
    with open('nopower.gif', 'wb') as f:
        f.write(url.read())

#prefix
def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    try:
        prefix = pickle.load(open("servers" + os.sep + message.server.id + os.sep + "prefix.p", "rb"))
    except:
        prefix = '?'
    #Check to see if we are outside of a guild. e.g DM's etc.
    if not message.server:
        #Only allow ? to be used in DMs
        return '?'
    
    return commands.when_mentioned_or(prefix)(bot, message)

description = '''A bot that can do things.'''

startup_extensions = ["modules.test1", #Default extensions (all enabled)
                      "modules.settings",
                      "modules.developer",
                      "modules.misc",
                      "modules.economy",
                      "modules.minigames",
                      ] 

bot = commands.Bot(command_prefix=get_prefix, description=description)

@bot.event
async def on_ready():
    #Bot preferences Setup
    myServers = bot.servers
    for server in myServers:
        if not os.path.exists("servers" + os.sep + str(server.id)):
            os.makedirs("servers" + os.sep + str(server.id))

    startup_extensions = []
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="with Snowden"))


async def background_task(): #Runs every 1 second, constantly.
    await bot.wait_until_ready()
    presenceCount = 0
    global GAMES
    while not bot.is_closed:
        #"Playing" Status
        if presenceCount == 30:
            randomGame = random.randint(0, len(GAMES)-1)
            await bot.change_presence(game=discord.Game(name=GAMES[randomGame]))
            presenceCount = 0
                 
        #Filesystem
        myServers = bot.servers
        for server in myServers:
            ADMINS =[]
            if not os.path.exists("servers" + os.sep + str(server.id)):
                os.makedirs("servers" + os.sep + str(server.id))
            for member in server.members:
                if not os.path.exists("servers" + os.sep + str(server.id) + os.sep + str(member.id)):
                    os.makedirs("servers" + os.sep + str(server.id) + os.sep + str(member.id))
                #Admin Permission
                if member.id not in ADMINS and member.server_permissions.administrator == True:
                    ADMINS.append(member.id)
            for role in server.roles:
                if not os.path.exists("servers" + os.sep + str(server.id) + os.sep + str(role.id)):
                    os.makedirs("servers" + os.sep + str(server.id) + os.sep + str(role.id))
            for dev in DEVS:
                ADMINS.append(dev)
            pickle.dump(ADMINS, open("servers" + os.sep + str(server.id) + os.sep + "ADMINS.p", "wb"))
        #Salary
        for server in myServers:
            try:
                waitSal = pickle.load(open("servers" + os.sep + str(server.id) + os.sep  + "waitSal.p", "rb"))
            except:
                waitSal = 0
            try:
                salHour = pickle.load(open("servers" + os.sep + str(server.id) + os.sep  + "salHour.p", "rb"))
                salMinute = pickle.load(open("servers" + os.sep + str(server.id) + os.sep  + "salMinute.p", "rb"))
            except:
                salHour = 0
                salMinute = 0
            now = datetime.datetime.now()
            now = int((datetime.timedelta(hours=24) - (now - now.replace(hour=salHour, minute=salMinute, second=0, microsecond=0))).total_seconds() % (24 * 3600))
            if now <=5 and waitSal <=0:
                waitSal = 10
                pickle.dump(waitSal, open("servers" + os.sep + str(server.id) + os.sep  + "waitSal.p", "wb"))
                try:
                    toChannel = pickle.load(open("servers" + os.sep + str(server.id) + os.sep  + "channel.p", "rb"))
                except:
                    toChannel = server.default_channel
                salEmbed = discord.Embed(title="Salary Pay", color=0x00ff00)
                for role in bot.get_server(server.id).roles:
                    try:
                        currentSal = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(role.id) + os.sep + "salary.p", "rb"))
                    except:
                        currentSal = 0
                    if currentSal != 0:
                        for member in server.members:
                            for item in member.roles:
                                if item.id == role.id:
                                    try:
                                        currentMoney = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "money.p", "rb"))
                                    except:
                                        currentMoney = 0
                                    currentMoney+=currentSal
                                    pickle.dump(currentMoney, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "money.p", "wb"))
                        toSay = str(role) + " got their salary of $" + "{:,}".format(currentSal)
                        if toSay[0] == "@":
                            await bot.send_message(toChannel, toSay[1:])
                        else:
                            await bot.send_message(toChannel, toSay)
            else:
                waitSal -= 1
                if waitSal <= -1:
                    waitSal = -1
                pickle.dump(waitSal, open("servers" + os.sep + str(server.id) + os.sep  + "waitSal.p", "wb"))


        #Roulette
        for server in myServers:
            try:
                rouletteOn = pickle.load(open("servers" + os.sep + str(server.id) + os.sep +"rouletteOn.p", "rb"))
            except:
                rouletteOn = False
            if rouletteOn:
                
                try:
                    rouletteBegun = pickle.load(open("servers" + os.sep + str(server.id) + os.sep +"rouletteBegun.p", "rb"))
                except:
                    rouletteBegun = False
                try:
                    rouChannel = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + "rouChannel.p", "rb"))
                except:
                    rouChannel = server.default_channel
                try:
                    rouCount = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + "rouCount.p", "rb"))
                except:
                    rouCount = 30
                if not rouletteBegun:
                    rouCount = 30
                    rouletteBegun = True
                else:
                    rouCount -=1
                if rouCount == 10:
                    await bot.send_message(rouChannel, "10 seconds left for roulette!")
                if rouCount <0:
                    winNum = random.randint(1, 36)
                    winCol = random.choice(["black", "red"])
                    await bot.send_message(rouChannel, "The ball landed on **" + winCol + " " + str(winNum) + "**!")
                    someoneWon = False
                    for member in server.members:
                        try:
                            playingRoulette = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "playingRoulette.p", "rb"))
                        except:
                            playingRoulette = False
                        if playingRoulette:
                            try:
                                currentMoney = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "money.p", "rb"))
                            except:
                                currentMoney = 0
                            try:
                                didWin = False
                                rouletteMultiplier = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "rouletteMultiplier.p", "rb"))
                                rouletteGuessType = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "rouletteGuessType.p", "rb"))
                                rouletteGuess = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "rouletteGuess.p", "rb"))
                                rouletteBet = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "rouletteBet.p", "rb"))
                                if rouletteGuessType =="numbers":
                                    if rouletteGuess == winNum:
                                        didWin = True
                                elif rouletteGuessType == "oddeven":
                                    if winNum %2 == 0 and rouletteGuess == "even":
                                        didWin = True
                                    elif winNum%2 != 0 and rouletteGuess == "odd":
                                        didWin = True
                                elif rouletteGuessType == "color":
                                    if winCol == rouletteGuess:
                                        didWin = True
                                elif rouletteGuessType == "dozen":
                                    if winNum<=12 and winNum>0 and rouletteGuess=="1st":
                                        didWin = True
                                    elif winNum<=24 and winNum>12 and rouletteGuess=="2nd":
                                        didWin = True
                                    elif winNum<=36 and winNum>24 and rouletteGuess=="3rd":
                                        didWin = True

                                        
                                if didWin:
                                    winMoney =  rouletteBet * rouletteMultiplier
                                    currentMoney += winMoney
                                    someoneWon = True
                                    await bot.send_message(rouChannel, str(member) + " won $" + "{:,}".format(winMoney) + "!")
                                    
                            except:
                                pass
                            pickle.dump(False, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "playingRoulette.p","wb"))
                            pickle.dump(currentMoney, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "money.p","wb"))
                    if not someoneWon:
                        await bot.send_message(rouChannel, "**No winners...**")
                    rouletteBegun = False
                    pickle.dump(False, open("servers" + os.sep + str(server.id) + os.sep + "rouletteOn.p","wb"))
                pickle.dump(rouletteBegun, open("servers" + os.sep + str(server.id) + os.sep + "rouletteBegun.p","wb"))
                pickle.dump(rouCount, open("servers" + os.sep + str(server.id) + os.sep + "rouCount.p","wb"))
                
        #Cooldowns
        for server in myServers:
            for member in server.members:
                try:
                    workCooldown = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "workCooldown.p", "rb"))
                except:
                    workCooldown = 0
                workCooldown -= 1

                if workCooldown<-60:
                    workCooldown=-60
                pickle.dump(workCooldown, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "workCooldown.p", "wb"))
                try:
                    crimeCooldown = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "crimeCooldown.p", "rb"))
                except:
                    crimeCooldown = 0
                crimeCooldown -= 1
                if crimeCooldown<-60:
                    crimeCooldown=-60
                pickle.dump(crimeCooldown, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "crimeCooldown.p", "wb"))
                try:
                    robCooldown = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "robCooldown.p", "rb"))
                except:
                    robCooldown = 0
                robCooldown -= 1
                if robCooldown<-60:
                    robCooldown=-60
                pickle.dump(robCooldown, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "robCooldown.p", "wb"))

                
                try:
                    questionCanGuess = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "questionCanGuess.p", "rb"))
                except:
                    questionCanGuess = False
                if questionCanGuess:
                    try:
                        trivCool = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "trivCool.p", "rb"))
                    except:
                        trivCool = 0
                    if trivCool <=0:
                        try:
                            trivChannel = pickle.load(open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "trivChannel.p", "rb"))
                        except:
                            trivChannel = server.default_channel
                        pickle.dump(False, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "questionCanGuess.p", "wb"))
                        await bot.send_message(trivChannel, str(member) + " ran out of time for trivia! Oops.")
                    trivCool -= 1
                    pickle.dump(trivCool, open("servers" + os.sep + str(server.id) + os.sep + str(member.id) + os.sep + "trivCool.p", "wb"))
        #Other counts
        presenceCount += 1

        await asyncio.sleep(1)
        
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    
    #Give money per message:
    try:
        try:
            currentMoney = pickle.load(open("servers" + os.sep + str(message.server.id) + os.sep + str(message.author.id) + os.sep + "money.p", "rb"))
        except:
            currentMoney = 0
        currentMoney += random.choice([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 5])
        pickle.dump(currentMoney, open("servers" + os.sep + str(message.server.id) + os.sep + str(message.author.id) + os.sep + "money.p","wb"))
    except:
        pass
    #Get DMs
    if message.channel.is_private and message.author.id != "357953549738573835":
        toChannel = await bot.get_user_info("357953549738573835")
        await bot.send_message(toChannel, "**Message from " + str(message.author) + "[*" + str(message.author.id) + "*]:** " + str(message.content))
    #Being paged
    if message.content == "<@421015092830666754>" or message.content == "<@!421015092830666754>":
        msg1 = 'Somebody page me?'.format(message)
        msg2 = 'Hello {0.author.mention}. *Glad to see you.*'.format(message)

        await bot.send_message(message.channel, msg1)
        await bot.send_file(message.channel, 'paged.gif')
        await bot.send_message(message.channel, msg2)

        

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            
    bot.loop.create_task(background_task())
    bot.run(pickle.load(open("token.p", "rb")))
