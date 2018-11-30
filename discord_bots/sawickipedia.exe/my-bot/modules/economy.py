#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import os  
import pickle
import collections
import math
import random
WORK = ['You did a job.', 'You work for Bill Gates for 10 seconds.', 'You make an app, and sell it on the app store.','Your YouTube channel ad revenue comes in.', 'You work as a teacher.','You sell your soul... or whatever you have there.', "You work on a farm for a day. It wasn't fun.",'You made a bet with someone that you could survive a fall off your house. You got two broken legs, but hey, money!',"You won a game of hangman. Your friend's right above you now.","You sold Doki Doki Literature club to a weeb. Not only did you scam them for a free game, he's gonna cry himself to sleep tonight.","You sold your company. It wasn't very good.",'You streamed on Twitch! Some guy felt bad for you and donated, since you had 1 sub.','You acquired the rights to the restaurant version of "Happy Birthday". Bascially no one uses that anymore, but still. Royalties!',"You wrote a fan-fiction novel! A couple teenagers bought it. Hopefully their parents don't see it...",'You got your kidney stolen, and woke up in a bathtub of ice! you sold the ice for money, and you had decent insurance.','You won a "Most Improved" award! You sold the medal to some rich, bratty kid.']
CRIMEWIN = ['You crimed. You won. Nice.', 'Filthy criminal; you got money.','The guy next door has really loud bass throbbing in the middle of the night, constantly. You stole his speakers and stole them to make some money, and enjoy the silence.','You saw your grandmother yesterday! She left her purse with you while she went to the bathroom.',"You hacked Hilary Clinton's emails. You sold them to a Trump supporter.",'You tried to assassinate the president. You failed, but some idiot believed you and gave you some cash as thanks.','You created a Tech Support Scam, and started calling some old ladies. Your Indian accent paid off, and you sold some fake software!','You saw a guy walking down an alleyway at night, looking sketchy. You threaten him, and he gives you his weed. You then sold it to the next guy coming down that alleyway.',"You stole some records from a guy's garage. People are crazy, and paid a lot of money for them.","You tried to rob a bank, but couldn't open the safe. Luckily, there was a cash register nearby.",'You pirated some games and sold them.','You dog decided to bite a guy the other day. That guy paid you to shoot your dog. Like the horrible monster you are, you accepted.','You robbed from a different currency bot!',"You pirated Doki Doki Literature club and sold it to a couple weebs. You then got more money from the inevitable therapy sessions that resulted, even though you're not a Doctor (probably). In any case, malpractice. You did it, though."]
CRIMELOSE = ['You crimed. You lost. Oof.', 'Criminal scum; you lost money.','You tried to escape Libyan terrorists, but you went 88 MPH. The plutonium from 2085 still cost a fair amount, though.','You tried to kill a funny skeleton. You had a bad time.',"You tried to prostitute yourself for a married guy. Too bad they're a good person, and a devout Catholic.","You attempted a Tech Support Scam. Unfortunantely, you didn't spoof your phone, and you called me.","You tried to pirate a Nintendo game. Too bad it's Nintendo.","Whilst escaping from the cops, you tripped over your own shoelaces. In a car. I don't even know how you managed that.",'You killed your S.O. You got caught. You deserved it.', 'You went on 4chan without Incognito mode. How stupid.',"You decided to watch hentai, since that's the kind of person you are. Too bad they were lolis, you live in America, and you already were on an FBI watch list.",'You brought your white van filled with candy to the park. How stupid are you?','You went on the Dark Web, but forgot Incognito mode. You imbecile.',"You killed a cat. You deserve death, but you were only fined. You'll be sorry when I take over.",'You tried to steal from me. Nice try.', 'You got caught being a pedophile. You deserve far worse than this.','You never wanted a sibling. Your parents just found out. You no longer have any siblings.','You tried to buy drugs from a police officer. Smart.', 'Hello, Mr. Cosby.','You taught your dog to Nazi Salute. In the UK. Oops.',"For some reason, you decided to pirate a free game. It was Doki Doki Literature club. Since you're an ignorant weeb, you thought it was a dating sim, and got excited. Your favorites were Sayori and Yuri. Not only did you get fined for using the Pirate Bay on your school account, but you also had to pay for those therapy sessions."]
ROBWIN = ['You succeeded at robbing!', 'You stole some money. Nice.','As your victim looked the other way, you stole his wallet! It was in his hand, too. Impressive.',"You broke into your victim's house late at night, and stole money from their safe. Why do they even have a safe?","You put ransomware on your victim's Mac. They are *not* immune to viruses.",'Your victim got tricked into calling you, "Windows", after you froze their PC. You sold them fake AV software, and took their money.',"You tried to break into your victim's bank vault. It didn't work, so you turned around and grabbed their wallet instead. Yes, they were behind you the whole time. Pretty stupid. At least you had a mask..."]
ROBLOSE = ['You failed at robbing!', 'You were fined. Oops.',"You put on your best robber outfit, and went to your victim's house. Why'd you wear a robber outfit!?","You took the wallet out of your victim's back pocket, and tried to run away. You tripped. They took their wallet back, *and* your wallet. Don't rob the robber.",'You tried to rob your victim as they were pulled over. By a police car. Are you ok?','Seriously, stop robbing. You got caught. Again. Be better next time.']


class Economy():
    def __init__(self, bot):
        self.bot = bot

    def getUsers(self, ctx, arg='noArg'):
        userList = []
        userIDList = []
        userNickList = []
        for person in ctx.guild.members:  #Creates lists
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

    @commands.command(
        aliases=['bal', 'mon'],
        description=
        'Displays the amount of money either you have, or the person you inputted. Displays On Hand money, Bank, and Total money.'
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def money(self, ctx, *user: str):
        "Checks your balance or someone else's balance."
        guild = ctx.guild.id
        member = ctx.author.id
        arg = ''
        for item in user:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        if arg == '':
            try:
                currentMoney = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
            except:
                currentMoney = 0
        else:
            try:
                if arg[2] == '!':
                    member = int(arg[3:len(arg) - 1])
                else:
                    member = int(arg[2:len(arg) - 1])
            except:
                member = ''
        if self.bot.get_guild(guild).get_member(member) is None:
            (findList, findIDList) = self.getUsers(ctx, arg)
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
                currentMoney = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
            except:
                currentMoney = 0
            try:
                currentBank = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p', 'rb'))
            except:
                currentBank = 0
            balanceEmbed = discord.Embed(
                title=str(self.bot.get_guild(guild).get_member(member)) + "'s Money", color=65280)
            balanceEmbed.add_field(name='On Hand', value='$' + str('{:,}'.format(currentMoney)), inline=True)
            balanceEmbed.add_field(name='Bank', value='$' + str('{:,}'.format(currentBank)), inline=True)
            balanceEmbed.add_field(
                name='Total', value='$' + str('{:,}'.format(currentMoney + currentBank)), inline=True)
            await ctx.send(embed=balanceEmbed)

    @commands.command(aliases=['money-adjust', 'mon-adj', 'money-adj', 'moneyadj'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def moneyadjust(self, ctx, amount: str, *user: str):
        'Admin-only. Adjusts the amount of money On Hand of the person inputted.'
        guild = ctx.guild.id
        member = ctx.author.id
        arg = ''
        for item in user:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        amount = amount.replace(',', '')
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if member in ADMINS:
            try:
                if arg[2] == '!':
                    member = int(arg[3:len(arg) - 1])
                else:
                    member = int(arg[2:len(arg) - 1])
            except:
                member = ''
            if self.bot.get_guild(guild).get_member(member) is None:
                (findList, findIDList) = self.getUsers(ctx, arg)
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
            if (self.bot.get_guild(guild).get_member(member) is None) or (amount == ''):
                await ctx.send('Invalid input, use `?money-adjust money @user`.')
            else:
                try:
                    currentMoney = pickle.load(
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p',
                             'rb'))
                except:
                    currentMoney = 0
                try:
                    currentMoney += int(amount)
                    pickle.dump(
                        currentMoney,
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p',
                             'wb'))
                    if int(amount) > 0:
                        giveEmbed = discord.Embed(
                            title=((((('$' + str('{:,}'.format(int(amount)))) + ' given to ') + str(
                                self.bot.get_guild(guild).get_member(member).display_name)) + ' by ') + str(
                                    ctx.author.display_name)) + '.',
                            color=65280)
                    elif int(amount) < 0:
                        giveEmbed = discord.Embed(
                            title=((((('$' + str('{:,}'.format(abs(int(amount))))) + ' taken from ') + str(
                                self.bot.get_guild(guild).get_member(member).display_name)) + ' by ') + str(
                                    ctx.author.display_name)) + '.',
                            color=65280)
                    else:
                        giveEmbed = discord.Embed(title='No money given.', color=65280)
                    await ctx.send(embed=giveEmbed)
                except:
                    await ctx.send('Error, make sure "money" is an integer in `?money-adjust money @user`.')
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(aliases=['bank-adjust', 'bank-adj', 'bankadj'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def bankadjust(self, ctx, amount: str, *user: str):
        'Admin-only. Same as ?money-adjust, but for the bank instead.'
        guild = ctx.guild.id
        member = ctx.author.id
        arg = ''
        for item in user:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        arg2 = amount.replace(',', '')
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if member in ADMINS:
            try:
                if arg[2] == '!':
                    member = int(arg[3:len(arg) - 1])
                else:
                    member = int(arg[2:len(arg) - 1])
            except:
                member = ''
            if self.bot.get_guild(guild).get_member(member) is None:
                (findList, findIDList) = self.getUsers(ctx, arg)
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
            if (self.bot.get_guild(guild).get_member(member) is None) or (arg2 == 'noArg'):
                await ctx.send('Invalid input, use `?bank-adjust money @user`.')
            else:
                try:
                    currentMoney = pickle.load(
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p',
                             'rb'))
                except:
                    currentMoney = 0
                try:
                    currentMoney += int(arg2)
                    pickle.dump(
                        currentMoney,
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p',
                             'wb'))
                    if int(arg2) > 0:
                        giveEmbed = discord.Embed(
                            title=((((('$' + '{:,}'.format(int(arg2))) + ' given to ') + str(
                                self.bot.get_guild(guild).get_member(member).display_name)) + "'s bank by ") + str(
                                    ctx.author.display_name)) + '.',
                            color=65280)
                    elif int(arg2) < 0:
                        giveEmbed = discord.Embed(
                            title=((((('$' + str('{:,}'.format(abs(int(arg2))))) + ' taken from ') + str(
                                self.bot.get_guild(guild).get_member(member).display_name)) + ' by ') + str(
                                    ctx.author.display_name)) + '.',
                            color=65280)
                    else:
                        giveEmbed = discord.Embed(title='No money given.', color=65280)
                    await ctx.send(embed=giveEmbed)
                except:
                    await ctx.send('Error, make sure "money" is an integer in `?bank-adjust money @user`.')
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(
        aliases=['dep'],
        description=
        'Deposits the money you have. You can deposit a specific amount, or all on hand. Format: "?dep all", or "?dep amount".'
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def deposit(self, ctx, amount: str):
        'Deposits the money you have.'
        guild = ctx.guild.id
        member = ctx.author.id
        try:
            currentMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            currentMoney = 0
        try:
            currentBank = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p', 'rb'))
        except:
            currentBank = 0
        arg = amount.replace(',', '')
        if arg == 'all':
            if currentMoney <= 0:
                await ctx.send('You have nothing to deposit.')
            else:
                currentBank += currentMoney
                depEmbed = discord.Embed(title=('$' + '{:,}'.format(currentMoney)) + ' deposited!', color=65280)
                await ctx.send(embed=depEmbed)
                currentMoney = 0
        else:
            try:
                if int(arg) > currentMoney:
                    await ctx.send("You're not that rich. Deposit what you can.")
                elif int(arg) < 0:
                    await ctx.send('Use `?with` to withdraw money.')
                else:
                    currentBank += int(arg)
                    currentMoney -= int(arg)
                    depEmbed = discord.Embed(title=('$' + '{:,}'.format(int(arg))) + ' deposited!', color=65280)
                    await ctx.send(embed=depEmbed)
            except:
                await ctx.send('Invalid input, use `?dep amount`.')
        pickle.dump(currentMoney,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
        pickle.dump(currentBank,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p', 'wb'))

    @commands.command(aliases=['with'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def withdraw(self, ctx, amount='noArg'):
        'Same as ?dep, but for withdrawing from the bank.'
        guild = ctx.guild.id
        member = ctx.author.id
        try:
            currentMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            currentMoney = 0
        try:
            currentBank = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p', 'rb'))
        except:
            currentBank = 0
        arg = amount.replace(',', '')
        if arg == 'all':
            if currentBank <= 0:
                await ctx.send('You have nothing in your bank. Sad, really.')
            else:
                currentMoney += currentBank
                withEmbed = discord.Embed(title=('$' + '{:,}'.format(currentBank)) + ' withdrawn!', color=65280)
                await ctx.send(embed=withEmbed)
                currentBank = 0
        else:
            try:
                if int(arg) > currentBank:
                    await ctx.send("You're not that rich. Withdraw what you have.")
                elif int(arg) < 0:
                    await ctx.send('Use `?dep` to deposit money.')
                else:
                    currentBank -= int(arg)
                    currentMoney += int(arg)
                    withEmbed = discord.Embed(title=('$' + '{:,}'.format(int(arg))) + ' withdrawn!', color=65280)
                    await ctx.send(embed=withEmbed)
            except:
                await ctx.send('Invalid input, use `?with amount`.')
        pickle.dump(currentMoney,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
        pickle.dump(currentBank,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p', 'wb'))

    @commands.command(description='Gives money to someone of your choice.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def give(self, ctx, amount: str, *person: str):
        'Gives money from your On Hand to someone else.'
        guild = ctx.guild.id
        member = ctx.author.id
        arg = ''
        for item in person:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        arg2 = amount.replace(',', '')
        try:
            giverMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            giverMoney = 0
        try:
            if arg[2] == '!':
                member = int(arg[3:len(arg) - 1])
            else:
                member = int(arg[2:len(arg) - 1])
        except:
            member = ''
        if self.bot.get_guild(guild).get_member(member) is None:
            (findList, findIDList) = self.getUsers(ctx, arg)
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
        if (self.bot.get_guild(guild).get_member(member) is None) or (arg2 == ''):
            await ctx.send('Invalid input, use `?give money @user`.')
        else:
            try:
                receiverMoney = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
            except:
                receiverMoney = 0
            if arg2 == 'all':
                arg2 = str(giverMoney)
            try:
                if int(arg2) <= 0:
                    await ctx.send("Don't try and exploit this anymore. My master fixed it. Use a positive number.")
                    return
                if int(arg2) > giverMoney:
                    giveEmbed = discord.Embed(title="You don't have that much. Poor you.", color=65280)
                else:
                    receiverMoney += int(arg2)
                    giverMoney -= int(arg2)
                    pickle.dump(
                        receiverMoney,
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p',
                             'wb'))
                    pickle.dump(
                        giverMoney,
                        open(((((
                            ('servers' + os.sep) + str(guild)) + os.sep) + str(ctx.author.id)) + os.sep) + 'money.p',
                             'wb'))
                    if int(arg2) > 0:
                        giveEmbed = discord.Embed(
                            title=((((('$' + '{:,}'.format(int(arg2))) + ' given to ') + str(
                                self.bot.get_guild(guild).get_member(member).display_name)) + ' by ') + str(
                                    ctx.author.display_name)) + '. How kind.',
                            color=65280)
                    elif int(arg2) < 0:
                        giveEmbed = discord.Embed(title="This isn't robbery. This is giving.", color=65280)
                    else:
                        giveEmbed = discord.Embed(title='Really? Nothing?', color=65280)
                await ctx.send(embed=giveEmbed)
            except:
                await ctx.send('Error, make sure "money" is an integer in `?give money @user`.')

    @commands.command(
        aliases=['lb', 'top', 'highscore'],
        description='Displays the server\'s leaderboard. Use "?lb page" for a different page.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def leaderboard(self, ctx, page='1'):
        "Displays the server's leaderboard."
        guild = ctx.guild.id
        arg = page
        myMembers = []
        myMoney = []
        for human in ctx.guild.members:
            try:
                currentMoney = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(human.id)) + os.sep) + 'money.p', 'rb'))
            except:
                currentMoney = 0
            try:
                currentBank = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(human.id)) + os.sep) + 'bank.p', 'rb'))
            except:
                currentBank = 0
            myMembers.append(str(human))
            myMoney.append(int(currentMoney + currentBank))
        moneyDict = dict(zip(myMembers, myMoney))
        topDict = collections.OrderedDict(sorted(zip(myMembers, myMoney), key=(lambda i: i[1]), reverse=True))
        orderMembers = []
        orderMoney = []
        for (k, v) in topDict.items():
            orderMembers.append(k)
            orderMoney.append(v)
        maxPage = math.ceil(len(myMembers) / 10)
        if int(arg) > maxPage:
            arg = str(maxPage)
        if int(arg) > 1:
            begIn = (int(arg) * 10) - 10
            endIn = int(arg) * 10
        else:
            arg = 1
            begIn = 0
            endIn = 10
        newMembers = orderMembers[begIn:endIn]
        newMoney = orderMoney[begIn:endIn]
        lbEmbed = discord.Embed(
            title=str(self.bot.get_guild(guild)) + ' Leaderboard',
            description='---------------------------------------------',
            color=16711680)
        x = begIn
        y = 0
        while x <= endIn:
            try:
                lbEmbed.add_field(
                    name=(((str(x + 1) + ': ') + str(newMembers[y])) + ' | $') + '{:,}'.format(newMoney[y]),
                    value=(((str(x + 2) + ': ') + str(newMembers[y + 1])) + ' | $') + '{:,}'.format(newMoney[y + 1]),
                    inline=False)
            except IndexError:
                try:
                    lbEmbed.add_field(
                        name=(((str(x + 1) + ': ') + str(newMembers[y])) + ' | $') + '{:,}'.format(newMoney[y]),
                        value='\u200b',
                        inline=False)
                except IndexError:
                    break
            x += 2
            y += 2
        lbEmbed.set_thumbnail(url=ctx.message.guild.icon_url)
        lbEmbed.set_footer(text=(('Page ' + str(arg)) + '/') + str(maxPage))
        await ctx.send(embed=lbEmbed)

    @commands.command(
        aliases=['reset-economy', 'reset-eco', 'reseteco'],
        description='Admin-only. Resets all money in the server. Make sure you want to do this for real.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reseteconomy(self, ctx, arg='Nope,', arg2=" I'm uncertain"):
        'Admin-only. Resets all money in the server.'
        guild = ctx.guild.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if ctx.author.id in ADMINS:
            if (arg == 'I_REALLY') and (arg2 == 'wantToDoThis'):
                for member in ctx.guild.members:
                    currentMoney = 0
                    currentBank = 0
                    try:
                        pickle.dump(
                            currentMoney,
                            open(((((
                                ('servers' + os.sep) + str(guild)) + os.sep) + str(member.id)) + os.sep) + 'money.p',
                                 'wb'))
                    except:
                        pass
                    try:
                        pickle.dump(
                            currentBank,
                            open(
                                ((((('servers' + os.sep) + str(guild)) + os.sep) + str(member.id)) + os.sep) + 'bank.p',
                                'wb'))
                    except:
                        pass
                await ctx.send('Done! I am yours to command! *...mostly.*')
            else:
                await ctx.send(
                    'You sure? This resets *all* money in this server. If you are sure, use `?reset-economy I_REALLY wantToDoThis`.'
                )
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(
        aliases=['give-to-all'], description='Admin-only. Gives a certain amount of money to everyone in the server.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def givetoall(self, ctx, amount: str):
        'Admin-only. Gives money to everyone.'
        guild = ctx.guild.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        errorThing = False
        arg = amount.replace(',', '')
        if ctx.author.id in ADMINS:
            for member in ctx.guild.members:
                try:
                    currentMoney = pickle.load(
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member.id)) + os.sep) + 'money.p',
                             'rb'))
                except:
                    currentMoney = 0
                try:
                    currentMoney += int(arg)
                except (TypeError, ValueError):
                    await ctx.send('Please use a valid sum of money.')
                    errorThing = True
                    break
                try:
                    pickle.dump(
                        currentMoney,
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member.id)) + os.sep) + 'money.p',
                             'wb'))
                except:
                    pass
            if (not errorThing):
                await ctx.send('Done! Enjoy the money, everyone!')
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(aliases=['set-salary', 'set-sal', 'setsal'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setsalary(self, ctx, role: str, salary: str):
        'Admin-only. Sets the salary for a certain role.'
        guild = ctx.guild.id
        member = ctx.author.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        arg = role
        arg2 = salary.replace(',', '')
        if member in ADMINS:
            if role[2] == '&':
                role = role[3:len(arg) - 1]
            else:
                role = role[2:len(arg) - 1]
            if (not os.path.exists(((('servers' + os.sep) + str(guild)) + os.sep) + str(role))) or (arg2 == ''):
                await ctx.send('Invalid input, use `?set-salary @role salary`.')
            else:
                try:
                    currentMoney = pickle.load(
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(role)) + os.sep) + 'salary.p',
                             'rb'))
                except:
                    currentMoney = 0
                try:
                    currentMoney = int(arg2)
                    pickle.dump(
                        currentMoney,
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(role)) + os.sep) + 'salary.p',
                             'wb'))
                    await ctx.send('Done!')
                except TypeError:
                    await ctx.send('Error, make sure "salary" is an integer in `?set-salary @role salary`.')
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(
        aliases=['give-salary', 'give-sal', 'givesal'],
        description="Admin-only. Distributes salary, even if it's not the right time.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def givesalary(self, ctx):
        'Admin-only. Distributes salary.'
        guild = ctx.guild.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if ctx.author.id in ADMINS:
            salEmbed = discord.Embed(title='Salary Pay', color=65280)
            for role in self.bot.get_guild(guild).roles:
                try:
                    currentSal = pickle.load(
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(role.id)) + os.sep) + 'salary.p',
                             'rb'))
                except:
                    currentSal = 0
                if currentSal != 0:
                    for member in ctx.guild.members:
                        for item in member.roles:
                            if item.id == role.id:
                                try:
                                    currentMoney = pickle.load(
                                        open(
                                            ((((('servers' + os.sep) + str(guild)) + os.sep) + str(member.id)) + os.sep)
                                            + 'money.p', 'rb'))
                                except:
                                    currentMoney = 0
                                currentMoney += currentSal
                                pickle.dump(
                                    currentMoney,
                                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member.id)) + os.sep) +
                                         'money.p', 'wb'))
                    toSay = (str(role) + ' got their salary of $') + '{:,}'.format(currentSal)
                    if toSay[0] == '@':
                        await ctx.send(toSay[1:])
                    else:
                        await ctx.send(toSay)
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(
        aliases=['sal'],
        description="Used to check the salaries of each role in the server. If it's $0, it won't show.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def salary(self, ctx):
        "Checks the server's salaries."
        guild = ctx.guild.id
        member = ctx.author.id
        salEmbed = discord.Embed(title='Role Salaries', color=65280)
        for role in self.bot.get_guild(guild).roles:
            try:
                currentMoney = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(role.id)) + os.sep) + 'salary.p', 'rb'))
            except:
                currentMoney = 0
            if currentMoney != 0:
                salEmbed.add_field(name=str(role), value='$' + '{:,}'.format(currentMoney), inline=False)
        salEmbed.add_field(name='Other Roles:', value='$0', inline=False)
        await ctx.send(embed=salEmbed)

    @commands.command(
        aliases=['set-channel', 'setchan', 'set-chan'],
        description=
        'Admin-only. Sets the channel for bot notifications. Uses the default one by default. Format: "?setchannel #channel".'
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setchannel(self, ctx, channel: str):
        'Admin-only. Sets the channel for bot notifications.'
        guild = ctx.guild.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        setChannel = False
        arg = channel
        if ctx.author.id in ADMINS:
            for thing in ctx.guild.channels:
                if self.bot.get_channel(int(arg[2:len(arg) - 1])) == thing:
                    pickle.dump(thing.id, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'channel.p', 'wb'))
                    await ctx.send('Channel Set!')
                    setChannel = True
            if (not setChannel):
                await ctx.send('Error, invalid channel.')
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(aliases=['reset-salary', 'reset-sal', 'resetsal'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def resetsalary(self, ctx, arg='I am ', arg2='unsure about this.'):
        'Admin-only. Resets all of the salaries for the server'
        guild = ctx.guild.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if ctx.author.id in ADMINS:
            if (arg == 'I_REALLY') and (arg2 == 'wantToDoThis'):
                for role in ctx.guild.roles:
                    currentMoney = 0
                    try:
                        pickle.dump(
                            currentMoney,
                            open(
                                ((((('servers' + os.sep) + str(guild)) + os.sep) + str(role.id)) + os.sep) + 'salary.p',
                                'wb'))
                    except:
                        pass
                await ctx.send('Done! I am yours to command! *...mostly.*')
            else:
                await ctx.send(
                    'You sure? This resets *all* wages in this server. If you are sure, use `?reset-salary I_REALLY wantToDoThis`.'
                )
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(
        aliases=['job'],
        description='Work for a small amount of money. Always succeeds, but only can be done sometimes.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def work(self, ctx):
        'Work for a small amount of money.'
        guild = ctx.guild.id
        member = ctx.author.id
        global WORK
        try:
            currentMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            currentMoney = 0
        try:
            workCooldown = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'workCooldown.p',
                     'rb'))
        except:
            workCooldown = 0
        try:
            coolWork = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolWork.p', 'rb'))
        except:
            coolWork = 60
        try:
            maxWork = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxWork.p', 'rb'))
        except:
            maxWork = 150
        try:
            minWork = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minWork.p', 'rb'))
        except:
            minWork = 50
        if workCooldown < 0:
            randomWork = WORK[random.randint(0, len(WORK) - 1)]
            randomMoney = random.randint(minWork, maxWork)
            workEmbed = discord.Embed(title=str(ctx.author) + "'s Work", description=randomWork, color=65280)
            workEmbed.add_field(name='Earned:', value='$' + '{:,}'.format(randomMoney), inline=True)
            currentMoney += randomMoney
            pickle.dump(
                currentMoney,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
            await ctx.send(embed=workEmbed)
            workCooldown = coolWork
            pickle.dump(
                workCooldown,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'workCooldown.p',
                     'wb'))
        else:
            await ctx.send(('Please wait ' + '{:,}'.format(workCooldown)) + ' seconds before working again!')

    @commands.command(aliases=['set-work'], description='Admin-only. Set max, min, and cooldown values of ?work.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setwork(self, ctx, myMin='noArg', myMax='noArg', coolDown='noArg'):
        'Admin-only. Set up values for work.'
        guild = ctx.guild.id
        member = ctx.author.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        try:
            maxWork = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxWork.p', 'rb'))
        except:
            maxWork = 150
        try:
            minWork = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minWork.p', 'rb'))
        except:
            minWork = 50
        try:
            coolWork = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolWork.p', 'rb'))
        except:
            coolWork = 60
        if member in ADMINS:
            if (myMin == 'noArg') or (myMax == 'noArg') or (coolDown == 'noArg'):
                workEmbed = discord.Embed(
                    title='Work Settings',
                    description='Use "?setwork min max cooldown" to set the values.',
                    color=65280)
                workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(int(maxWork)), inline=True)
                workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(int(minWork)), inline=True)
                workEmbed.add_field(name='Cooldown:', value='{:,}'.format(int(coolWork)) + ' Seconds', inline=True)
                await ctx.send(embed=workEmbed)
            else:
                try:
                    minWork = int(myMin)
                    maxWork = int(myMax)
                    coolWork = int(coolDown)
                    pickle.dump(maxWork, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxWork.p', 'wb'))
                    pickle.dump(minWork, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minWork.p', 'wb'))
                    pickle.dump(coolWork, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolWork.p', 'wb'))
                    await ctx.send('Done!')
                except TypeError:
                    workEmbed = discord.Embed(
                        title='Work Settings',
                        description='Use "?setwork min max cooldown" to set the values.',
                        color=65280)
                    workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(int(maxWork)), inline=True)
                    workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(int(minWork)), inline=True)
                    workEmbed.add_field(name='Cooldown:', value='{:,}'.format(int(coolWork)) + ' Seconds', inline=True)
                    await ctx.send(embed=workEmbed)
        else:
            workEmbed = discord.Embed(
                title='Work Settings',
                description=
                "These are the stats for the work command. You're not an admin, so this command does nothing else. Sucks for you.",
                color=65280)
            workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(int(maxWork)), inline=True)
            workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(int(minWork)), inline=True)
            workEmbed.add_field(name='Cooldown:', value='{:,}'.format(int(coolWork)) + ' Seconds', inline=True)
            await ctx.send(embed=workEmbed)

    @commands.command(description='Crime for a large amount of money. Sometimes fails, and you lose money instead.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def crime(self, ctx):
        "Crime for a large amount of money. Sometimes you win, and sometimes you're bad."
        guild = ctx.guild.id
        member = ctx.author.id
        global CRIMEWIN
        global CRIMELOSE
        try:
            currentMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            currentMoney = 0
        try:
            currentBank = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p', 'rb'))
        except:
            currentBank = 0
        myMoney = currentBank + currentMoney
        try:
            crimeCooldown = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'crimeCooldown.p',
                     'rb'))
        except:
            crimeCooldown = 0
        try:
            coolCrime = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolCrime.p', 'rb'))
        except:
            coolCrime = 120
        try:
            crimeRate = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'crimeRate.p', 'rb'))
        except:
            crimeRate = 20
        try:
            maxCrime = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxCrime.p', 'rb'))
        except:
            maxCrime = 1500
        try:
            minCrime = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minCrime.p', 'rb'))
        except:
            minCrime = 500
        if crimeCooldown < 0:
            didSucceed = 0
            currentChance = random.randint(0, 100)
            if myMoney >= 0:
                currentChance += myMoney / 1000
            else:
                currentChance -= myMoney / (-10)
            if currentChance > 100:
                currentChance = 100
            elif currentChance < 0:
                currentChance = 0
            if currentChance < crimeRate:
                didSucceed = 1
            if didSucceed == 1:
                randomCrime = CRIMEWIN[random.randint(0, len(CRIMEWIN) - 1)]
            else:
                randomCrime = CRIMELOSE[random.randint(0, len(CRIMELOSE) - 1)]
            randomMoney = random.randint(minCrime, maxCrime)
            if didSucceed == 1:
                crimeEmbed = discord.Embed(title=str(ctx.author) + "'s Crimes", description=randomCrime, color=65280)
                crimeEmbed.add_field(name='Earned:', value='$' + '{:,}'.format(randomMoney), inline=True)
                currentMoney += randomMoney
                pickle.dump(
                    currentMoney,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
                await ctx.send(embed=crimeEmbed)
            else:
                crimeEmbed = discord.Embed(title=str(ctx.author) + "'s Crimes", description=randomCrime, color=16711680)
                crimeEmbed.add_field(name='Lost:', value='$' + '{:,}'.format(randomMoney), inline=True)
                currentMoney -= randomMoney
                pickle.dump(
                    currentMoney,
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'wb'))
                await ctx.send(embed=crimeEmbed)
            crimeCooldown = coolCrime
            pickle.dump(
                crimeCooldown,
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'crimeCooldown.p',
                     'wb'))
        else:
            await ctx.send(('Please wait ' + '{:,}'.format(crimeCooldown)) + ' seconds before being a criminal again!')

    @commands.command(
        aliases=['set-crime'],
        description=
        'Admin-only. Set max, min, winrate, and cooldown values of ?crime. Losing = you lose a number between min and max. Winning = gaining that number.'
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setcrime(self, ctx, myMin='noArg', myMax='noArg', winRate='noArg', coolDown='noArg'):
        'Admin-only. Set crime cooldowns.'
        guild = ctx.guild.id
        member = ctx.author.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        try:
            maxCrime = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxCrime.p', 'rb'))
        except:
            maxCrime = 1500
        try:
            minCrime = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minCrime.p', 'rb'))
        except:
            minCrime = 500
        try:
            crimeRate = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'crimeRate.p', 'rb'))
        except:
            crimeRate = 20
        try:
            coolCrime = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolCrime.p', 'rb'))
        except:
            coolCrime = 120
        if member in ADMINS:
            if (myMin == 'noArg') or (myMax == 'noArg') or (coolDown == 'noArg') or (winRate == 'noArg'):
                workEmbed = discord.Embed(
                    title='Crime Settings',
                    description=
                    'Use "?setcrime min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.',
                    color=65280)
                workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(maxCrime), inline=True)
                workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(minCrime), inline=True)
                workEmbed.add_field(name='Crimerate:', value='{:,}'.format(crimeRate) + '%', inline=True)
                workEmbed.add_field(name='Cooldown:', value='{:,}'.format(coolCrime) + ' Seconds', inline=True)
                await ctx.send(embed=workEmbed)
            else:
                try:
                    minCrime = int(myMin)
                    maxCrime = int(myMax)
                    crimeRate = int(winRate)
                    coolCrime = int(coolDown)
                    if crimeRate > 99:
                        crimeRate = 99
                    elif crimeRate < 1:
                        crimeRate = 1
                    pickle.dump(maxCrime, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxCrime.p', 'wb'))
                    pickle.dump(minCrime, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minCrime.p', 'wb'))
                    pickle.dump(crimeRate, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'crimeRate.p', 'wb'))
                    pickle.dump(coolCrime, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolCrime.p', 'wb'))
                    await ctx.send('Done!')
                except TypeError:
                    workEmbed = discord.Embed(
                        title='Crime Settings',
                        description=
                        'Use "?setcrime min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.',
                        color=65280)
                    workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(maxCrime), inline=True)
                    workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(minCrime), inline=True)
                    workEmbed.add_field(name='Crimerate:', value='{:,}'.format(crimeRate) + '%', inline=True)
                    workEmbed.add_field(name='Cooldown:', value='{:,}'.format(coolCrime) + ' Seconds', inline=True)
                    await ctx.send(embed=workEmbed)
        else:
            workEmbed = discord.Embed(
                title='Crime Settings',
                description=
                "You're no admin. Anyway, here's the stats.. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.",
                color=65280)
            workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(maxCrime), inline=True)
            workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(minCrime), inline=True)
            workEmbed.add_field(name='Crimerate:', value='{:,}'.format(crimeRate) + '%', inline=True)
            workEmbed.add_field(name='Cooldown:', value='{:,}'.format(coolCrime) + ' Seconds', inline=True)
            await ctx.send(embed=workEmbed)

    @commands.command(
        aliases=['steal'], description="Rob money from a member's On Hand. It may fail, and you'll lose instead.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def rob(self, ctx, *person: str):
        "Rob money from a member's On Hand."
        guild = ctx.guild.id
        member = ctx.author.id
        arg = ''
        for item in person:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        global ROBWIN
        global ROBLOSE
        try:
            robberMoney = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
        except:
            robberMoney = 0
        try:
            currentBank = pickle.load(
                open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'bank.p', 'rb'))
        except:
            currentBank = 0
        try:
            if arg[2] == '!':
                member = int(arg[3:len(arg) - 1])
            else:
                member = int(arg[2:len(arg) - 1])
        except:
            member = ''
        if self.bot.get_guild(guild).get_member(member) is None:
            (findList, findIDList) = self.getUsers(ctx, arg)
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
            await ctx.send('Invalid input, use `?rob @user`.')
        else:
            if member == ctx.author.id:
                await ctx.send('Robbing yourself is a stupid idea. Stop it.')
                return
            try:
                robbedMoney = pickle.load(
                    open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p', 'rb'))
            except:
                robbedMoney = 0
            try:
                robCooldown = pickle.load(
                    open(((((
                        ('servers' + os.sep) + str(guild)) + os.sep) + str(ctx.author.id)) + os.sep) + 'robCooldown.p',
                         'rb'))
            except:
                robCooldown = 0
            try:
                coolRob = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolRob.p', 'rb'))
            except:
                coolRob = 120
            try:
                robRate = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'robRate.p', 'rb'))
            except:
                robRate = 20
            try:
                maxRob = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxRob.p', 'rb'))
            except:
                maxRob = 1500
            try:
                minRob = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minRob.p', 'rb'))
            except:
                minRob = 500
            if robCooldown < 0:
                didSucceed = 0
                currentChance = random.randint(0, 100)
                if robberMoney >= 0:
                    currentChance += (robberMoney + currentBank) / 1000
                else:
                    currentChance -= (robberMoney + currentBank) / (-10)
                if currentChance > 100:
                    currentChance = 100
                elif currentChance < 0:
                    currentChance = 0
                if currentChance < robRate:
                    didSucceed = 1
                if didSucceed == 1 and robbedMoney > 0:
                    randomRob = ROBWIN[random.randint(0, len(ROBWIN) - 1)]
                    randomMoney = int((random.randint(75, 95) / 100) * robbedMoney)
                else:
                    randomRob = ROBLOSE[random.randint(0, len(ROBLOSE) - 1)]
                    randomMoney = int(random.randint(minRob, maxRob))
                if robbedMoney <= 0:
                    robEmbed = discord.Embed(
                        title=(str(ctx.author) + "'s Robbery of ") + str(
                            self.bot.get_guild(guild).get_member(member)),
                        description="They didn't even have enough money to rob! Idiot.",
                        color=16711680)
                    robEmbed.add_field(name='Fined:', value='$' + '{:,}'.format(randomMoney), inline=True)
                    robberMoney -= randomMoney
                    pickle.dump(
                        robberMoney,
                        open(((((
                            ('servers' + os.sep) + str(guild)) + os.sep) + str(ctx.author.id)) + os.sep) + 'money.p',
                             'wb'))
                    await ctx.send(embed=robEmbed)
                elif didSucceed == 1:
                    robEmbed = discord.Embed(
                        title=(str(ctx.author) + "'s Robbery of ") + str(
                            self.bot.get_guild(guild).get_member(member)),
                        description=randomRob,
                        color=65280)
                    robEmbed.add_field(name='Stolen:', value='$' + '{:,}'.format(randomMoney), inline=True)
                    robberMoney += randomMoney
                    robbedMoney -= randomMoney
                    pickle.dump(
                        robberMoney,
                        open(((((
                            ('servers' + os.sep) + str(guild)) + os.sep) + str(ctx.author.id)) + os.sep) + 'money.p',
                             'wb'))
                    pickle.dump(
                        robbedMoney,
                        open(((((('servers' + os.sep) + str(guild)) + os.sep) + str(member)) + os.sep) + 'money.p',
                             'wb'))
                    await ctx.send(embed=robEmbed)
                else:
                    robEmbed = discord.Embed(
                        title=(str(ctx.author) + "'s Robbery of ") + str(
                            self.bot.get_guild(guild).get_member(member)),
                        description=randomRob,
                        color=16711680)
                    robEmbed.add_field(name='Fined:', value='$' + '{:,}'.format(randomMoney), inline=True)
                    robberMoney -= randomMoney
                    pickle.dump(
                        robberMoney,
                        open(((((
                            ('servers' + os.sep) + str(guild)) + os.sep) + str(ctx.author.id)) + os.sep) + 'money.p',
                             'wb'))
                    await ctx.send(embed=robEmbed)
                robCooldown = coolRob
                pickle.dump(
                    robCooldown,
                    open(((((
                        ('servers' + os.sep) + str(guild)) + os.sep) + str(ctx.author.id)) + os.sep) + 'robCooldown.p',
                         'wb'))
            else:
                await ctx.send(('Please wait ' + '{:,}'.format(robCooldown)) + ' seconds before trying to rob again!')

    @commands.command(
        aliases=['set-rob', 'set-steal', 'setsteal'],
        description=
        "Admin-only. Set max, min, winrate, and cooldown values of rob. Losing = you lose a number between min and max. Winning = rob around 85% of the person's On Hand."
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setrob(self, ctx, myMin='noArg', myMax='noArg', winRate='noArg', coolDown='noArg'):
        'Admin-only. Set rob values.'
        guild = ctx.guild.id
        member = ctx.author.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        try:
            maxRob = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxRob.p', 'rb'))
        except:
            maxRob = 1500
        try:
            minRob = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minRob.p', 'rb'))
        except:
            minRob = 500
        try:
            robRate = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'robRate.p', 'rb'))
        except:
            robRate = 20
        try:
            coolRob = pickle.load(open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolRob.p', 'rb'))
        except:
            coolRob = 120
        if member in ADMINS:
            if (myMin == 'noArg') or (myMax == 'noArg') or (coolDown == 'noArg') or (winRate == 'noArg'):
                workEmbed = discord.Embed(
                    title='Rob Settings',
                    description=
                    'Use "?setrob min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.',
                    color=65280)
                workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(maxRob), inline=True)
                workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(minRob), inline=True)
                workEmbed.add_field(name='Robrate:', value='{:,}'.format(robRate) + '%', inline=True)
                workEmbed.add_field(name='Cooldown:', value='{:,}'.format(coolRob) + ' Seconds', inline=True)
                await ctx.send(embed=workEmbed)
            else:
                try:
                    minRob = int(myMin)
                    maxRob = int(myMax)
                    robRate = int(winRate)
                    coolRob = int(coolDown)
                    if robRate > 99:
                        robRate = 99
                    elif robRate < 1:
                        robRate = 1
                    pickle.dump(maxRob, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'maxRob.p', 'wb'))
                    pickle.dump(minRob, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'minRob.p', 'wb'))
                    pickle.dump(robRate, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'robRate.p', 'wb'))
                    pickle.dump(coolRob, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'coolRob.p', 'wb'))
                    await ctx.send('Done!')
                except TypeError:
                    workEmbed = discord.Embed(
                        title='Rob Settings',
                        description=
                        'Use "?setrob min max chance% cooldown" to set the values. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.',
                        color=65280)
                    workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(maxRob), inline=True)
                    workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(minRob), inline=True)
                    workEmbed.add_field(name='Robrate:', value='{:,}'.format(robRate) + '%', inline=True)
                    workEmbed.add_field(name='Cooldown:', value='{:,}'.format(coolRob) + ' Seconds', inline=True)
                    await ctx.send(embed=workEmbed)
        else:
            workEmbed = discord.Embed(
                title='Rob Settings',
                description=
                "Rob stats! No admin for you, though, so you can't do anything with this command. Note: For every $1,000 above 0$, chance goes down by 1%. For every $10 below 0$, it goes up by 1%.",
                color=65280)
            workEmbed.add_field(name='Max:', value='$' + '{:,}'.format(maxRob), inline=True)
            workEmbed.add_field(name='Min:', value='$' + '{:,}'.format(minRob), inline=True)
            workEmbed.add_field(name='Robrate:', value='{:,}'.format(robRate) + '%', inline=True)
            workEmbed.add_field(name='Cooldown:', value='{:,}'.format(coolRob) + ' Seconds', inline=True)
            await ctx.send(embed=workEmbed)

    @commands.command(
        aliases=['set-salary-time', 'setsaltime', 'set-sal-time'],
        description='Admin-only. Sets the salary giving time.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def setsalarytime(self, ctx, hour='noArg', minute='noArg'):
        'Admin-only. Sets the salary giving time to what is said. Please use military time. Format: "?set-salary-time hour minute".'
        guild = ctx.guild.id
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if ctx.author.id in ADMINS:
            try:
                hour = int(hour)
                minute = int(minute)
                if (hour < 24) and (hour >= 0) and (minute < 60) and (minute >= 0):
                    pickle.dump(hour, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'salHour.p', 'wb'))
                    pickle.dump(minute, open(((('servers' + os.sep) + str(guild)) + os.sep) + 'salMinute.p', 'wb'))
                    await ctx.send('Done!')
                else:
                    await ctx.send('Please input a valid time! (Military time)')
            except:
                await ctx.send(
                    'Invalid input! Please use the format `?set-salary-time hour minute`, using military time.')
        else:
            await ctx.channel.send(file=discord.File('nopower.gif', filename='nopower.gif'))

    @commands.command(aliases=['get-salary-time', 'getsaltime', 'get-sal-time', 'saltime', 'sal-time'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def getsalarytime(self, ctx):
        'This command tells you when the salaries will be given.'
        guild = ctx.guild.id
        try:
            salHour = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'salHour.p', 'rb'))
            salMinute = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'salMinute.p', 'rb'))
        except:
            salHour = 0
            salMinute = 0
        thePM = 'A.M.'
        if salHour == 0:
            salHour = 12
        if salHour > 12:
            salHour = salHour - 12
            thePM = 'P.M.'
        if salMinute < 10:
            salMinute = '0' + str(salMinute)
        await ctx.send((((('The salaries will be given at ' + str(salHour)) + ':') + str(salMinute)) + ' ') + thePM)


def setup(bot):
    bot.add_cog(Economy(bot))
