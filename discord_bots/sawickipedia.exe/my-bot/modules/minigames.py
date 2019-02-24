#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os  
import pickle
import random
import html.parser
import math
import ast
import urllib.request


class Minigames(commands.Cog)):
    def __init__(self, bot):
        self.bot = bot
        self.trivURL = 'https://opentdb.com/api.php?amount=1'
        self.html_parser = html.parser.HTMLParser()

    def findWord(self, string, sub, listindex=[], offset=0):
        listindex = []
        i = string.find(sub, offset)
        while i >= 0:
            listindex.append(i)
            i = string.find(sub, i + 1)
        return listindex[0]

    def getInfo(self, url, start, end):
        begIn = self.findWord(url, start) + len(start)
        endIn = self.findWord(url, end)
        return url[begIn:endIn]

    def getUsers(self, ctx, arg='noArg'):
        userList = []
        userIDList = []
        userNickList = []
        #Creates lists
        for person in ctx.guild.members:
            userList.append(person)
            userIDList.append(person.id)
            try:
                if len(person.display_name) > 0:
                    userNickList.append(person.display_name)
                else:
                    userNickList.append(person)
            except:
                userNickList.append(person)
        findList = []
        findIDList = []
        pos = 0
        #Finds user
        for thing in userList:
            if str(thing).lower().startswith(arg.lower()):
                findList.append(str(thing)) 
                findIDList.append(userIDList[pos])
            pos += 1
        pos = 0
        for thing in userNickList:
            if str(thing).lower().startswith(arg.lower()) and (str(userList[pos]) not in findList):
                findList.append(str(userList[pos]))
                findIDList.append(userIDList[pos])
            pos += 1
        return (findList, findIDList)

    @commands.command(aliases=['bj'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def blackjack(self, ctx, arg='noArg'):
        'Blackjack! Use "?bj about" for details.'
        guild = ctx.guild.id
        member = ctx.author.id
        arg = arg.replace(',', '')
        bjCards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K']
        try:
            currentMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            currentMoney = 0
        try:
            betBJ = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'betBJ.p', 'rb'))
        except:
            betBJ = 0
        try:
            playingBJ = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playingBJ.p', 'rb'))
        except:
            playingBJ = False
        try:
            playStatus = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playStatusBJ.p',
                     'rb'))
        except:
            playStatus = 0
        try:
            playerCards = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playerCards.p', 'rb'))
        except:
            playerCards = []
        try:
            dealerCards = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'dealerCards.p', 'rb'))
        except:
            dealerCards = []
        doCalculate = False
        totalCards = 0
        numAces = 0
        firstPlayer = False
        turnNum = 0
        if arg == 'about':
            bjEmbed = discord.Embed(title='Blackjack Rules', color=255)
            bjEmbed.add_field(
                name='This is Blackjack! Try and beat the dealer!',
                value='Use the format `?bj bet` for your first bet.',
                inline=False)
            bjEmbed.add_field(
                name='Use `?bj hit` to draw another card, and `?bj stand` to end your turn.',
                value='Also, use `?bj double` to draw one more card and double your bet.',
                inline=False)
            bjEmbed.add_field(
                name="Don't go over 21, or you'll bust and lose!", value='Try and beat the dealer!', inline=False)
            await ctx.send(embed=bjEmbed)
            return
        if (not playingBJ):
            myBet = 0
            if arg == 'all':
                arg = str(currentMoney)
            try:
                myBet = int(arg)
            except:
                await ctx.send('Please use the format `?bj bet`.')
                return
            if myBet > currentMoney:
                await ctx.send("You don't even have that much on hand, you poor peasant. Try again when you have money."
                               )
                return
            if myBet <= 0:
                await ctx.send("That's not enough money to bet.")
                return
            betBJ = myBet
            currentMoney -= betBJ
            playerCards = []
            dealerCards = []
            playerCards.append(random.choice(bjCards))
            playerCards.append(random.choice(bjCards))
            dealerCards.append(random.choice(bjCards))
            playingBJ = True
            firstPlayer = True
            pickle.dump(
                playerCards,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playerCards.p', 'wb'))
            pickle.dump(
                dealerCards,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'dealerCards.p', 'wb'))
            pickle.dump(
                betBJ, open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'betBJ.p',
                            'wb'))
            pickle.dump(
                currentMoney,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
            playStatus = 0
        else:
            doCalculate = False
            if (arg == 'hit') or (arg == 'h'):
                playerCards.append(random.choice(bjCards))
                pickle.dump(
                    playerCards,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playerCards.p',
                         'wb'))
            elif (arg == 'stand') or (arg == 's'):
                dealDone = False
                turnNum = 0
                while (not dealDone):
                    totalCards = 0
                    numAces = 0
                    dealerCards.append(random.choice(bjCards))
                    for card in dealerCards:
                        try:
                            card = int(card)
                        except:
                            pass
                        if card == 'A':
                            numAces += 1
                            card = 11
                        elif (card == 'J') or (card == 'Q') or (card == 'K'):
                            card = 10
                        totalCards += card
                    while (numAces > 0) and (totalCards > 21):
                        totalCards = totalCards - 10
                        numAces -= 1
                    if totalCards > 16:
                        dealDone = True
                    turnNum += 1
                doCalculate = True
            elif (arg == 'double') or (arg == 'd'):
                playerCards.append(random.choice(bjCards))
                pickle.dump(
                    playerCards,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playerCards.p',
                         'wb'))
                dealDone = False
                turnNum = 0
                while (not dealDone):
                    totalCards = 0
                    numAces = 0
                    dealerCards.append(random.choice(bjCards))
                    for card in dealerCards:
                        try:
                            card = int(card)
                        except:
                            pass
                        if card == 'A':
                            numAces += 1
                            card = 11
                        elif (card == 'J') or (card == 'Q') or (card == 'K'):
                            card = 10
                        totalCards += card
                    while (numAces > 0) and (totalCards > 21):
                        totalCards = totalCards - 10
                        numAces -= 1
                    if totalCards > 16:
                        dealDone = True
                    turnNum += 1
                doCalculate = True
                betBJ = betBJ * 2
                currentMoney -= betBJ / 2
                pickle.dump(
                    int(currentMoney),
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
            else:
                await ctx.send('Game in Progress! Finish it first. If you forget what the game was, here:')
        if (not doCalculate):
            for card in dealerCards:
                try:
                    card = int(card)
                except:
                    pass
                if card == 'A':
                    numAces += 1
                    card = 11
                elif (card == 'J') or (card == 'Q') or (card == 'K'):
                    card = 10
                totalCards += card
        if numAces > 0:
            totalDealerCards = 'Soft ' + str(totalCards)
        elif totalCards > 21:
            totalDealerCards = 'Bust ' + str(totalCards)
            playStatus = 1
        else:
            totalDealerCards = str(totalCards)
        totalDealNum = totalCards
        if (turnNum == 1) and (totalCards == 21):
            totalDealerCards = 'Blackjack'
            playStatus = (-3)
        totalCards = 0
        numAces = 0
        for card in playerCards:
            try:
                card = int(card)
            except:
                pass
            if card == 'A':
                numAces += 1
                card = 11
            elif (card == 'J') or (card == 'Q') or (card == 'K'):
                card = 10
            totalCards += card
        while (numAces > 0) and (totalCards > 21):
            totalCards = totalCards - 10
            numAces -= 1
        if numAces > 0:
            totalPlayerCards = 'Soft ' + str(totalCards)
        elif totalCards > 21:
            totalPlayerCards = 'Bust ' + str(totalCards)
            playStatus = (-1)
        else:
            totalPlayerCards = str(totalCards)
        if firstPlayer and (totalCards == 21):
            totalPlayerCards = 'Blackjack'
            playStatus = 3
        if (totalCards == 21) and (totalPlayerCards != 'Blackjack'):
            dealDone = False
            turnNum = 0
            totalPlayerCards = totalCards
            while (not dealDone):
                totalCards = 0
                numAces = 0
                dealerCards.append(random.choice(bjCards))
                for card in dealerCards:
                    try:
                        card = int(card)
                    except:
                        pass
                    if card == 'A':
                        numAces += 1
                        card = 11
                    elif (card == 'J') or (card == 'Q') or (card == 'K'):
                        card = 10
                    totalCards += card
                while (numAces > 0) and (totalCards > 21):
                    totalCards = totalCards - 10
                    numAces -= 1
                if totalCards > 16:
                    dealDone = True
                turnNum += 1
            doCalculate = True
            if numAces > 0:
                totalDealerCards = 'Soft ' + str(totalCards)
            elif totalCards > 21:
                totalDealerCards = 'Bust ' + str(totalCards)
                playStatus = 1
            else:
                totalDealerCards = str(totalCards)
            totalDealNum = totalCards
            if (turnNum == 1) and (totalCards == 21):
                totalDealerCards = 'Blackjack'
                playStatus = (-3)
            totalCards = totalPlayerCards
        if doCalculate and (playStatus == 0):
            if totalDealNum > totalCards:
                playStatus = (-1)
            elif totalDealNum == totalCards:
                playStatus = 2
            else:
                playStatus = 1
        if playStatus == (-3):
            playStatus = (-1)
        if playStatus == 1:
            bjEmbed = discord.Embed(
                title=str(ctx.author) + "'s Blackjack game",
                description='Player Wins $' + '{:,}'.format(betBJ),
                color=65280)
            currentMoney += 2 * betBJ
            pickle.dump(
                int(currentMoney),
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
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
                if card == 'A':
                    numAces += 1
                    card = 11
                elif (card == 'J') or (card == 'Q') or (card == 'K'):
                    card = 10
                totalCards += card
            while (numAces > 0) and (totalCards > 21):
                totalCards = totalCards - 10
                numAces -= 1
            if totalCards == 21:
                totalDealerCards = 'Blackjack'
            if totalPlayerCards != totalDealerCards:
                bjEmbed = discord.Embed(
                    title=str(ctx.author) + "'s Blackjack game",
                    description='Player Wins $' + '{:,}'.format(int(1.5 * betBJ)),
                    color=65280)
                currentMoney += betBJ + int(1.5 * betBJ)
                pickle.dump(
                    int(currentMoney),
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
                playingBJ = False
            else:
                bjEmbed = discord.Embed(
                    title=str(ctx.author) + "'s Blackjack game", description='Push, money back', color=16744448)
                currentMoney += betBJ
                pickle.dump(
                    int(currentMoney),
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
                playingBJ = False
        elif playStatus == (-1):
            bjEmbed = discord.Embed(
                title=str(ctx.author) + "'s Blackjack game",
                description='Player Loses $' + '{:,}'.format(betBJ),
                color=16711680)
            playingBJ = False
        elif playStatus == 2:
            bjEmbed = discord.Embed(
                title=str(ctx.author) + "'s Blackjack game", description='Push, money back', color=16744448)
            currentMoney += betBJ
            pickle.dump(
                int(currentMoney),
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
            playingBJ = False
        else:
            bjEmbed = discord.Embed(
                title=str(ctx.author) + "'s Blackjack game",
                description=
                ('Use `?bj hit` to draw another card, and `?bj stand` to end your turn. Use `?bj double` to double down (draw one card more, and double your bet). This game is for $'
                 + '{:,}'.format(betBJ)) + '.',
                color=255)
        playerCardString = ''
        for card in playerCards:
            playerCardString = playerCardString + '|'
            playerCardString = playerCardString + str(card)
            playerCardString = playerCardString + '| '
        dealerCardString = ''
        for card in dealerCards:
            dealerCardString = dealerCardString + '|'
            dealerCardString = dealerCardString + str(card)
            dealerCardString = dealerCardString + '| '
        bjEmbed.add_field(name=("Player's Hand (" + str(totalPlayerCards)) + ')', value=playerCardString, inline=True)
        bjEmbed.add_field(name=("Dealer's Hand (" + str(totalDealerCards)) + ')', value=dealerCardString, inline=True)
        await ctx.send(embed=bjEmbed)
        pickle.dump(
            playStatus,
            open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playStatusBJ.p', 'wb'))
        pickle.dump(
            playingBJ,
            open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playingBJ.p', 'wb'))

    @commands.command(aliases=['rou'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roulette(self, ctx, bet='noArg', place='noArg'):
        'Roulette! Use "?roulette about" for details.'
        guild = ctx.guild.id
        member = ctx.author.id
        bet = bet.replace(',', '')
        if bet == 'about':
            rouEmbed = discord.Embed(title='Roulette Rules', color=255)
            rouEmbed.add_field(
                name='This is Roulette! Try and guess what the ball will land on! You have 30 seconds.',
                value='Use the format "?roulette bet guess".',
                inline=False)
            rouEmbed.add_field(
                name='The ball will land on a number from 0-36, and either red or black.',
                value=
                "For 1/2 chance payments, you'll get twice your payment back, for 1/3 chance, you get 3 times, etc.",
                inline=False)
            rouEmbed.add_field(
                name='1/2 chance: Evens/Odds, and Red/Black',
                value='1/3 chance: 1st(1-12), 2nd(13-24), 3rd(25-36)',
                inline=False)
            rouEmbed.add_field(
                name='1/36 chance: Any number from 1-36',
                value='Make sure "place" is either a number from 1-36, 1st/2nd/3rd, red/black, or even/odd.',
                inline=False)
            await ctx.send(embed=rouEmbed)
        else:
            try:
                currentMoney = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
            except:
                currentMoney = 0
            if bet == 'all':
                bet = currentMoney
            try:
                bet = int(bet)
            except:
                await ctx.send('Invalid input! Use `?roulette bet place`.')
            if bet <= 0:
                await ctx.send("That's not a bet. Bet greater than 0.")
                return
            if bet > currentMoney:
                await ctx.send("You're too poor for that bet. Try again.")
                return
            try:
                playingRoulette = pickle.load(
                    open(
                        ((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playingRoulette.p',
                        'rb'))
            except:
                playingRoulette = False
            if playingRoulette == True:
                await ctx.send("You're in the middle of a game of one now. Just wait.")
                return
            isInt = True
            try:
                place = int(place)
            except:
                isInt = False
            if isInt:
                if (int(place) > 0) and (int(place) <= 36):
                    multiplier = 36
                    guessType = 'numbers'
                    guess = int(place)
                else:
                    await ctx.send(
                        'Invalid input! Make sure `place` is either a number from 1-36, 1st/2nd/3rd, red/black, or even/odd.'
                    )
                    return
            elif (place == 'even') or (place == 'odd'):
                multiplier = 2
                guessType = 'oddeven'
                guess = place
            elif (place == 'red') or (place == 'black'):
                multiplier = 2
                guessType = 'color'
                guess = place
            elif (place == '1st') or (place == '2nd') or (place == '3rd'):
                multiplier = 3
                guessType = 'dozen'
                guess = place
            else:
                await ctx.send(
                    'Invalid input! Make sure `place` is either a number from 1-36, 1st/2nd/3rd, red/black, or even/odd.'
                )
                return
            try:
                rouletteOn = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'rouletteOn.p', 'rb'))
            except:
                rouletteOn = False
            currentMoney -= bet
            if (not rouletteOn):
                pickle.dump(ctx.channel.id, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'rouChannel.p', 'wb'))
            pickle.dump(
                bet,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'rouletteBet.p', 'wb'))
            pickle.dump(
                currentMoney,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
            pickle.dump(
                True,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'playingRoulette.p',
                     'wb'))
            pickle.dump(
                multiplier,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'rouletteMultiplier.p',
                     'wb'))
            pickle.dump(
                guessType,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'rouletteGuessType.p',
                     'wb'))
            pickle.dump(
                guess,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'rouletteGuess.p',
                     'wb'))
            pickle.dump(True, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'rouletteOn.p', 'wb'))
            if rouletteOn == False:
                await ctx.send('New roulette game started! Make your bets! You have 30 seconds.')
            else:
                await ctx.send('Bet placed!')

    @commands.command(aliases=['triv'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def trivia(self, ctx, arg='noArg', *user: str):
        'A Trivia Game! Use "?trivia about" for details.'
        guild = ctx.guild.id
        member = ctx.author.id
        try:
            questionCanGuess = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'questionCanGuess.p',
                     'rb'))
        except:
            questionCanGuess = False
        try:
            rawCorrect = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'rawCorrect.p', 'rb'))
        except:
            rawCorrect = 'ERROR'
        try:
            correctLoc = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'correctLoc.p', 'rb'))
        except:
            correctLoc = 666
        try:
            correctLetter = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'correctLetter.p',
                     'rb'))
        except:
            correctLetter = 'F'
        try:
            numCorrect = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numCorrect.p', 'rb'))
        except:
            numCorrect = 0
        try:
            numGuessed = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numGuessed.p', 'rb'))
        except:
            numGuessed = 0
        try:
            trivCool = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'trivCool.p', 'rb'))
        except:
            trivCool = 0
        try:
            currentMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            currentMoney = False
        if arg == 'about':
            aboutTrivEmbed = discord.Embed(title='This is a trivia game!', color=6684774)
            aboutTrivEmbed.add_field(
                name='Use `?trivia q` to have it ask you a question...',
                value='And after it says *all* possible answers, guess with `?trivia a`, replacing "a" with your guess!',
                inline=False)
            aboutTrivEmbed.add_field(
                name="If it's a true/false question, respond with t/f or true/false, depending on your guess!",
                value="Also, use `?trivia score @User` to get someone's score!",
                inline=False)
            await ctx.send(embed=aboutTrivEmbed)
        elif (arg == 'q') or (arg == 'question'):
            questionTrivEmbed = discord.Embed(
                title=str(self.bot.get_guild(guild).get_member(member)),
                description='You have 10 seconds.',
                color=65331)
            if questionCanGuess:
                await ctx.send('Guess the previous one first!')
            else:
                rawData = str(urllib.request.urlopen(self.trivURL).read())
                rawCategory = self.html_parser.unescape(self.getInfo(rawData, 'category":"', '","type'))
                rawType = self.getInfo(rawData, '"type":"', '","difficulty')  
                rawDifficulty = self.getInfo(rawData, '"difficulty":"', '","question"')
                rawQuestion = self.html_parser.unescape(self.getInfo(rawData, '"question":"', '","correct_answer"'))
                rawCorrect = self.html_parser.unescape(
                    self.getInfo(rawData, '"correct_answer":', ',"incorrect_answers"'))
                rawCorrect = ast.literal_eval(rawCorrect)
                rawIncorrect = self.html_parser.unescape(self.getInfo(rawData, '"incorrect_answers":', "}]}'"))
                rawIncorrect = ast.literal_eval(rawIncorrect)
                prettyType = ''
                if rawType == 'multiple':
                    prettyType = 'Multiple Choice (A-D)'
                elif rawType == 'boolean':
                    prettyType = 'T/F'
                questionTrivEmbed.add_field(name='Category', value=rawCategory, inline=True)
                questionTrivEmbed.add_field(name='Difficulty', value=rawDifficulty.capitalize(), inline=True)
                questionTrivEmbed.add_field(name='Type', value=prettyType, inline=True)
                questionTrivEmbed.add_field(name='Question', value=rawQuestion + '\n\n', inline=False)
                questionTrivEmbed.add_field(name='\u200b', value='\u200b', inline=True)
                if rawType == 'multiple':
                    if type(rawCorrect) is str:
                        correct = random.randint(0, len(rawIncorrect))
                        correctSaid = False
                        correctLoc = (-1)
                        for x in range(0, len(rawIncorrect) + 1):
                            if x == 0:
                                letter = 'A'
                            elif x == 1:
                                letter = 'B'
                            elif x == 2:
                                letter = 'C'
                            elif x == 3:
                                letter = 'D'
                            if x == correct:
                                questionTrivEmbed.add_field(
                                    name=(letter + ': ') + rawCorrect, value='\u200b', inline=False)
                                correct = 100
                                correctSaid = True
                                correctLoc = x + 1
                                if x == 0:
                                    correctLetter = 'A'
                                elif x == 1:
                                    correctLetter = 'B'
                                elif x == 2:
                                    correctLetter = 'C'
                                elif x == 3:
                                    correctLetter = 'D'
                            elif correctSaid:
                                questionTrivEmbed.add_field(
                                    name=(letter + ': ') + rawIncorrect[x - 1], value='\u200b', inline=False)
                            else:
                                questionTrivEmbed.add_field(
                                    name=(letter + ': ') + rawIncorrect[x], value='\u200b', inline=False)
                        questionCanGuess = True
                    else:
                        questionTrivEmbed.add_field(
                            name='Sorry! An error occurred. Please try asking again! Error: -2',
                            value='\u200b',
                            inline=False)
                        questionCanGuess = True
                elif rawType == 'boolean':
                    questionTrivEmbed.add_field(name='True', value='\u200b', inline=False)
                    questionTrivEmbed.add_field(name='False', value='\u200b', inline=False)
                    questionCanGuess = True
                else:
                    questionTrivEmbed.add_field(
                        name='Sorry! An error occurred. Please try asking again! Error: -1',
                        value='\u200b',
                        inline=False)
                    questionCanGuess = True
                await ctx.send(embed=questionTrivEmbed)
                pickle.dump(ctx.channel.id,open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'trivChannel.p','wb'))
                pickle.dump(10,open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'trivCool.p','wb'))
                pickle.dump(questionCanGuess,open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'questionCanGuess.p','wb'))
                pickle.dump(rawCorrect, open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'rawCorrect.p','wb')) 
                pickle.dump(correctLoc, open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'correctLoc.p','wb'))
                pickle.dump(correctLetter, open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'correctLetter.p','wb'))
        elif (arg == '1') or (arg == '2') or (arg == '3') or (arg == '4') or (arg == 'a') or (arg == 'b') or (
                arg == 'c') or (arg == 'd'):
            if questionCanGuess:
                guess = arg
                if guess == 'a':
                    guess = '1'
                elif guess == 'b': 
                    guess = '2'  
                elif guess == 'c':
                    guess = '3'
                elif guess == 'd':
                    guess = '4'
                else:
                    guess = '1'
                guess = int(guess)
                if guess == correctLoc:
                    await ctx.send('Correct! You got $75!')
                    currentMoney += 75
                    pickle.dump(currentMoney,open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p','wb'))
                    numCorrect += 1
                    numGuessed += 1
                else:
                    await ctx.send(((('Wrong! The right answer was: ***' + correctLetter) + '***: *') + rawCorrect) + '*')
                    numGuessed += 1
                questionCanGuess = False
                pickle.dump(questionCanGuess,open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'questionCanGuess.p','wb'))
                pickle.dump( numCorrect,open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numCorrect.p','wb'))
                pickle.dump(numGuessed,open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numGuessed.p','wb'))
            else:
                await ctx.send('Hey, hold on! Ask a question first! (Or if you did, wait for *all* answers to appear).')
        elif (arg == 't') or (arg == 'f') or (arg == 'true') or (arg == 'false'):
            if questionCanGuess:
                guess = arg
                if (guess == 't') or (guess == 'true'):
                    guess = 'true'
                else:
                    guess = 'false'
                if guess == rawCorrect.lower():
                    await ctx.send('Correct! You got $50!')
                    currentMoney += 50  
                    pickle.dump(
                        currentMoney,
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p',
                             'wb'))
                    numCorrect += 1
                    numGuessed += 1  
                else:
                    await ctx.send('Wrong!')
                    numGuessed += 1
                questionCanGuess = False
                pickle.dump(
                    questionCanGuess,
                    open(((((
                        ('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'questionCanGuess.p',
                         'wb'))
                pickle.dump(
                    numCorrect,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numCorrect.p',
                         'wb'))
                pickle.dump(
                    numGuessed,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numGuessed.p',
                         'wb'))
            else:
                await ctx.send('Hey, hold on! Ask a question first! (Or if you did, wait for *all* answers to appear).'
                               )  
        elif arg == 'score':
            arg2 = '' 
            for item in user:
                arg2 = (arg2 + item) + ' '
            arg2 = arg2[:len(arg2) - 1]
            if arg2 != '':
                try:
                    if arg2[2] == '!':
                        member = int(arg2[3:len(arg2) - 1])
                    else:
                        member = int(arg2[2:len(arg2) - 1])
                except:
                    member = ''
            if self.bot.get_guild(guild).get_member(member) is None:
                (findList, findIDList) = self.getUsers(ctx, arg2)
                theID = ''
                if len(findIDList) == 1:
                    theID = findIDList[0]
                elif len(findIDList) == 0:
                    await ctx.send('No users found. Type it correctly next time.')
                    return
                else:
                    await ctx.send('Multiple people found. Pick someone specific next time.')
                    userFindEmbed = discord.Embed(title='Users Found:', color=16742144)
                    aNum = 0
                    for human in findList:
                        userFindEmbed.add_field(name=('#' + str(aNum + 1)) + ':', value=human, inline=True)
                        aNum += 1
                    await ctx.send(embed=userFindEmbed)
                    return
                member = theID
            if self.bot.get_guild(guild).get_member(member) is None:
                await ctx.send('Not a valid user, please try again.')
            else:
                try:
                    numCorrect = pickle.load(
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numCorrect.p',
                             'rb'))
                except:  
                    numCorrect = 0
                try:
                    numGuessed = pickle.load(
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'numGuessed.p',
                             'rb'))
                except:
                    numGuessed = 0
                scoreTrivEmbed = discord.Embed(title=str(self.bot.get_guild(guild).get_member(member)), color=153)
                scoreTrivEmbed.add_field(name='# Correct: ', value='{:,}'.format(numCorrect), inline=True)
                scoreTrivEmbed.add_field(name='# Guessed: ', value='{:,}'.format(numGuessed), inline=True)
                if numGuessed != 0:
                    scoreTrivEmbed.add_field(
                        name='Percentage: ', value=str(int((numCorrect / numGuessed) * 100)) + '%', inline=True)
                await ctx.send(embed=scoreTrivEmbed)
        else:
            await ctx.send("Sorry! That's not a valid trivia command! Try `?trivia about` for more info!"
                           )  


def setup(bot):
    bot.add_cog(Minigames(bot))
