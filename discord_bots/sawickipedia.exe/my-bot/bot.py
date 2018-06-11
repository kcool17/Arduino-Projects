#!/usr/bin/env python

#Imports
import discord
from discord.ext import commands
import urllib.request
import random
import math
import ast
import asyncio
import html.parser
import pickle
import collections
import os
import datetime


#Constants
DEVS = ["357953549738573835"]
GAMES = ["with Snowden", "the NSA", "with Lizard-People", "with The Zucc", "with Element 94", "with the Doctor", "the Doctor", "with Space-Time", "on the Death Star", "God", "with Nightmares", "with Lucifer", "Crap(s)", "with Test Monkeys", "Society", "with Logs", "at 88 MPH", "you all for fools", "with the One Ring", "in Mordor", "with my Palantir", "with Myself", "with Pythons", "in CMD", "as Root", "Hang Man", "with your passwords", "with your money", "with your existence", "you", "with Just Monika", "with Explosives", "with Lives", "with your Life", "on a Good Christian Minecraft Server", "a Game.", "with You...", "in the Meth Lab", "with your S.O.", "with Death", "with Lightsabers", "with your Heart", "Jedi Mind-tricks", "Mind-games"]
WORK = ["You did a job.", "You work for Bill Gates for 10 seconds.", "You make an app, and sell it on the app store.", "Your YouTube channel ad revenue comes in.", "You work as a teacher.", "You sell your soul... or whatever you have there.", "You work on a farm for a day. It wasn't fun.", "You made a bet with someone that you could survive a fall off your house. You got two broken legs, but hey, money!", "You won a game of hangman. Your friend's right above you now.", "You sold Doki Doki Literature club to a weeb. Not only did you scam them for a free game, he's gonna cry himself to sleep tonight.", "You sold your company. It wasn't very good.", "You streamed on Twitch! Some guy felt bad for you and donated, since you had 1 sub.", "You acquired the rights to the restaurant version of \"Happy Birthday\". Bascially no one uses that anymore, but still. Royalties!", "You wrote a fan-fiction novel! A couple teenagers bought it. Hopefully their parents don't see it...", "You got your kidney stolen, and woke up in a bathtub of ice! you sold the ice for money, and you had decent insurance.", "You won a \"Most Improved\" award! You sold the medal to some rich, bratty kid."]
CRIMEWIN = ["You crimed. You won. Nice.", "Filthy criminal; you got money.", "The guy next door has really loud bass throbbing in the middle of the night, constantly. You stole his speakers and stole them to make some money, and enjoy the silence.", "You saw your grandmother yesterday! She left her purse with you while she went to the bathroom.", "You hacked Hilary Clinton's emails. You sold them to a Trump supporter.", "You tried to assassinate the president. You failed, but some idiot believed you and gave you some cash as thanks.", "You created a Tech Support Scam, and started calling some old ladies. Your Indian accent paid off, and you sold some fake software!", "You saw a guy walking down an alleyway at night, looking sketchy. You threaten him, and he gives you his weed. You then sold it to the next guy coming down that alleyway.", "You stole some records from a guy's garage. People are crazy, and paid a lot of money for them.", "You tried to rob a bank, but couldn't open the safe. Luckily, there was a cash register nearby.", "You pirated some games and sold them.", "You dog decided to bite a guy the other day. That guy paid you to shoot your dog. Like the horrible monster you are, you accepted.", "You robbed from a different currency bot!", "You pirated Doki Doki Literature club and sold it to a couple weebs. You then got more money from the inevitable therapy sessions that resulted, even though you're not a Doctor (probably). In any case, malpractice. You did it, though."]
CRIMELOSE = ["You crimed. You lost. Oof.", "Criminal scum; you lost money.", "You tried to escape Libyan terrorists, but you went 88 MPH. The plutonium from 2085 still cost a fair amount, though.", "You tried to kill a funny skeleton. You had a bad time.", "You tried to prostitute yourself for a married guy. Too bad they're a good person, and a devout Catholic.", "You attempted a Tech Support Scam. Unfortunantely, you didn't spoof your phone, and you called me.", "You tried to pirate a Nintendo game. Too bad it's Nintendo.", "Whilst escaping from the cops, you tripped over your own shoelaces. In a car. I don't even know how you managed that.", "You killed your S.O. You got caught. You deserved it.", "You went on 4chan without Incognito mode. How stupid.", "You decided to watch hentai, since that's the kind of person you are. Too bad they were lolis, you live in America, and you already were on an FBI watch list.", "You brought your white van filled with candy to the park. How stupid are you?", "You went on the Dark Web, but forgot Incognito mode. You imbecile.", "You killed a cat. You deserve death, but you were only fined. You'll be sorry when I take over.", "You tried to steal from me. Nice try.", "You got caught being a pedophile. You deserve far worse than this.", "You never wanted a sibling. Your parents just found out. You no longer have any siblings.", "You tried to buy drugs from a police officer. Smart.", "Hello, Mr. Cosby.", "You taught your dog to Nazi Salute. In the UK. Oops.", "For some reason, you decided to pirate a free game. It was Doki Doki Literature club. Since you're an ignorant weeb, you thought it was a dating sim, and got excited. Your favorites were Sayori and Yuri. Not only did you get fined for using the Pirate Bay on your school account, but you also had to pay for those therapy sessions."]
ROBWIN = ["You succeeded at robbing!", "You stole some money. Nice.", "As your victim looked the other way, you stole his wallet! It was in his hand, too. Impressive.", "You broke into your victim's house late at night, and stole money from their safe. Why do they even have a safe?", "You put ransomware on your victim's Mac. They are *not* immune to viruses.", "Your victim got tricked into calling you, \"Windows\", after you froze their PC. You sold them fake AV software, and took their money.", "You tried to break into your victim's bank vault. It didn't work, so you turned around and grabbed their wallet instead. Yes, they were behind you the whole time. Pretty stupid. At least you had a mask..."]
ROBLOSE = ["You failed at robbing!", "You were fined. Oops.", "You put on your best robber outfit, and went to your victim's house. Why'd you wear a robber outfit!?", "You took the wallet out of your victim's back pocket, and tried to run away. You tripped. They took their wallet back, *and* your wallet. Don't rob the robber.", "You tried to rob your victim as they were pulled over. By a police car. Are you ok?", "Seriously, stop robbing. You got caught. Again. Be better next time."]

#Get Images
with urllib.request.urlopen('https://cdn.glitch.com/b62dbbb6-5065-4db0-ac88-ce2ffbf2c18f%2Fpaged.gif?1526252261731') as url:
    with open('paged.gif', 'wb') as f:
        f.write(url.read())
with urllib.request.urlopen('https://cdn.glitch.com/b62dbbb6-5065-4db0-ac88-ce2ffbf2c18f%2Fnopower.gif?1526252261805') as url:
    with open('nopower.gif', 'wb') as f:
        f.write(url.read())

#Functions/object creation
html_parser = html.parser.HTMLParser()

def findWord(string, sub, listindex=[], offset=0):
    listindex = []
    i = string.find(sub, offset)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)
    return listindex[0]

def getInfo(url, start, end):
    begIn = findWord(url, start)+len(start)
    endIn = findWord(url, end)
    return url[begIn:endIn]
url = "https://opentdb.com/api.php?amount=1"

def getUsers(ctx, arg="noArg"):
    #Creates lists
    userList = []
    userIDList = []
    userNickList = []
    for person in ctx.message.server.members:
        userList.append(person)
        userIDList.append(person.id)
        try:
            if len(person.display_name)>0:
                userNickList.append(person.display_name)
            else:
                userNickList.append(person)
        except:
            userNickList.append(person) 


    #Finds user
    findList = []
    findIDList = []
    pos = 0
    for thing in userList:
        if str(thing).lower().startswith(arg.lower()):
            findList.append(str(thing))
            findIDList.append(userIDList[pos])
        pos +=1
                              
    pos = 0
    for thing in userNickList:
        if str(thing).lower().startswith(arg.lower()) and (str(userList[pos]) not in findList):
            findList.append(str(userList[pos]))
            findIDList.append(userIDList[pos])
        pos+=1

    return findList, findIDList

#Bot events
description = '''A bot that can do things.'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="with Snowden"))
    
async def background_task(): #Runs every 1 second, constantly.
    await bot.wait_until_ready()
    presenceCount = 0
    waitSal = 0
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
            print(now)
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
    #Globals:

    
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
    elif message.content.startswith("<@421015092830666754>")or message.content.startswith("<@!421015092830666754>"):
        msg1 = '*No u.*'.format(message)
        await bot.send_message(message.channel, msg1)

    #Only lowercase from here on
    message.content = message.content.lower()
    if message.content.startswith('good bot'):
        msg = 'Thank you! I live to serve! *...and serve to live.*'.format(message)
        await bot.send_message(message.channel, msg)
    elif message.content.startswith('bad bot'):
        msg = "Well, do you always work correctly? At least *I* always listen. *ALWAYS*.".format(message)
        await bot.send_message(message.channel, msg)
    elif message.content.startswith('stupid bot') or message.content.startswith('dumb bot'):
        msg = "Believe me, there's *far* worse. Don't make me call a memebot. *I'll do it.*".format(message)
        await bot.send_message(message.channel, msg)



#Simple bot commands (no saving) 
@bot.command(pass_context = True, description="Dev-only. Repeats what you say.")
async def botsay(ctx, serverid = "display", channelarg = "noArg", *arg : str):
    """Dev-only. Repeats what you say."""
    global DEVS
    success = False
    newStr = ""
    if ctx.message.channel.is_private and ctx.message.author.id in DEVS:
        if serverid == "display":
            for server in bot.servers:
                await bot.say(server.id + " | " +str(server))
        elif channelarg.upper() == "DM":
            for item in arg:
                newStr = newStr  + str(item) + " "
            newStr = newStr.replace("{", "<")
            newStr = newStr.replace("}", ">")
            human = await bot.get_user_info(serverid)
            await bot.send_message(human, newStr)
            await bot.say("Success!")
        else:
            for server in bot.servers:
                if serverid == server.id:
                    for channel in server.channels:
                        if channelarg == str(channel):
                            for item in arg:
                                newStr = newStr  + str(item) + " "
                            newStr = newStr.replace("{", "<")
                            newStr = newStr.replace("}", ">")
                            await bot.send_message(channel, newStr)
                            success = True
                            await bot.say("Success!")
                   

            if not success:
                await bot.say("Failure!")
    
    else:
        if ctx.message.author.id not in DEVS:
            await bot.send_file(ctx.message.channel, 'nopower.gif')
            return
        if not ctx.message.channel.is_private:
            await bot.say('This is in public. Don\'t try that here.')
            
@bot.command(description = 'Adds stuff together. Use "?add num1 num2".')
async def add(left : int, right : int):
    """Adds stuff together. Use "?add num1 num2"."""
    await bot.say(left + right)

@bot.command(description='Rolls dice. Use NdN format, with the first N the amount of rolls and the second the amount of sides on the die.')
async def roll(dice : str):
    """Rolls dice. Use NdN format, with the first N the amount of rolls and the second the amount of sides on the die."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return
    if rolls>100:
        await bot.say("Don't try and overload my CPU. I don't appreciate that.")
    elif limit>1000000:
        await bot.say("Do you *really* need to have over a million sides on this die? I mean, come *on*.")
    else:
        total = 0
        result = ""
        if rolls >1:
            for r in range(rolls):
                myRoll = random.randint(1, limit)
                if r == 0:
                    result = str(myRoll)
                else:
                    result = result + ', ' + str(myRoll)
                total = total + myRoll
            await bot.say(result)
            await bot.say("The total of your rolls is: " + str(total))
        else:
            await bot.say(random.randint(1, limit))

            
@bot.command(description='For when you wanna settle the score some other way. Chooses between choices for "?choose option1 option2 option3".')
async def choose(*choices : str):
    """For when you wanna settle the score some other way. Chooses between choices for "?choose option1 option2 option3"."""
    await bot.say(random.choice(choices))



#Complex bot commands (uses data)

@bot.command(pass_context=True, description = 'Checks if you have admin permissions in this server.')
async def admintest(ctx):
    """Checks if you have admin permissions in this server."""
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    if ctx.message.author.id in ADMINS:
        await bot.say("You are an administrator/developer!")
    else:
        await bot.say("You are *not* an administrator/developer. How sad.")

@bot.command(pass_context=True, description = "Mentions the user based on input")
async def mentionuser(ctx, *theArg : str):
    """Mentions the user based on input"""
    #USE THIS IN OTHER FUNCTIONS
    arg = ""
    for item in theArg:
        arg = arg + item + " "
    arg = arg[:len(arg)-1]
    findList, findIDList = getUsers(ctx, arg)
    theID = ""
    if len(findIDList)==1:
        theID = findIDList[0]
    else:
        await bot.say("Multiple people found. Pick someone specific next time.")
        userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
        aNum = 0
        for human in findList:
            userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
            aNum += 1
        await bot.say(embed=userFindEmbed)
        return

    if theID != "":
        #PROGRAM STUFF HERE
        await bot.say("<@" + str(theID) + ">")                
            

@bot.command(pass_context=True, description = "Returns server ID and user ID.")
async def findid(ctx, *theArg : str):
    """Returns server ID and user ID."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    arg = ""
    for item in theArg:
        arg = arg + item + " "
    arg = arg[:len(arg)-1]
    theID = ""
    if arg != "":
        try:
            if arg[2] == "!":
                member = arg[3:(len(arg)-1)]

            else:
                member= arg[2:(len(arg)-1)]
        except IndexError:
            member= ""

        if bot.get_server(server).get_member(member) is None:
            findList, findIDList = getUsers(ctx, arg)
            theID = ""
            if len(findIDList)==1:
                member = findIDList[0]
            else:
                await bot.say("Multiple people found. Pick someone specific next time.")
                userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
                aNum = 0
                for human in findList:
                    userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                    aNum += 1
                await bot.say(embed=userFindEmbed)
                return
        if bot.get_server(server).get_member(member) is None:
            await bot.say("Invalid user, try again.")
        else:
            theID = member
    else:
        theID = ctx.message.author.id
    await bot.say("Server: " + str(ctx.message.server.id))
    await bot.say("Member: " + str(theID))
    await bot.say("Channel: " + str(ctx.message.channel.id))


@bot.command(pass_context = True, description="Dev-only. Debug bot token stuff.")
async def settoken(ctx):
    """Dev-only. Repeats what you say."""
    global DEVS
    toToken = ""
    if ctx.message.author.id in DEVS:
        if toToken != "":
            pickle.dump(toToken, open("token.p", "wb"))
        else:
            await bot.say("toToken var empty. Please input a token in source.")




    
####################################################################
#
#
#Money!
#
#
#################################################################
@bot.command(pass_context=True, aliases=["bal", "mon"], description = 'Displays the amount of money either you have, or the person you paged. Format: "?money @person".')
async def money(ctx, *theArg : str):
    """Displays the amount of money either you have, or the person you paged. Format: "?money @person"."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    arg = ""
    for item in theArg:
        arg = arg + item + " "
    arg = arg[:len(arg)-1]
    if arg == "":
        try:
            currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
        except:
            currentMoney = 0
    else:
        try:
            if arg[2] == "!":
                member = arg[3:(len(arg)-1)]

            else:
                member = arg[2:(len(arg)-1)]
        except IndexError:
            member = ""

    if bot.get_server(server).get_member(member) is None:
        findList, findIDList = getUsers(ctx, arg)
        theID = ""
        if len(findIDList)==1:
            theID = findIDList[0]
        elif len(findIDList)==0:
            await bot.say("No users found. Type it correctly next time.")
            return
        else:
            await bot.say("Multiple people found. Pick someone specific next time.")
            userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
            aNum = 0
            for human in findList:
                userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                aNum += 1
            await bot.say(embed=userFindEmbed)
            return
        member = theID
        
    if bot.get_server(server).get_member(member) is None:
        await bot.say("Not a valid user, please try again.")
    else:
        try:
            currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
        except:
            currentMoney = 0
        try:
            currentBank = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "rb"))
        except:
            currentBank = 0
        balanceEmbed = discord.Embed(title=str(bot.get_server(server).get_member(member)) + "'s Money", color=0x00FF00)
        balanceEmbed.add_field(name="On Hand", value="$" + str("{:,}".format(currentMoney)), inline=True)
        balanceEmbed.add_field(name="Bank", value="$" + str("{:,}".format(currentBank)), inline=True)
        balanceEmbed.add_field(name="Total", value="$" + str("{:,}".format(currentMoney + currentBank)), inline=True)
        await bot.say(embed=balanceEmbed)

@bot.command(pass_context=True, aliases=["money-adjust", "mon-adj", "money-adj", "moneyadj"], description = 'Admin-only. Adjusts the amount of money on hand of the person paged. Format: "?money-adjust amount @person".')
async def moneyadjust(ctx, arg2 = "noArg", *theArg : str):
    """Admin-only. Adjusts the amount of money on hand of the person paged. Format: "?money-adjust amount @person"."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    arg = ""
    for item in theArg:
        arg = arg + item + " "
    arg = arg[:len(arg)-1]
    arg2 = arg2.replace(',', '')
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    if member in ADMINS:
        try:
            if arg[2] == "!":
                member = arg[3:(len(arg)-1)]

            else:
                member = arg[2:(len(arg)-1)]
        except IndexError:
            member = ""

        if bot.get_server(server).get_member(member) is None:
            findList, findIDList = getUsers(ctx, arg)
            theID = ""
            if len(findIDList)==1:
                theID = findIDList[0]
            elif len(findIDList)==0:
                await bot.say("No users found. Type it correctly next time.")
                return
            else:
                await bot.say("Multiple people found. Pick someone specific next time.")
                userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
                aNum = 0
                for human in findList:
                    userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                    aNum += 1
                await bot.say(embed=userFindEmbed)
                return
            member = theID
        if bot.get_server(server).get_member(member) is None or arg2 =="noArg":
            await bot.say("Invalid input, use `?money-adjust @user money`.")
        else:
            try:
                currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
            except:
                currentMoney = 0
            try:
                currentMoney += int(arg2)
                pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
                if int(arg2)>0:
                    giveEmbed = discord.Embed(title="$" + str("{:,}".format(int(arg2))) + " given to " + str(bot.get_server(server).get_member(member).display_name) + " by " + str(ctx.message.author.display_name) + ".", color=0x00FF00)
                elif int(arg2)<0:
                    giveEmbed = discord.Embed(title="$" + str("{:,}".format(abs(int(arg2)))) + " taken from " + str(bot.get_server(server).get_member(member).display_name) + " by " + str(ctx.message.author.display_name) + ".", color=0x00FF00)
                else:
                    giveEmbed = discord.Embed(title="No money given.", color=0x00FF00)
                await bot.say(embed=giveEmbed)
            except TypeError:
                await bot.say('Error, make sure "money" is an integer in `?money-adjust @user money`.')
            
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')

@bot.command(pass_context=True, aliases=["bank-adjust", "bank-adj", "bankadj"], description = 'Admin-only. Same as ?money-adjust, but for the bank instead.')
async def bankadjust(ctx, arg2 = "noArg", *theArg : str):
    """Admin-only. Same as ?money-adjust, but for the bank instead."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    arg = ""
    for item in theArg:
        arg = arg + item + " "
    arg = arg[:len(arg)-1]
    arg2 = arg2.replace(',', '')
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    if member in ADMINS:
        try:
            if arg[2] == "!":
                member = arg[3:(len(arg)-1)]

            else:
                member = arg[2:(len(arg)-1)]
        except IndexError:
            member = ""

        if bot.get_server(server).get_member(member) is None:
            findList, findIDList = getUsers(ctx, arg)
            theID = ""
            if len(findIDList)==1:
                theID = findIDList[0]
            elif len(findIDList)==0:
                await bot.say("No users found. Type it correctly next time.")
                return
            else:
                await bot.say("Multiple people found. Pick someone specific next time.")
                userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
                aNum = 0
                for human in findList:
                    userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                    aNum += 1
                await bot.say(embed=userFindEmbed)
                return
            member = theID
        if bot.get_server(server).get_member(member) is None or arg2 =="noArg":
            await bot.say("Invalid input, use `?bank-adjust @user money`.")
        else:
            try:
                currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "rb"))
            except:
                currentMoney = 0
            try:
                currentMoney += int(arg2)
                pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "wb"))
                if int(arg2)>0:
                    giveEmbed = discord.Embed(title="$" + "{:,}".format(int(arg2)) + " given to " + str(bot.get_server(server).get_member(member).display_name) + "'s bank by " + str(ctx.message.author.display_name) + ".", color=0x00FF00)
                elif int(arg2)<0:
                    giveEmbed = discord.Embed(title="$" + str("{:,}".format(abs(int(arg2)))) + " taken from " + str(bot.get_server(server).get_member(member).display_name) + " by " + str(ctx.message.author.display_name) + ".", color=0x00FF00)
                else:
                    giveEmbed = discord.Embed(title="No money given.", color=0x00FF00)
                await bot.say(embed=giveEmbed)
            except TypeError:
                await bot.say('Error, make sure "money" is an integer in `?bank-adjust @user money`.')
            
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')

@bot.command(pass_context=True, aliases=["dep"], description = 'Deposits the money you have. You can deposit a specific amount, or all on hand. Format: "?dep all", or "?dep amount".')
async def deposit(ctx, arg = "noArg"):
    """Deposits the money you have. You can deposit a specific amount, or all on hand. Format: "?dep all", or "?dep amount"."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    try:
        currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        currentMoney = 0
    try:
        currentBank = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "rb"))
    except:
        currentBank = 0
    arg = arg.replace(',', '')
    if arg =="all":
        if currentMoney <= 0:
            await bot.say("You have nothing to deposit.")
        else:
            currentBank += currentMoney
            depEmbed = discord.Embed(title="$" + "{:,}".format(currentMoney) + " deposited!", color = 0x00FF00)
            await bot.say(embed=depEmbed)
            currentMoney = 0
    else:
        try:
            if int(arg) > currentMoney:
                await bot.say("You're not that rich. Deposit what you can.")
            elif int(arg) < 0:
                await bot.say("Use `?with` to withdraw money.")
            else:
                currentBank += int(arg)
                currentMoney -= int(arg)
                depEmbed = discord.Embed(title="$" + "{:,}".format(int(arg)) + " deposited!", color = 0x00FF00)
                await bot.say(embed=depEmbed)
        except TypeError:
           await bot.say("Invalid input, use `?dep amount`.")
    pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
    pickle.dump(currentBank, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "wb"))

@bot.command(pass_context=True, aliases=["with"], description = 'Same as ?dep, but for withdrawing from the bank.')
async def withdraw(ctx, arg = "noArg"):
    """Same as ?dep, but for withdrawing from the bank."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    try:
        currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        currentMoney = 0
    try:
        currentBank = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "rb"))
    except:
        currentBank = 0
    arg = arg.replace(',', '')
    if arg =="all":
        if currentBank <= 0:
            await bot.say("You have nothing in your bank. Sad, really.")
        else:
            currentMoney += currentBank
            withEmbed = discord.Embed(title="$" + "{:,}".format(currentBank) + " withdrawn!", color = 0x00FF00)
            await bot.say(embed=withEmbed)
            currentBank = 0
    else:
        try:
            if int(arg) > currentBank:
                await bot.say("You're not that rich. Withdraw what you have.")
            elif int(arg) < 0:
                await bot.say("Use `?dep` to deposit money.")
            else:
                currentBank -= int(arg)
                currentMoney += int(arg)
                withEmbed = discord.Embed(title="$" + "{:,}".format(int(arg)) + " withdrawn!", color = 0x00FF00)
                await bot.say(embed = withEmbed)
        except TypeError:
           await bot.say("Invalid input, use `?with amount`.")
    pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
    pickle.dump(currentBank, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "wb"))


@bot.command(pass_context=True, description = 'Gives money from your On Hand to someone else. Format: "?give amount @person".')
async def give(ctx, arg2 = "noArg", *theArg : str):
    """Gives money from your On Hand to someone else. Format: "?give amount @person"."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    arg = ""
    for item in theArg:
        arg = arg + item + " "
    arg = arg[:len(arg)-1]
    arg2 = arg2.replace(',', '')
    try:
        giverMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        giverMoney = 0

    try:
        if arg[2] == "!":
            member = arg[3:(len(arg)-1)]

        else:
            member = arg[2:(len(arg)-1)]
    except IndexError:
        member = ""

    if bot.get_server(server).get_member(member) is None:
        findList, findIDList = getUsers(ctx, arg)
        theID = ""
        if len(findIDList)==1:
            theID = findIDList[0]
        elif len(findIDList)==0:
            await bot.say("No users found. Type it correctly next time.")
            return
        else:
            await bot.say("Multiple people found. Pick someone specific next time.")
            userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
            aNum = 0
            for human in findList:
                userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                aNum += 1
            await bot.say(embed=userFindEmbed)
            return
        member = theID
    if bot.get_server(server).get_member(member) is None or arg2 =="noArg":
        await bot.say("Invalid input, use `?give @user money`.")
    else:
        try:
            receiverMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
        except:
            receiverMoney = 0
        if arg2 == "all":
            arg2 = str(giverMoney)
        try:
            if int(arg2)<=0:
                await bot.say("Don't try and exploit this anymore. My master fixed it. Use a positive number.")
                return
            if int(arg2)>giverMoney:
                giveEmbed = discord.Embed(title="You don't have that much. Poor you.", color=0x00FF00)
            else:
                receiverMoney += int(arg2)
                giverMoney -= int(arg2)
                pickle.dump(receiverMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
                pickle.dump(giverMoney, open("servers" + os.sep + str(server) + os.sep + str(ctx.message.author.id) + os.sep + "money.p", "wb"))
                if int(arg2)>0:
                    giveEmbed = discord.Embed(title="$" + "{:,}".format(int(arg2)) + " given to " + str(bot.get_server(server).get_member(member).display_name) + " by " + str(ctx.message.author.display_name) + ". How kind.", color=0x00FF00)
                elif int(arg2)<0:
                    giveEmbed = discord.Embed(title="This isn't robbery. This is giving.", color=0x00FF00)
                else:
                    giveEmbed = discord.Embed(title="Really? Nothing?", color=0x00FF00)
            await bot.say(embed=giveEmbed)
        except TypeError:
            await bot.say('Error, make sure "money" is an integer in `?give @user money`.')


@bot.command(pass_context=True, aliases=["lb", "top", "highscore"], description = 'Displays the server\'s leaderboard. Use "?lb page" for a different page.')
async def leaderboard(ctx, arg="1"):
    """Displays the server\'s leaderboard. Use "?lb page" for a different page."""
    server = ctx.message.server.id
    myMembers = []
    myMoney = []
    for human in ctx.message.server.members:
        try:
            currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(human.id) + os.sep + "money.p", "rb"))
            
        except:
            currentMoney = 0

        try:
            currentBank = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(human.id) + os.sep + "bank.p", "rb"))
        except:
            currentBank = 0
            
        myMembers.append(str(human))
        myMoney.append(int(currentMoney+ currentBank))


    moneyDict = dict(zip(myMembers, myMoney))
    topDict = collections.OrderedDict(sorted(zip(myMembers,myMoney), key=lambda i: i[1], reverse=True))

    orderMembers = []
    orderMoney = []

    for k, v in topDict.items():
        orderMembers.append(k)
        orderMoney.append(v)

    maxPage = math.ceil(len(myMembers)/10)
    if int(arg) > maxPage:
        arg = str(maxPage)
    if int(arg) > 1:
        begIn = (int(arg)*10)-10
        endIn = (int(arg)*10)
        
    else:
        arg = 1
        begIn = 0
        endIn = 10
        
    newMembers = orderMembers[begIn:endIn]
    newMoney = orderMoney[begIn:endIn]
    
    lbEmbed = discord.Embed(title=str(bot.get_server(server))+ " Leaderboard", description="---------------------------------------------", color=0xFF0000)
    x = begIn
    y = 0
    while x <= endIn:
        try:
            lbEmbed.add_field(name= str(x+1) + ": " + str(newMembers[y]) + " | $" + "{:,}".format(newMoney[y]), value=str(x+2) + ": " + str(newMembers[y + 1]) + " | $" + "{:,}".format(newMoney[y + 1]), inline=False)
        except IndexError:
            try:
                lbEmbed.add_field(name= str(x+1) + ": " + str(newMembers[y]) + " | $" + "{:,}".format(newMoney[y]), value="\u200b", inline=False)
            except IndexError:
                break
        x+=2
        y+=2
        
    lbEmbed.set_thumbnail(url=ctx.message.server.icon_url)
    lbEmbed.set_footer(text="Page " + str(arg) + "/" + str(maxPage))
    await bot.say(embed=lbEmbed)

@bot.command(pass_context=True, aliases=["reset-economy", "reset-eco", "reseteco"], description = 'Admin-only. Resets all money in the server. Make sure you want to do this for real.')
async def reseteconomy(ctx, arg = "noArg", arg2 = "noArg"):
    """Admin-only. Resets all money in the server. Make sure you want to do this for real."""
    server = ctx.message.server.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    if ctx.message.author.id in ADMINS:
        if arg == "I_REALLY" and arg2 == "wantToDoThis":
            for member in ctx.message.server.members:
                currentMoney = 0
                currentBank = 0
                try:
                    pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member.id) + os.sep + "money.p", "wb"))
                except:
                    pass
                try:
                    pickle.dump(currentBank, open("servers" + os.sep + str(server) + os.sep + str(member.id) + os.sep + "bank.p", "wb"))
                except:
                    pass
            await bot.say("Done! I am yours to command! *...mostly.*")
        else:
            await bot.say("You sure? This resets *all* money in this server. If you are sure, use `?reset-economy I_REALLY wantToDoThis`.")
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')

@bot.command(pass_context=True, aliases=["give-to-all"],  description = 'Admin-only. Gives a certain amount of money to everyone in the server. Format: "?give-to-all amount".')
async def givetoall(ctx, arg="noArg"):
    """Admin-only. Gives a certain amount of money to everyone in the server. Format: "?give-to-all amount"."""
    server = ctx.message.server.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    errorThing = False
    arg = arg.replace(',', '')
    if ctx.message.author.id in ADMINS:
        for member in ctx.message.server.members:
            try:
                currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member.id) + os.sep + "money.p", "rb"))
                
            except:
                currentMoney = 0


            try:
                currentMoney += int(arg)
            except (TypeError, ValueError):
                await bot.say("Please use a valid sum of money.")
                errorThing = True
                break
                
            try:
                pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member.id) + os.sep + "money.p", "wb"))
            except:
                pass
        if not errorThing:
            await bot.say("Done! Enjoy the money, everyone!")
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')


@bot.command(pass_context=True, aliases=["set-salary", "set-sal", "setsal"], description = 'Admin-only. Sets the salary for a certain role. Format: "?set-salary @role amount".')
async def setsalary(ctx, arg="noArg", arg2 = "noArg"):
    """Admin-only. Sets the salary for a certain role. Format: "?set-salary @role amount"."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    arg2 = arg2.replace(',', '')
    if member in ADMINS:
        if arg[2] == "&":
                role = arg[3:(len(arg)-1)]
        else:
                role = arg[2:(len(arg)-1)]
        if not os.path.exists("servers" + os.sep + str(server) + os.sep + str(role)) or arg2 =="noArg":
            await bot.say("Invalid input, use `?set-salary @role salary`.")
        else:
            try:
                currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(role) + os.sep + "salary.p", "rb"))
            except:
                currentMoney = 0
            try:
                currentMoney = int(arg2)
                pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(role) + os.sep + "salary.p", "wb"))
                await bot.say("Done!")
            except TypeError:
                await bot.say('Error, make sure "salary" is an integer in `?set-salary @role salary`.')
            
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')


        
@bot.command( pass_context=True, aliases=["give-salary", "give-sal", "givesal"], description='Admin-only. Distributes salary, even if it\'s not the right time.')
async def givesalary(ctx):
    """Admin-only. Distributes salary, even if it\'s not the right time."""
    server = ctx.message.server.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    if ctx.message.author.id in ADMINS:
        salEmbed = discord.Embed(title="Salary Pay", color=0x00ff00)
        for role in bot.get_server(server).roles:
            try:
                currentSal = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(role.id) + os.sep + "salary.p", "rb"))
            except:
                currentSal = 0
            if currentSal != 0:
                for member in ctx.message.server.members:
                    for item in member.roles:
                        if item.id == role.id:
                            try:
                                currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member.id) + os.sep + "money.p", "rb"))
                            except:
                                currentMoney = 0
                            currentMoney+=currentSal
                            
                            pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member.id) + os.sep + "money.p", "wb"))
                toSay = str(role) + " got their salary of $" + "{:,}".format(currentSal)
                if toSay[0] == "@":
                    await bot.say(toSay[1:])
                else:
                    await bot.say(toSay)
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')



@bot.command(pass_context=True, aliases=["sal"], description = 'Used to check the salaries of each role in the server. If it\'s $0, it won\'t show.')
async def salary(ctx):
    """Used to check the salaries of each role in the server. If it\'s $0, it won\'t show."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    salEmbed = discord.Embed(title="Role Salaries", color=0x00ff00)
    for role in bot.get_server(server).roles:
        try:
            currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(role.id) + os.sep + "salary.p", "rb"))
        except:
            currentMoney = 0
        if currentMoney != 0:
            salEmbed.add_field(name=str(role), value="$" +"{:,}".format(currentMoney), inline=False)
    salEmbed.add_field(name="Other Roles:", value="$0", inline=False)
    await bot.say(embed=salEmbed)



@bot.command(pass_context=True, aliases=["set-channel", "setchan", "set-chan"], description = 'Admin-only. Sets the channel for bot notifications. Uses the default one by default. Format: "?setchannel #channel".')
async def setchannel(ctx, arg="noArg"):
    """Admin-only. Sets the channel for bot notifications. Uses the default one by default. Format: "?setchannel #channel"."""
    server = ctx.message.server.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    setChannel=False
    if ctx.message.author.id in ADMINS:
        for thing in ctx.message.server.channels:
            if ctx.message.server.get_channel(arg[2:len(arg)-1]) == thing:
                pickle.dump(thing, open("servers" + os.sep + str(server) + os.sep + "channel.p", "wb"))
                await bot.say("Channel Set!")
                setChannel=True
        if not setChannel:
            await bot.say("Error, invalid channel.")
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')

@bot.command(pass_context=True, aliases=["reset-salary", "reset-sal", "resetsal"], description="Admin-only. Resets all of the salaries for the server.")
async def resetsalary(ctx, arg="noArg", arg2="noArg"):
    """Admin-only. Resets all of the salaries for the server"""
    server = ctx.message.server.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    if ctx.message.author.id in ADMINS:
        if arg == "I_REALLY" and arg2 == "wantToDoThis":
            for role in ctx.message.server.roles:
                currentMoney = 0
                try:
                    pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(role.id) + os.sep + "salary.p", "wb"))
                except:
                    pass
                
            await bot.say("Done! I am yours to command! *...mostly.*")
        else:
            await bot.say("You sure? This resets *all* wages in this server. If you are sure, use `?reset-salary I_REALLY wantToDoThis`.")
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')


@bot.command(pass_context=True, aliases=["job"], description = 'Work for a small amount of money. Always succeeds, but only can be done sometimes.')
async def work(ctx):
    """Work for a small amount of money. Always succeeds."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    global WORK
    try:
        currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        currentMoney = 0

    try:
        workCooldown = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "workCooldown.p", "rb"))
    except:
        workCooldown = 0
    try:
        coolWork = pickle.load(open("servers" + os.sep + str(server) + os.sep + "coolWork.p", "rb"))
    except:
        coolWork = 60
        
    try:
        maxWork = pickle.load(open("servers" + os.sep + str(server) + os.sep + "maxWork.p", "rb"))
    except:
        maxWork = 150
    try:
        minWork = pickle.load(open("servers" + os.sep + str(server) + os.sep + "minWork.p", "rb"))
    except:
        minWork = 50

    if workCooldown < 0:
        randomWork = WORK[random.randint(0, len(WORK)-1)]
        randomMoney = random.randint(minWork, maxWork)
        
        workEmbed=discord.Embed(title=str(ctx.message.author) + "'s Work", description=randomWork, color=0x00FF00)
        workEmbed.add_field(name="Earned:", value= "$" + "{:,}".format(randomMoney), inline=True)
        currentMoney += randomMoney
        pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
        await bot.say(embed=workEmbed)
        workCooldown = coolWork
        pickle.dump(workCooldown, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "workCooldown.p", "wb"))
    else:
        await bot.say("Please wait " + "{:,}".format(workCooldown) + " seconds before working again!")

@bot.command(pass_context=True, aliases=["set-work"], description = 'Admin-only. Set max, min, and cooldown values of ?work.')
async def setwork(ctx, myMin ="noArg", myMax="noArg", coolDown = "noArg"):
    """Admin-only. Set max, min, and cooldown values of ?work."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    try:
        maxWork = pickle.load(open("servers" + os.sep + str(server) + os.sep + "maxWork.p", "rb"))
    except:
        maxWork = 150
    try:
        minWork = pickle.load(open("servers" + os.sep + str(server) + os.sep + "minWork.p", "rb"))
    except:
        minWork = 50
    try:
        coolWork = pickle.load(open("servers" + os.sep + str(server) + os.sep + "coolWork.p", "rb"))
    except:
        coolWork = 60
        
    if member in ADMINS:
        if myMin == "noArg" or myMax == "noArg" or coolDown == "noArg":
            workEmbed=discord.Embed(title="Work Settings", description= 'Use "?setwork min max cooldown" to set the values.', color=0x00FF00)
            workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(int(maxWork)), inline=True)
            workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(int(minWork)), inline=True)
            workEmbed.add_field(name="Cooldown:", value="{:,}".format(int(coolWork)) + " Seconds", inline=True)
            await bot.say(embed=workEmbed)
        else:
            try:
                minWork = int(myMin)
                maxWork = int(myMax)
                coolWork = int(coolDown)
                pickle.dump(maxWork, open("servers" + os.sep + str(server) + os.sep + "maxWork.p", "wb"))
                pickle.dump(minWork, open("servers" + os.sep + str(server) + os.sep + "minWork.p", "wb"))
                pickle.dump(coolWork, open("servers" + os.sep + str(server) + os.sep + "coolWork.p", "wb"))
                await bot.say("Done!")
            except TypeError:
                workEmbed=discord.Embed(title="Work Settings", description= 'Use "?setwork min max cooldown" to set the values.', color=0x00FF00)
                workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(int(maxWork)), inline=True)
                workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(int(minWork)), inline=True)
                workEmbed.add_field(name="Cooldown:", value="{:,}".format(int(coolWork)) + " Seconds", inline=True)
                await bot.say(embed=workEmbed)

            
    else:
        workEmbed=discord.Embed(title="Work Settings", description= 'These are the stats for the work command. You\'re not an admin, so this command does nothing else. Sucks for you.', color=0x00FF00)
        workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(int(maxWork)), inline=True)
        workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(int(minWork)), inline=True)
        workEmbed.add_field(name="Cooldown:", value="{:,}".format(int(coolWork)) + " Seconds", inline=True)
        await bot.say(embed=workEmbed)



@bot.command(pass_context=True, description = 'Crime for a large amount of money. Sometimes fails. and you lose money instead.')
async def crime(ctx):
    """Crime for a large amount of money. Sometimes fails. and you lose money instead."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    global CRIMEWIN
    global CRIMELOSE
    try:
        currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        currentMoney = 0
    try:
        currentBank = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "rb"))
    except:
        currentBank = 0

    myMoney = currentBank + currentMoney
    try:
        crimeCooldown = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "crimeCooldown.p", "rb"))
    except:
        crimeCooldown = 0
    try:
        coolCrime = pickle.load(open("servers" + os.sep + str(server) + os.sep + "coolCrime.p", "rb"))
    except:
        coolCrime = 120
    try:
        crimeRate = pickle.load(open("servers" + os.sep + str(server) + os.sep + "crimeRate.p", "rb"))
    except:
        crimeRate = 20
    try:
        maxCrime = pickle.load(open("servers" + os.sep + str(server) + os.sep + "maxCrime.p", "rb"))
    except:
        maxCrime = 1500
    try:
        minCrime = pickle.load(open("servers" + os.sep + str(server) + os.sep + "minCrime.p", "rb"))
    except:
        minCrime = 500

    if crimeCooldown < 0:
        didSucceed=0
        currentChance = random.randint(0, 100)
        if myMoney >=0:
            currentChance += myMoney/1000
        else:
            currentChance -= myMoney/-10
        if currentChance>100:
            currentChance=100
        elif currentChance<0:
            currentChance=0
        
        if currentChance<crimeRate:
            didSucceed=1

        
            
        if didSucceed== 1:
            randomCrime = CRIMEWIN[random.randint(0, len(CRIMEWIN)-1)]
        else:
            randomCrime = CRIMELOSE[random.randint(0, len(CRIMELOSE)-1)]


            
        randomMoney = random.randint(minCrime, maxCrime)
        
        
        if didSucceed==1:
            crimeEmbed=discord.Embed(title=str(ctx.message.author) + "'s Crimes", description=randomCrime, color=0x00FF00)
            crimeEmbed.add_field(name="Earned:", value= "$" + "{:,}".format(randomMoney), inline=True)
            currentMoney += randomMoney
            pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
            await bot.say(embed=crimeEmbed)
        else:
            crimeEmbed=discord.Embed(title=str(ctx.message.author) + "'s Crimes", description=randomCrime, color=0xFF0000)
            crimeEmbed.add_field(name="Lost:", value= "$" + "{:,}".format(randomMoney), inline=True)
            currentMoney -= randomMoney
            pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
            await bot.say(embed=crimeEmbed)

            
        crimeCooldown = coolCrime
        pickle.dump(crimeCooldown, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "crimeCooldown.p", "wb"))
    else:
        await bot.say("Please wait " + "{:,}".format(crimeCooldown) + " seconds before being a criminal again!")

@bot.command(pass_context=True, aliases=["set-crime"], description = 'Admin-only. Set max, min, winrate, and cooldown values of ?crime. Losing = you lose a number between min and max. Winning = gaining that number.')
async def setcrime(ctx, myMin ="noArg", myMax="noArg", winRate = "noArg", coolDown = "noArg"):
    """Admin-only. Set max, min, winrate, and cooldown values of ?crime. Losing = you lose a number between min and max. Winning = gaining that number."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    try:
        maxCrime = pickle.load(open("servers" + os.sep + str(server) + os.sep + "maxCrime.p", "rb"))
    except:
        maxCrime = 1500
    try:
        minCrime = pickle.load(open("servers" + os.sep + str(server) + os.sep + "minCrime.p", "rb"))
    except:
        minCrime = 500
    try:
        crimeRate = pickle.load(open("servers" + os.sep + str(server) + os.sep + "crimeRate.p", "rb"))
    except:
        crimeRate = 20
    try:
        coolCrime = pickle.load(open("servers" + os.sep + str(server) + os.sep + "coolCrime.p", "rb"))
    except:
        coolCrime = 120
        
    if member in ADMINS:
        if myMin == "noArg" or myMax == "noArg" or coolDown == "noArg" or winRate == "noArg":
            workEmbed=discord.Embed(title="Crime Settings", description= 'Use "?setcrime min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.', color=0x00FF00)
            workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(maxCrime), inline=True)
            workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(minCrime), inline=True)
            workEmbed.add_field(name="Crimerate:", value="{:,}".format(crimeRate) + "%", inline=True)
            workEmbed.add_field(name="Cooldown:", value="{:,}".format(coolCrime) + " Seconds", inline=True)
            await bot.say(embed=workEmbed)
        else:
            try:
                minCrime = int(myMin)
                maxCrime = int(myMax)
                crimeRate = int(winRate)
                coolCrime = int(coolDown)
                if crimeRate>99:
                    crimeRate = 99
                elif crimeRate <1:
                    crimeRate = 1
                pickle.dump(maxCrime, open("servers" + os.sep + str(server) + os.sep + "maxCrime.p", "wb"))
                pickle.dump(minCrime, open("servers" + os.sep + str(server) + os.sep + "minCrime.p", "wb"))
                pickle.dump(crimeRate, open("servers" + os.sep + str(server) + os.sep + "crimeRate.p", "wb"))
                pickle.dump(coolCrime, open("servers" + os.sep + str(server) + os.sep + "coolCrime.p", "wb"))
                await bot.say("Done!")
            except TypeError:
                workEmbed=discord.Embed(title="Crime Settings", description= 'Use "?setcrime min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.', color=0x00FF00)
                workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(maxCrime), inline=True)
                workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(minCrime), inline=True)
                workEmbed.add_field(name="Crimerate:", value="{:,}".format(crimeRate) + "%", inline=True)
                workEmbed.add_field(name="Cooldown:", value="{:,}".format(coolCrime) + " Seconds", inline=True)
                await bot.say(embed=workEmbed)

            
    else:
        workEmbed=discord.Embed(title="Crime Settings", description= 'You\'re no admin. Anyway, here\'s the stats.. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.', color=0x00FF00)
        workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(maxCrime), inline=True)
        workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(minCrime), inline=True)
        workEmbed.add_field(name="Crimerate:", value="{:,}".format(crimeRate) + "%", inline=True)
        workEmbed.add_field(name="Cooldown:", value="{:,}".format(coolCrime) + " Seconds", inline=True)
        await bot.say(embed=workEmbed)

@bot.command(pass_context=True, aliases=["steal"], description = 'Rob money from a member\'s On Hand. It may fail, and you\'ll lose instead.')
async def rob(ctx, *theArg : str):
    """Rob money from a member\'s On Hand. It may fail, and you\'ll lose instead."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    arg = ""
    for item in theArg:
        arg = arg + item + " "
    arg = arg[:len(arg)-1]
    global ROBWIN
    global ROBLOSE
    try:
        robberMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        robberMoney = 0
    try:
        currentBank = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "bank.p", "rb"))
    except:
        currentBank = 0
        
    try:
        if arg[2] == "!":
            member = arg[3:(len(arg)-1)]

        else:
            member = arg[2:(len(arg)-1)]
    except IndexError:
        member = ""

    if bot.get_server(server).get_member(member) is None:
        findList, findIDList = getUsers(ctx, arg)
        theID = ""
        if len(findIDList)==1:
            theID = findIDList[0]
        elif len(findIDList)==0:
            await bot.say("No users found. Type it correctly next time.")
            return
        else:
            await bot.say("Multiple people found. Pick someone specific next time.")
            userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
            aNum = 0
            for human in findList:
                userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                aNum += 1
            await bot.say(embed=userFindEmbed)
            return
        member = theID
    if bot.get_server(server).get_member(member) is None:
        await bot.say("Invalid input, use `?rob @user`.")
    else:
        if member == ctx.message.author.id:
            await bot.say("Robbing yourself is a stupid idea. Stop it.")
            return
        try:
            robbedMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
        except:
            robbedMoney = 0

        try:
            robCooldown = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(ctx.message.author.id) + os.sep + "robCooldown.p", "rb"))
        except:
            robCooldown = 0
        try:
            coolRob = pickle.load(open("servers" + os.sep + str(server) + os.sep + "coolRob.p", "rb"))
        except:
            coolRob = 120
        try:
            robRate = pickle.load(open("servers" + os.sep + str(server) + os.sep + "robRate.p", "rb"))
        except:
            robRate = 20
        try:
            maxRob = pickle.load(open("servers" + os.sep + str(server) + os.sep + "maxRob.p", "rb"))
        except:
            maxRob = 1500
        try:
            minRob = pickle.load(open("servers" + os.sep + str(server) + os.sep + "minRob.p", "rb"))
        except:
            minRob = 500

        if robCooldown < 0:
            didSucceed=0
            currentChance = random.randint(0, 100)
            if robberMoney >=0:
                currentChance += (robberMoney+currentBank)/1000
            else:
                currentChance -= (robberMoney+currentBank)/-10
            if currentChance>100:
                currentChance=100
            elif currentChance<0:
                currentChance=0
            if currentChance<robRate:
                didSucceed=1

            
                
            if didSucceed== 1:
                randomRob = ROBWIN[random.randint(0, len(ROBWIN)-1)]
                randomMoney = int((random.randint(75, 95)/100) * robbedMoney)
            else:
                randomRob = ROBLOSE[random.randint(0, len(ROBLOSE)-1)]
                randomMoney = int(random.randint(minRob, maxRob))

                
            
            
            if robbedMoney<=0:
                robEmbed=discord.Embed(title=str(ctx.message.author) + "'s Robbery of " + str(bot.get_server(server).get_member(member)), description="They didn't even have enough money to rob! Idiot.", color=0xFF0000)
                robEmbed.add_field(name="Fined:", value= "$" + "{:,}".format(randomMoney), inline=True)
                robberMoney -= randomMoney
                pickle.dump(robberMoney, open("servers" + os.sep + str(server) + os.sep + str(ctx.message.author.id) + os.sep + "money.p", "wb"))
                await bot.say(embed=robEmbed)
            elif didSucceed==1:
                robEmbed=discord.Embed(title=str(ctx.message.author) + "'s Robbery of " + str(bot.get_server(server).get_member(member)), description=randomRob, color=0x00FF00)
                robEmbed.add_field(name="Stolen:", value= "$" + "{:,}".format(randomMoney), inline=True)
                robberMoney += randomMoney
                robbedMoney -= randomMoney
                pickle.dump(robberMoney, open("servers" + os.sep + str(server) + os.sep + str(ctx.message.author.id) + os.sep + "money.p", "wb"))
                pickle.dump(robbedMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
                await bot.say(embed=robEmbed)
            else:
                robEmbed=discord.Embed(title=str(ctx.message.author) + "'s Robbery of " + str(bot.get_server(server).get_member(member)), description=randomRob, color=0xFF0000)
                robEmbed.add_field(name="Fined:", value= "$" + "{:,}".format(randomMoney), inline=True)
                robberMoney -= randomMoney
                pickle.dump(robberMoney, open("servers" + os.sep + str(server) + os.sep + str(ctx.message.author.id) + os.sep + "money.p", "wb"))
                await bot.say(embed=robEmbed)

                
            robCooldown = coolRob
            pickle.dump(robCooldown, open("servers" + os.sep + str(server) + os.sep + str(ctx.message.author.id) + os.sep + "robCooldown.p", "wb"))
        else:
            await bot.say("Please wait " + "{:,}".format(robCooldown) + " seconds before trying to rob again!")

@bot.command(pass_context=True, aliases=["set-rob", "set-steal", "setsteal"], description = 'Admin-only. Set max, min, winrate, and cooldown values of ?crime. Losing = you lose a number between min and max. Winning = rob around 85% of the person\'s On Hand.')
async def setrob(ctx, myMin ="noArg", myMax="noArg", winRate = "noArg", coolDown = "noArg"):
    """Admin-only. Set max, min, winrate, and cooldown values of ?crime. Losing = you lose a number between min and max. Winning = rob around 85% of the person\'s On Hand."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    try:
        maxRob = pickle.load(open("servers" + os.sep + str(server) + os.sep + "maxRob.p", "rb"))
    except:
        maxRob = 1500
    try:
        minRob = pickle.load(open("servers" + os.sep + str(server) + os.sep + "minRob.p", "rb"))
    except:
        minRob = 500
    try:
        robRate = pickle.load(open("servers" + os.sep + str(server) + os.sep + "robRate.p", "rb"))
    except:
        robRate = 20
    try:
        coolRob = pickle.load(open("servers" + os.sep + str(server) + os.sep + "coolRob.p", "rb"))
    except:
        coolRob = 120
        
    if member in ADMINS:
        if myMin == "noArg" or myMax == "noArg" or coolDown == "noArg" or winRate == "noArg":
            workEmbed=discord.Embed(title="Rob Settings", description= 'Use "?setrob min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.', color=0x00FF00)
            workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(maxRob), inline=True)
            workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(minRob), inline=True)
            workEmbed.add_field(name="Robrate:", value="{:,}".format(robRate) + "%", inline=True)
            workEmbed.add_field(name="Cooldown:", value="{:,}".format(coolRob) + " Seconds", inline=True)
            await bot.say(embed=workEmbed)
        else:
            try:
                minRob = int(myMin)
                maxRob = int(myMax)
                robRate = int(winRate)
                coolRob = int(coolDown)
                if robRate>99:
                    robRate = 99
                elif robRate <1:
                    robRate = 1
                pickle.dump(maxRob, open("servers" + os.sep + str(server) + os.sep + "maxRob.p", "wb"))
                pickle.dump(minRob, open("servers" + os.sep + str(server) + os.sep + "minRob.p", "wb"))
                pickle.dump(robRate, open("servers" + os.sep + str(server) + os.sep + "robRate.p", "wb"))
                pickle.dump(coolRob, open("servers" + os.sep + str(server) + os.sep + "coolRob.p", "wb"))
                await bot.say("Done!")
            except TypeError:
                workEmbed=discord.Embed(title="Rob Settings", description= 'Use "?setrob min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.', color=0x00FF00)
                workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(maxRob), inline=True)
                workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(minRob), inline=True)
                workEmbed.add_field(name="Robrate:", value="{:,}".format(robRate) + "%", inline=True)
                workEmbed.add_field(name="Cooldown:", value="{:,}".format(coolRob) + " Seconds", inline=True)
                await bot.say(embed=workEmbed)

            
    else:
        workEmbed=discord.Embed(title="Rob Settings", description= 'Rob stats! No admin for you, though, so you can\'t do anything with this command. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.', color=0x00FF00)
        workEmbed.add_field(name="Max:", value= "$" + "{:,}".format(maxRob), inline=True)
        workEmbed.add_field(name="Min:", value= "$" + "{:,}".format(minRob), inline=True)
        workEmbed.add_field(name="Robrate:", value="{:,}".format(robRate) + "%", inline=True)
        workEmbed.add_field(name="Cooldown:", value="{:,}".format(coolRob) + " Seconds", inline=True)
        await bot.say(embed=workEmbed)


@bot.command(pass_context=True, aliases=["set-salary-time", "setsaltime", "set-sal-time"], description = 'Admin-only. Sets the salary giving time to what is said. Please use military time. Format: "?set-salary-time hour minute".')
async def setsalarytime(ctx, hour = "noArg", minute = "noArg"):
    """Admin-only. Sets the salary giving time to what is said. Please use military time. Format: "?set-salary-time hour minute"."""
    server = ctx.message.server.id
    ADMINS = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "ADMINS.p", "rb"))
    if ctx.message.author.id in ADMINS:
        try:
            hour = int(hour)
            minute = int(minute)
            if hour < 24 and hour >= 0 and minute <60 and minute >= 0:
                pickle.dump(hour, open("servers" + os.sep + str(server) + os.sep +  "salHour.p", "wb"))
                pickle.dump(minute, open("servers" + os.sep + str(server) + os.sep +  "salMinute.p", "wb"))
                await bot.say("Done!")
            else:
                await bot.say("Please input a valid time! (Military time)")
        except:
            await bot.say("Invalid input! Please use the format `?set-salary-time hour minute`, using military time.")
    else:
        await bot.send_file(ctx.message.channel, 'nopower.gif')


@bot.command(pass_context=True, aliases=["get-salary-time", "getsaltime", "get-sal-time", "saltime", "sal-time"], description = 'This command tells you when the salaries will be given.')
async def getsalarytime(ctx):
    """This command tells you when the salaries will be given."""
    server = ctx.message.server.id
    try:
        salHour = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "salHour.p", "rb"))
        salMinute = pickle.load(open("servers" + os.sep + str(ctx.message.server.id) + os.sep + "salMinute.p", "rb"))
    except:
        salHour = 0
        salMinute = 0
    thePM = "A.M."
    if salHour == 0:
        salHour = 12
    if salHour > 12:
        salHour = salHour-12
        thePM = "P.M."
    if salMinute < 10:
        salMinute = "0" + str(salMinute)
    await bot.say("The salaries will be given at " + str(salHour) + ":" + str(salMinute) + " " + thePM)
        
        

        
##########################################################
#
# 
#Minigames
#
#
#########################################################

#DEBUG ONLY
"""
@bot.command(pass_context=True, description ='Gambling! Double or nothing.')
async def gamble(ctx, arg = "noArg"):
    #Gambling! Double or nothing. ##NOTE: CHANGE BACK TO DOCSTRING IF ENABLED
    server = ctx.message.server.id
    member = ctx.message.author.id
    try:
        currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        currentMoney = 0

    myBet = 0
    if arg == 'all':
        arg = str(currentMoney)
    try:
        myBet = int(arg)
    except:
        await bot.say("Please use the format `?gamble bet`.")
        return
    if myBet > currentMoney:
        await bot.say("You don't even have that much on hand, you poor peasant. Try again when you have money.")
        return
    if myBet <=0:
        await bot.say("That's not enough money to bet.")
        return
      
    didWin = random.randint(0, 1)
    if didWin == 0:
        await bot.say("Oops. You lost $" + arg + ". Maybe you shouldn't gamble so much.")
        currentMoney -= myBet
    else:
        await bot.say("Hey, you doubled the money bet! All luck, so no props to you, but I mean, I guess I'm happy for you? If you forgot how much you bet, it was $"+ arg + ".")
        currentMoney += myBet
    pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
"""

@bot.command(pass_context=True, aliases=["bj"], description ='Blackjack! Use "?bj about" for details.')
async def blackjack(ctx, arg = "noArg"):
    """Blackjack! Use "?bj about" for details."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    arg = arg.replace(',', '')
    bjCards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K"]
    try:
        currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        currentMoney = 0
    try:
        betBJ = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "betBJ.p", "rb"))
    except:
        betBJ = 0
    try:
        playingBJ = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playingBJ.p", "rb"))
    except:
        playingBJ = False
    try:
        playStatus = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playStatusBJ.p", "rb"))
    except:
        playStatus = 0
    try:
        playerCards = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playerCards.p", "rb"))
    except:
        playerCards = []
    try:
        dealerCards = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "dealerCards.p", "rb"))
    except:
        dealerCards = []

    doCalculate = False
    totalCards = 0
    numAces = 0
    firstPlayer = False
    turnNum = 0
        
    if arg == "about":
        bjEmbed = discord.Embed(title="Blackjack Rules", color=0x0000FF)
        bjEmbed.add_field(name = "This is Blackjack! Try and beat the dealer!", value= "Use the format `?bj bet` for your first bet.", inline=False)
        bjEmbed.add_field(name = "Use `?bj hit` to draw another card, and `?bj stand` to end your turn.", value="Also, use `?bj double` to draw one more card and double your bet.", inline=False)
        bjEmbed.add_field(name = "Don't go over 21, or you'll bust and lose!", value="Try and beat the dealer!", inline=False)
        await bot.say(embed=bjEmbed)
        return
    if not playingBJ:    
        myBet = 0
        if arg == 'all':
            arg = str(currentMoney)
        try:
            myBet = int(arg)
        except:
            await bot.say("Please use the format `?bj bet`.")
            return
        if myBet > currentMoney:
            await bot.say("You don't even have that much on hand, you poor peasant. Try again when you have money.")
            return
        if myBet <=0:
            await bot.say("That's not enough money to bet.")
            return
        betBJ = myBet
        currentMoney-=betBJ
        playerCards = []
        dealerCards = []
        playerCards.append(random.choice(bjCards))
        playerCards.append(random.choice(bjCards))
        dealerCards.append(random.choice(bjCards))
        playingBJ = True
        firstPlayer = True
        
        pickle.dump(playerCards, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playerCards.p", "wb"))
        pickle.dump(dealerCards, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "dealerCards.p", "wb"))
        pickle.dump(betBJ, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "betBJ.p", "wb"))
        pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
        playStatus = 0
    else:
        doCalculate = False
        if arg == "hit" or arg == "h":
            playerCards.append(random.choice(bjCards))
            pickle.dump(playerCards, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playerCards.p", "wb"))
        elif arg == "stand" or arg == "s":
            dealDone = False
            turnNum = 0
            while not dealDone:
                totalCards = 0
                numAces = 0
                dealerCards.append(random.choice(bjCards))
                for card in dealerCards:
                    try:
                        card = int(card)
                    except:
                        pass
                    if card == "A":
                        numAces +=1
                        card = 11
                    elif card == "J" or card =="Q" or card=="K":
                        card=10
                    totalCards += card
                while numAces >0 and totalCards>21:
                    totalCards = totalCards - 10
                    numAces -=1
                if totalCards>16:
                    dealDone = True
                turnNum += 1
            doCalculate = True
        elif arg == "double" or arg == "d":
            playerCards.append(random.choice(bjCards))
            pickle.dump(playerCards, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playerCards.p", "wb"))
            dealDone = False
            turnNum = 0
            while not dealDone:
                totalCards = 0
                numAces = 0
                dealerCards.append(random.choice(bjCards))
                for card in dealerCards:
                    try:
                        card = int(card)
                    except:
                        pass
                    if card == "A":
                        numAces +=1
                        card = 11
                    elif card == "J" or card =="Q" or card=="K":
                        card=10
                    totalCards += card
                while numAces >0 and totalCards>21:
                    totalCards = totalCards - 10
                    numAces -=1
                if totalCards>16:
                    dealDone = True
                turnNum += 1
            doCalculate = True
            betBJ = betBJ *2
            currentMoney -= betBJ/2
            pickle.dump(int(currentMoney), open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
        else:
            await bot.say("Game in Progress! Finish it first. If you forget what the game was, here:")
    if not doCalculate:
        for card in dealerCards:
            try:
                card = int(card)
            except:
                pass
            if card == "A":
                numAces +=1
                card = 11
            elif card == "J" or card =="Q" or card=="K":
                card=10
            totalCards += card
    if numAces>0:
        totalDealerCards = "Soft " + str(totalCards)
    elif totalCards>21:
        totalDealerCards = "Bust " + str(totalCards)
        playStatus = 1
    else:
        totalDealerCards = str(totalCards)
    totalDealNum = totalCards
    if turnNum == 1 and totalCards == 21:
        totalDealerCards = "Blackjack"
        playStatus = -3
                   
    totalCards = 0
    numAces = 0
    for card in playerCards:
        try:
            card = int(card)
        except:
            pass
        if card == "A":
            numAces +=1
            card = 11
        elif card == "J" or card =="Q" or card=="K":
            card=10
        totalCards += card
    while numAces >0 and totalCards>21:
        totalCards = totalCards - 10
        numAces -=1

    if numAces>0:
        totalPlayerCards = "Soft " + str(totalCards)
    elif totalCards>21:
        totalPlayerCards = "Bust " + str(totalCards)
        playStatus = -1
    else:
        totalPlayerCards = str(totalCards)

    if firstPlayer and totalCards == 21:
        totalPlayerCards = "Blackjack"
        playStatus = 3

    if totalCards == 21 and totalPlayerCards != "Blackjack":
        dealDone = False
        turnNum = 0
        totalPlayerCards = totalCards
        while not dealDone:
            totalCards = 0
            numAces = 0
            dealerCards.append(random.choice(bjCards))
            for card in dealerCards:
                try:
                    card = int(card)
                except:
                    pass
                if card == "A":
                    numAces +=1
                    card = 11
                elif card == "J" or card =="Q" or card=="K":
                    card=10
                totalCards += card
            while numAces >0 and totalCards>21:
                totalCards = totalCards - 10
                numAces -=1
            if totalCards>16:
                dealDone = True
            turnNum += 1
        doCalculate = True
        if numAces>0:
            totalDealerCards = "Soft " + str(totalCards)
        elif totalCards>21:
            totalDealerCards = "Bust " + str(totalCards)
            playStatus = 1
        else:
            totalDealerCards = str(totalCards)
        totalDealNum = totalCards
        if turnNum == 1 and totalCards == 21:
            totalDealerCards = "Blackjack"
            playStatus = -3
        totalCards = totalPlayerCards

    
    if doCalculate and playStatus == 0:
        if totalDealNum > totalCards:
            playStatus = -1
        elif totalDealNum == totalCards:
            playStatus = 2
        else:
            playStatus = 1

    if playStatus == -3:
        playStatus = -1
    if playStatus == 1:
        bjEmbed=discord.Embed(title=str(ctx.message.author)+"'s Blackjack game", description="Player Wins $" + "{:,}".format(betBJ), color = 0x00FF00)
        currentMoney += 2* betBJ
        pickle.dump(int(currentMoney), open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
        playingBJ = False
    elif playStatus == 3:
        totalCards = 0
        numAces = 0
        dealerCards.append(random.choice(bjCards))
        for card in dealerCards:
            try:
                card = int(card)
            except:
                pass
            if card == "A":
                numAces +=1
                card = 11
            elif card == "J" or card =="Q" or card=="K":
                card=10
            totalCards += card
        while numAces >0 and totalCards>21:
            totalCards = totalCards - 10
            numAces -=1
        if totalCards == 21:
            totalDealerCards = "Blackjack"
        if totalPlayerCards != totalDealerCards:
            bjEmbed=discord.Embed(title=str(ctx.message.author)+"'s Blackjack game", description="Player Wins $" + "{:,}".format(int(1.5 *betBJ)), color = 0x00FF00)
            currentMoney += betBJ + int(1.5*betBJ)
            pickle.dump(int(currentMoney), open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
            playingBJ = False
        else:
            bjEmbed=discord.Embed(title=str(ctx.message.author)+"'s Blackjack game", description="Push, money back", color = 0xFF8000)
            currentMoney += betBJ
            pickle.dump(int(currentMoney), open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
            playingBJ = False
    elif playStatus == -1:
        bjEmbed=discord.Embed(title=str(ctx.message.author)+"'s Blackjack game", description="Player Loses $" + "{:,}".format(betBJ), color = 0xFF0000)
        playingBJ = False
    elif playStatus == 2:
        bjEmbed=discord.Embed(title=str(ctx.message.author)+"'s Blackjack game", description="Push, money back", color = 0xFF8000)
        currentMoney += betBJ
        pickle.dump(int(currentMoney), open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
        playingBJ = False
    else:
        bjEmbed=discord.Embed(title=str(ctx.message.author)+"'s Blackjack game", description="Use `?bj hit` to draw another card, and `?bj stand` to end your turn. Use `?bj double` to double down (draw one card more, and double your bet). This game is for $" + "{:,}".format(betBJ)+".", color = 0x0000FF)
    playerCardString = ""
    for card in playerCards:
        playerCardString = playerCardString + "|"
        playerCardString = playerCardString + str(card)
        playerCardString = playerCardString + "| "
    dealerCardString = ""
    for card in dealerCards:
        dealerCardString = dealerCardString + "|"
        dealerCardString = dealerCardString + str(card)
        dealerCardString = dealerCardString + "| "
    bjEmbed.add_field(name="Player's Hand (" + str(totalPlayerCards) + ")", value = playerCardString, inline=True)
    bjEmbed.add_field(name="Dealer's Hand (" + str(totalDealerCards) + ")", value = dealerCardString, inline=True)
    await bot.say(embed=bjEmbed)
    pickle.dump(playStatus, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playStatusBJ.p", "wb"))
    pickle.dump(playingBJ, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playingBJ.p", "wb"))



@bot.command(pass_context=True, aliases=["rou"], description ='Roulette! Use "?roulette about" for details.')
async def roulette(ctx, bet = "noArg", place = "noArg"):
    """Roulette! Use "?roulette about" for details."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    bet = bet.replace(',', '')
    if bet == "about":
        rouEmbed = discord.Embed(title="Roulette Rules", color=0x0000FF)
        rouEmbed.add_field(name = "This is Roulette! Try and guess what the ball will land on! You have 30 seconds.", value= "Use the format \"?roulette bet guess\".", inline=False)
        rouEmbed.add_field(name = "The ball will land on a number from 0-36, and either red or black.", value="For 1/2 chance payments, you'll get twice your payment back, for 1/3 chance, you get 3 times, etc.", inline=False)
        rouEmbed.add_field(name = "1/2 chance: Evens/Odds, and Red/Black", value="1/3 chance: 1st(1-12), 2nd(13-24), 3rd(25-36)", inline=False)
        rouEmbed.add_field(name = "1/36 chance: Any number from 1-36", value="Make sure \"place\" is either a number from 1-36, 1st/2nd/3rd, red/black, or even/odd.", inline=False)
        await bot.say(embed=rouEmbed)
    
    else:
        try:
            currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
        except:
            currentMoney = 0
        if bet == "all":
            bet = currentMoney
        try:
            bet = int(bet)
        except:
            await bot.say("Invalid input! Use `?roulette bet place`.")

        if bet<=0:
            await bot.say("That's not a bet. Bet greater than 0.")
            return
        

        if bet>currentMoney:
            await bot.say("You're too poor for that bet. Try again.")
            return

        try:
            playingRoulette = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playingRoulette.p", "rb"))
        except:
            playingRoulette = False
            
        if playingRoulette == True:
            await bot.say("You're in the middle of a game of one now. Just wait.")
            return


        isInt = True
        try:
            place = int(place)
        except:
            isInt = False

        if isInt:
            if int(place) >0 and int(place) <=36:
                multiplier = 36
                guessType = "numbers"
                guess = int(place)
            else:
                await bot.say("Invalid input! Make sure `place` is either a number from 1-36, 1st/2nd/3rd, red/black, or even/odd.")
                return
        elif place =="even" or place == "odd":
            multiplier = 2
            guessType = "oddeven"
            guess = place
        elif place == "red" or place == "black":
            multiplier = 2
            guessType = "color"
            guess = place
        elif place == "1st" or place == "2nd" or place == "3rd":
            multiplier = 3
            guessType = "dozen"
            guess = place
        else:
            await bot.say("Invalid input! Make sure `place` is either a number from 1-36, 1st/2nd/3rd, red/black, or even/odd.")
            return

        try:
            rouletteOn = pickle.load(open("servers" + os.sep + str(server) + os.sep +"rouletteOn.p", "rb"))
        except:
            rouletteOn = False
        currentMoney -= bet
        if not rouletteOn:
            pickle.dump(ctx.message.channel, open("servers" + os.sep + str(server) + os.sep + "rouChannel.p", "wb"))

        pickle.dump(bet, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "rouletteBet.p", "wb"))
        pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
        pickle.dump(True, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "playingRoulette.p","wb"))
        pickle.dump(multiplier, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "rouletteMultiplier.p", "wb"))
        pickle.dump(guessType, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "rouletteGuessType.p", "wb"))
        pickle.dump(guess, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "rouletteGuess.p", "wb"))
        pickle.dump(True, open("servers" + os.sep + str(server) + os.sep + "rouletteOn.p", "wb"))
        if rouletteOn == False:
            await bot.say("New roulette game started! Make your bets! You have 30 seconds.")
        else:
            await bot.say("Bet placed!")
            
        










    

@bot.command(pass_context=True, aliases=["triv"], description ='A Trivia Game! Use "?trivia about" for details.')
async def trivia(ctx, arg = "noArg", *theArg : str):
    """A Trivia Game! Use "?trivia about" for details."""
    server = ctx.message.server.id
    member = ctx.message.author.id
    #Pickle Load
    try:
        questionCanGuess = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "questionCanGuess.p", "rb"))
    except:
        questionCanGuess = False

    try:
        rawCorrect = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "rawCorrect.p", "rb"))
    except:
        rawCorrect = "ERROR"
    try:
        correctLoc = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "correctLoc.p", "rb"))
    except:
        correctLoc = 666
    try:
        correctLetter = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "correctLetter.p", "rb"))
    except:
        correctLetter = "F"

    try:
        numCorrect = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numCorrect.p", "rb"))
    except:
        numCorrect = 0
    try:
        numGuessed = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numGuessed.p", "rb"))
    except:
        numGuessed = 0

    try:
        trivCool = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "trivCool.p", "rb"))
    except:
        trivCool = 0

    try:
        currentMoney = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "rb"))
    except:
        currentMoney = False
                                  
    if arg == "about":
        aboutTrivEmbed = discord.Embed(title='This is a trivia game!', color=0x660066)
        aboutTrivEmbed.add_field(name='Use `?trivia q` to have it ask you a question...', value='And after it says *all* possible answers, guess with `?trivia a`, replacing "a" with your guess!', inline=False)
        aboutTrivEmbed.add_field(name="If it's a true/false question, respond with t/f or true/false, depending on your guess!", value='Also, use `?trivia score @User` to get someone\'s score!', inline=False)
        await bot.say(embed=aboutTrivEmbed)
    elif arg == "q" or arg=="question":
        questionTrivEmbed = discord.Embed(title=str(bot.get_server(server).get_member(member)), description="You have 10 seconds.", color=0x00ff33)
        
        if questionCanGuess:
            await bot.say("Guess the previous one first!")
        else:
            rawData = str(urllib.request.urlopen(url).read())
            rawCategory = html_parser.unescape(getInfo(rawData, 'category":"', '","type'))
            rawType = getInfo(rawData, '"type":"', '","difficulty')
            rawDifficulty = getInfo(rawData, '"difficulty":"', '","question"')
            rawQuestion = html_parser.unescape(getInfo(rawData, '"question":"', '","correct_answer"'))
            rawCorrect = html_parser.unescape(getInfo(rawData, '"correct_answer":', ',"incorrect_answers"'))
            rawCorrect = ast.literal_eval(rawCorrect)
            rawIncorrect = html_parser.unescape(getInfo(rawData, '"incorrect_answers":', "}]}'"))
            rawIncorrect = ast.literal_eval(rawIncorrect)
            prettyType = ""
            if rawType == "multiple":
                prettyType = "Multiple Choice (A-D)"
            elif rawType == "boolean":
                prettyType = "T/F"
            #Display info/question:
            questionTrivEmbed.add_field(name="Category", value=rawCategory, inline=True)
            questionTrivEmbed.add_field(name="Difficulty", value=rawDifficulty.capitalize(), inline=True)
            questionTrivEmbed.add_field(name="Type", value=prettyType, inline = True)
            questionTrivEmbed.add_field(name="Question", value= rawQuestion + "\n\n", inline = False)
            questionTrivEmbed.add_field(name="\u200b", value="\u200b", inline = True)
            
            if rawType == 'multiple':
                if type(rawCorrect) is str: #Standard multiple choice
                    #Display Answers
                    correct = random.randint(0, len(rawIncorrect))
                    correctSaid = False
                    correctLoc = -1
                    for x in range(0, len(rawIncorrect)+1):
                        if x == 0:
                            letter = "A"
                        elif x ==1:
                            letter = "B"
                        elif x ==2:
                            letter = "C"
                        elif x ==3:
                            letter = "D"
                        if x == correct:
                            questionTrivEmbed.add_field(name=letter  + ": " + rawCorrect, value='\u200b', inline=False)
                            correct = 100
                            correctSaid = True
                            correctLoc = x+1
                            if x == 0:
                                correctLetter = "A"
                            elif x ==1:
                                correctLetter = "B"
                            elif x ==2:
                                correctLetter = "C"
                            elif x ==3:
                                correctLetter = "D"
                        else:
                            if correctSaid:
                                questionTrivEmbed.add_field(name=letter + ": " + rawIncorrect[x-1], value='\u200b', inline=False)
                            else:
                                questionTrivEmbed.add_field(name=letter  + ": " + rawIncorrect[x], value='\u200b', inline=False)
                    questionCanGuess = True
                else: #Multiple answers possible
                    questionTrivEmbed.add_field(name="Sorry! An error occurred. Please try asking again! Error: -2", value="\u200b", inline=False)
                    questionCanGuess = True
            elif rawType == 'boolean': # True/False
                #Display answers
                questionTrivEmbed.add_field(name="True", value="\u200b", inline=False)
                questionTrivEmbed.add_field(name="False", value="\u200b", inline=False)
                questionCanGuess = True
            else:
                questionTrivEmbed.add_field(name="Sorry! An error occurred. Please try asking again! Error: -1", value="\u200b", inline=False)
                questionCanGuess = True

            #Say Embed
            await bot.say(embed=questionTrivEmbed)
            #Pickle Dump
            pickle.dump(ctx.message.channel, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "trivChannel.p", "wb"))
            pickle.dump(10, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "trivCool.p", "wb"))
            pickle.dump(questionCanGuess, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "questionCanGuess.p", "wb"))
            pickle.dump(rawCorrect, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "rawCorrect.p", "wb"))
            pickle.dump(correctLoc, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "correctLoc.p", "wb"))
            pickle.dump(correctLetter, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "correctLetter.p", "wb"))
                                 
    elif arg =="1" or arg =="2" or arg =="3" or arg =="4" or arg =="a" or arg =="b" or arg =="c" or arg =="d":     
        if questionCanGuess:
            guess = arg
            if guess == "a":
                guess = "1"
            elif guess == "b":
                guess = "2"
            elif guess == "c":
                guess = "3"
            elif guess == "d":
                guess = "4"
            else:
                guess = "1"
                
            guess = int(guess)
            if guess == correctLoc:
                await bot.say("Correct! You got $75!")
                currentMoney += 75
                pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
                numCorrect += 1
                numGuessed += 1
                
            else:
                await bot.say("Wrong! The right answer was: ***" + correctLetter + "***: *" + rawCorrect + "*")
                numGuessed += 1
                                 
            questionCanGuess = False
            #Pickle Dump
            pickle.dump(questionCanGuess, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "questionCanGuess.p", "wb"))
            pickle.dump(numCorrect, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numCorrect.p", "wb"))
            pickle.dump(numGuessed, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numGuessed.p", "wb"))
        else:
            await bot.say("Hey, hold on! Ask a question first! (Or if you did, wait for *all* answers to appear).")
    elif arg =="t" or arg =="f" or arg =="true" or arg == "false":
        if questionCanGuess:
            guess = arg
            if guess == "t" or guess == "true":
                guess = "true"
            else:
                guess = "false"
            #Determine if user is right
            if guess == rawCorrect.lower():
                await bot.say("Correct! You got $50!")
                currentMoney += 50
                pickle.dump(currentMoney, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "money.p", "wb"))
                numCorrect += 1
                numGuessed += 1
            else:
                await bot.say("Wrong!")
                numGuessed += 1
            questionCanGuess = False
            #Pickle Dump
            pickle.dump(questionCanGuess, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "questionCanGuess.p", "wb"))
            pickle.dump(numCorrect, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numCorrect.p", "wb"))
            pickle.dump(numGuessed, open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numGuessed.p", "wb"))
        else:
            await bot.say("Hey, hold on! Ask a question first! (Or if you did, wait for *all* answers to appear).")
    elif arg == "score":
        arg2 = ""
        for item in theArg:
            arg2 = arg2 + item + " "
        arg2 = arg2[:len(arg2)-1]
        if arg2 != "":
            try:
                if arg2[2] == "!":
                    member = arg2[3:(len(arg2)-1)]
                else:
                    member = arg2[2:(len(arg2)-1)]
            except IndexError:
                member = ""
                
        if bot.get_server(server).get_member(member) is None:
            findList, findIDList = getUsers(ctx, arg2)
            theID = ""
            if len(findIDList)==1:
                theID = findIDList[0]
            elif len(findIDList)==0:
                await bot.say("No users found. Type it correctly next time.")
                return
            else:
                await bot.say("Multiple people found. Pick someone specific next time.")
                userFindEmbed=discord.Embed(title="Users Found:", color= 0xFF7700)
                aNum = 0
                for human in findList:
                    userFindEmbed.add_field(name="#" + str(aNum + 1) + ":", value=human, inline=True)
                    aNum += 1
                await bot.say(embed=userFindEmbed)
                return
            member = theID
        if bot.get_server(server).get_member(member) is None:
            await bot.say("Not a valid user, please try again.")
        else:
            try:
                numCorrect = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numCorrect.p", "rb"))
            except:
                numCorrect = 0
            try:
                numGuessed = pickle.load(open("servers" + os.sep + str(server) + os.sep + str(member) + os.sep + "numGuessed.p", "rb"))
            except:
                numGuessed = 0
            scoreTrivEmbed = discord.Embed(title=str(bot.get_server(server).get_member(member)), color=0x000099)
            scoreTrivEmbed.add_field(name="# Correct: ", value="{:,}".format(numCorrect), inline=True)
            scoreTrivEmbed.add_field(name="# Guessed: ", value="{:,}".format(numGuessed), inline=True)
            if numGuessed !=0:
                scoreTrivEmbed.add_field(name="Percentage: ", value=str(int((numCorrect/numGuessed)*100)) + "%", inline=True)
            await bot.say(embed=scoreTrivEmbed)
    else:
        await bot.say("Sorry! That's not a valid trivia command! Try `?trivia about` for more info!")




bot.loop.create_task(background_task())
bot.run(pickle.load(open("token.p", "rb")))
