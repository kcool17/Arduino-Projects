#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import pickle  
import os
import random
import re
import asyncio
import json
import math
from prettytable import PrettyTable

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    
    def find_sigfigs(self, x):
        '''Returns the number of significant digits in a number. This takes into account
           strings formatted in 1.23e+3 format and even strings such as 123.450'''
        # change all the 'E' to 'e'
        x = x.lower()
        if ('e' in x):
            # return the length of the numbers before the 'e'
            myStr = x.split('e')
            return len( myStr[0] ) - 1 # to compenstate for the decimal point
        else:
            # put it in e format and return the result of that
            ### NOTE: because of the 8 below, it may do crazy things when it parses 9 sigfigs
            n = ('%.*e' %(8, float(x))).split('e')
            # remove and count the number of removed user added zeroes. (these are sig figs)
            if '.' in x:
                s = x.replace('.', '')
                #number of zeroes to add back in
                l = len(s) - len(s.rstrip('0'))
                #strip off the python added zeroes and add back in the ones the user added
                n[0] = n[0].rstrip('0') + ''.join(['0' for num in range(l)])
            else:
                #the user had no trailing zeroes so just strip them all
                n[0] = n[0].rstrip('0')
            #pass it back to the beginning to be parsed
        return self.find_sigfigs('e'.join(n))

    @commands.command(description='Add two numbers together. Change "num1" and "num2" to the numbers you wish to add together.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add(self, ctx, num1: int, num2: int):
        '''Adds stuff together.'''
        await ctx.send(num1 + num2)

    @commands.command(description='Use NdN format, with the first N the amount of rolls and the second the amount of sides on the die.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roll(self, ctx, dice: str):
        '''Rolls dice.'''
        try:
            (rolls, limit) = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        if rolls > 100:
            await ctx.send("Don't try and overload my CPU. I don't appreciate that.")
        elif limit > 1000000:
            await ctx.send('Do you *really* need to have over a million sides on this die? I mean, come *on*.')
        else:
            total = 0
            result = ''
            if rolls > 1:
                for r in range(rolls):
                    myRoll = random.randint(1, limit)
                    if r == 0:
                        result = str(myRoll)
                    else:
                        result = (result + ', ') + str(myRoll)
                    total = total + myRoll
                await ctx.send(result)
                await ctx.send('The total of your rolls is: ' + str(total))
            else:
                await ctx.send(random.randint(1, limit))

    @commands.command(description='Have as many options as you want after "?choose", with a space in between each one. One will be randomly chosen.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def choose(self, ctx, *choices: str):
        '''Chooses a random argument you give.'''
        newChoice = random.choice(choices)
        choiceEmbed = discord.Embed(title=str(ctx.author) + "'s Choices", description = newChoice, color=0x00FF00)
        await ctx.send(embed=choiceEmbed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def admintest(self, ctx):
        '''Checks if you have admin permissions in this server.'''
        ADMINS = pickle.load(open(((('servers' + os.sep) + str(ctx.guild.id)) + os.sep) + 'ADMINS.p', 'rb'))
        if str(ctx.author.id) in ADMINS:
            await ctx.send('You are an administrator/developer!')
        else:
            await ctx.send('You are *not* an administrator/developer. How sad.')

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mentionuser(self, ctx, *user: str):
        '''Mentions the user based on input'''
        #USE THIS IN OTHER FUNCTIONS
        arg = ''
        for item in user:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        (findList, findIDList) = self.getUsers(ctx, arg)
        theID = ''
        if len(findIDList) == 1:
            theID = findIDList[0]
        else:
            await ctx.send('Multiple people found. Pick someone specific next time.') 
            userFindEmbed = discord.Embed(title='Users Found:', color=16742144)
            aNum = 0
            for human in findList:
                userFindEmbed.add_field(name=('#' + str(aNum + 1)) + ':', value=human, inline=True)
                aNum += 1
            await ctx.send(embed=userFindEmbed)
            return
        #PROGRAM STUFF HERE
        if theID != '':
            await ctx.send(('<@' + str(theID)) + '>')

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def findid(self, ctx, *user: str):
        '''Returns server ID and user ID.'''
        guild = ctx.guild.id
        member = ctx.author.id
        arg = ''
        for item in user:
            arg = (arg + item) + ' '
        arg = arg[:len(arg) - 1]
        theID = ''  
        if arg != '':
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
                    member = findIDList[0]
                else:
                    await ctx.send('Multiple people found. Pick someone specific next time.')
                    userFindEmbed = discord.Embed(title='Users Found:', color=16742144)
                    aNum = 0
                    for human in findList:
                        userFindEmbed.add_field(name=('#' + str(aNum + 1)) + ':', value=human, inline=True)
                        aNum += 1
                    await ctx.send(embed=userFindEmbed)
                    return
            if self.bot.get_guild(guild).get_member(member) is None:
                await ctx.send('Invalid user, try again.')
            else:
                theID = member
        else:
            theID = ctx.author.id
        await ctx.send('Server: ' + str(ctx.guild.id))
        await ctx.send('Member: ' + str(theID))
        await ctx.send('Channel: ' + str(ctx.channel.id))

    @commands.command(description="Make an Embed with the info given. Use RRRGGGBBB format for color (0-256 for R, 0-256 for G, etc.), and name::value format for fields.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def embed(self, ctx, myTitle = "", myDescription= "", myColor = 0x000000, *nameValue):
        """Creates an Embed with the info given."""
        myNames = []
        myValues = []
        for item in nameValue:
            try:
                (myName, myValue) = map(str, item.split('::'))
                myNames.append(myName)
                myValues.append(myValue)
            except:
                pass
                
        try:
            myEmbed=discord.Embed(title=myTitle, description=myDescription, color=myColor)
        except:
            myEmbed=discord.Embed(title=myTitle, description=myDescription, color=0x000000)
        x=0
        for item in myNames:
            myEmbed.add_field(name=item, value=myValues[x], inline=False)
            x+=1
        await ctx.send(embed=myEmbed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def help(self, ctx, *commands : str):
        """Shows this message."""
        await ctx.send("Sorry, the `help` command is disabled for the time being! You'll have to wait for an update for that. In the meantime, check my GitHub if you *really* have to know a command name. Or just ask me, and I'll check GitHub.") 
        """
        bot = self.bot
        destination = ctx.message.author if bot.dm_help else ctx.message.channel
        pageNum = 1
        if len(commands) == 1:
            try:
                pageNum = int(commands[0])
                commands = []
            except:
                pass
        pageNum -=1
        
        _mentions_transforms = {'@everyone': '@\u200beveryone','@here': '@\u200bhere'}
        _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))
        def repl(obj):
            return _mentions_transforms.get(obj.group(0), '')
        # help by itself just lists our own commands.
        if len(commands) == 0:
            pages = await bot.formatter.format_help_for(ctx, bot)
        elif len(commands) == 1:
            # try to see if it is a cog name
            name = _mention_pattern.sub(repl, commands[0])
            command = None
            if name in bot.cogs:
                command = bot.cogs[name]
            else:
                command = bot.all_commands.get(name)
                if command is None:
                    await destination.send(bot.command_not_found.format(name))
                    return
            pages = await bot.formatter.format_help_for(ctx, command)
        else:
            name = _mention_pattern.sub(repl, commands[0])
            command = bot.all_commands.get(name)
            if command is None:
                await destination.send(bot.command_not_found.format(name))
                return
            for key in commands[1:]:
                try:
                    key = _mention_pattern.sub(repl, key)
                    command = command.all_commands.get(key)
                    if command is None:
                        await destination.send(bot.command_not_found.format(key))
                        return
                except AttributeError:
                    await destination.send(bot.command_has_no_subcommands.format(command, key))
                    return
            pages = await bot.formatter.format_help_for(ctx, command)
        if bot.dm_help is None:
            characters = sum(map(len, pages))
            # modify destination based on length of pages.
            if characters > 1000:
                destination = ctx.message.author
        myEmbed = discord.Embed(title="sawickipedia.exe Help", description=str(pages[pageNum]))
        myEmbed.set_footer(text="Page " + str(pageNum+1) + "/" + str(len(pages)))
        await ctx.send(embed=myEmbed)
        """

    @commands.command(name = "convert-to-owo", aliases = ["OWO", "OwO", "converttoowo", "convert-to-OwO", "converttoOwO", "owo"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def convertToOwo(self, ctx, *, toConvert : str):
        """A disgusting command. I don't even know why this needs to exist."""
        newStr = ''
        for letter in toConvert:
            if letter == 'a':
                newStr = newStr + 'awa'
            elif letter == 'e':
                newStr = newStr + 'ewe'
            elif letter == 'i':
                newStr = newStr + 'iwi'
            elif letter == 'o':
                newStr = newStr + 'owo'
            elif letter == 'u':
                newStr = newStr + 'uwu'
            elif letter == 'A':
                newStr = newStr + 'AWA'
            elif letter == 'E':
                newStr = newStr + 'EWE'
            elif letter == 'I':
                newStr = newStr + 'IWI'
            elif letter == 'O':
                newStr = newStr + 'OWO'
            elif letter == 'U':
                newStr = newStr + 'UWU'
            else:
                newStr = newStr + letter
        embed = discord.Embed(title=str(ctx.author) + "'s Horrible Translation", description = newStr, color=0xDC143C)
        await ctx.send(embed = embed)
    
    
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def makeBCA(self, ctx, *, userInput : str):
        """Creates a BCA table based on your input. Use ?makeBCA help to see how to format it properly."""
        
        if userInput != "help":
            try:
                #Load data & configure user input
                pData = json.load(open("periodictable.json", "r"))
                temp = userInput.split("|")
                userMass = temp[1]
                
                #Sigfig rounding function
                round_to_n = lambda x, n: round(x, -int(math.floor(math.log10(x))) + (n - 1))
                
                #Data configuration
                temp = temp[0].split("->")
                reactants = temp[0].split("+")
                products = temp[1].split("+")
                compounds = []
                coefficients = []
                molarmass = []
          
                #Split input into coefficient and compound lists
                for item in reactants:
                    item = item.strip()
                    try:
                        coefficients.append(int(item[0]))
                        item = item[1:]
                    except:
                        coefficients.append(1)
                    compounds.append(item)
                for item in products:
                    item = item.strip()
                    try:
                        coefficients.append(int(item[0]))
                        item = item[1:]
                    except:
                        coefficients.append(1)
                    compounds.append(item)
                  
                #Gets the molar mass of each compound, and adds that to the list
                for compound in compounds:
                    #Ensures that subscripts + parentheses work right (nested parentheses do NOT work)
                    newStr = ""
                    paren = False
                    x = 0
                    while x < len(compound):
                        if compound[x] == "(":
                            paren = True
                            compound = compound[:x] + compound[x+1:]
                            x -= 1
                        elif paren:
                            if compound[x] != ")":
                                newStr += compound[x]
                            else:
                                paren = False
                                compound = compound[:x] + (newStr * (int(compound[x+1])-1)) + compound[x+2:]
                                print(compound)
                                x -= 1
                                x += len(newStr)
                                newStr = ""
                        x += 1
                    elements = re.findall('[A-Z][^A-Z]*', compound)
                    totalMass = 0.0
                    for element in elements:
                        head = element.rstrip('0123456789')
                        tail = element[len(head):]
                        items = head, tail
                        
                        for element in pData:
                            if element["symbol"] == items[0]:
                                mass = float(element["atomicMass"].split("(")[0])
                        if items[1] == "":
                            totalMass += mass
                        else:
                            totalMass += mass * int(items[1])
                            
                    molarmass.append(totalMass)
                
                #Changes the user-inputted mass into something more useful. Also finds the correct amount of sigfigs for later
                userMass = userMass.split("->")
                newMass = []
                for item in userMass:
                    for thing in item.split("+"):
                        newMass.append(thing.strip())
                temp = 0
                for item in newMass:
                    if item != "x" and item != "xs":
                        temp += 1
                
                for thing in newMass:
                    if thing != "x" and thing != "xs":
                        sample = thing[:len(thing)-1]
                        sigfigs = self.find_sigfigs(sample)
                
                #Creates data for later
                known = ""
                changes = [0] * len(coefficients)
                before = list(changes)
                after = list(changes)
                limitingReactant = "None"
                #Converts the known mass to moles
                loc = 0
                for item in newMass:
                    if item != "x" and item != "xs":
                        known = item
                        limitingReactant = loc
                        break
                    loc += 1
                if known[len(known)-1] == "g":
                    known = float(known[:len(known)-1])
                    known = known / molarmass[loc]
                    known = round_to_n(known, sigfigs)
                elif known[len(known)-1] == "m":
                    known = float(known[:len(known)-1])
                else:
                    await ctx.send("Error! Make sure your given masses end in either g or m!")
                    return
                
                
                #Finds the proper data for the changes list
                x = 0
                for y in range(0, len(changes)):
                    if x != loc:
                        changes[y] = known * float(coefficients[x] / coefficients[loc])
                    else:
                        changes[y] = known
                    x += 1
                
                #Rounds the changes list, and then puts the proper data in the before and after lists. Also makes changes negative if needed
                for num in range(0, len(changes)):
                    changes[num] = round_to_n(changes[num], sigfigs)
                for num in range(0, len(reactants)):
                    toAdd = newMass[num]
                    if toAdd[len(toAdd)-1] == "g":
                        toAdd = float(toAdd[:len(toAdd)-1])
                        toAdd = toAdd / molarmass[num]
                        toAdd = round_to_n(toAdd, sigfigs)
                    elif toAdd[len(toAdd)-1] == "m":
                        toAdd = float(toAdd[:len(toAdd)-1])
                    elif toAdd != "x" and toAdd != "xs":
                        await ctx.send("Error! Make sure your given masses end in either g or m!")
                        return
                    before[num] = toAdd
                    changes[num] = -1 * changes[num]
                for num in range(0, len(changes)):
                    if before[num] != "xs":
                        after[num] = before[num] + changes[num]
                    else:
                        after[num] = before[num] + str(changes[num])
                for num in range(0, len(after)):
                    try:
                        after[num] = float(after[num])
                        if after[num] > 0:
                            after[num] = round_to_n(after[num], sigfigs)
                    except:
                        newStr = after[num][3:]
                        after[num] = "xs-" + str(round_to_n(float(newStr), sigfigs))
                
                #If there are two givens, this repeats the earlier process (from converting mass to moles and down), but with the second given.
                if temp == 2:
                    loc = 0
                    second = False
                    for item in newMass:
                        if item != "x" and item != "xs" and second:
                            known = item
                            limitingReactant = loc
                            break
                        elif item != "x" and item != "xs":
                            second = True
                        loc += 1
                    if known[len(known)-1] == "g":
                        known = float(known[:len(known)-1])
                        known = known / molarmass[loc]
                        known = round_to_n(known, sigfigs)
                    elif known[len(known)-1] == "m":
                        known = float(known[:len(known)-1])
                    else:
                        await ctx.send("Error! Make sure your given masses end in either g or m!")
                        return
                    
                    if known + changes[loc] < 0:
                        x = 0
                        for y in range(0, len(changes)):
                            if x != loc:
                                changes[y] = known * float(coefficients[x] / coefficients[loc])
                            else:
                                changes[y] = known
                            x += 1
                            
                        for num in range(0, len(changes)):
                            changes[num] = round_to_n(changes[num], sigfigs)
                        for num in range(0, len(reactants)):
                            toAdd = newMass[num]
                            if toAdd[len(toAdd)-1] == "g":
                                toAdd = float(toAdd[:len(toAdd)-1])
                                toAdd = toAdd / molarmass[num]
                                toAdd = round_to_n(toAdd, sigfigs)
                            elif toAdd[len(toAdd)-1] == "m":
                                toAdd = float(toAdd[:len(toAdd)-1])
                            elif toAdd != "x" and toAdd != "xs":
                                await ctx.send("Error! Make sure your given masses end in either g or m!")
                                return
                            before[num] = toAdd
                            changes[num] = -1 * changes[num]
                        for num in range(0, len(changes)):
                            if before[num] != "xs":
                                after[num] = before[num] + changes[num]
                            else:
                                after[num] = before[num] + str(changes[num])
                        for num in range(0, len(after)):
                            try:
                                after[num] = float(after[num])
                                if after[num] > 0:
                                    after[num] = round_to_n(after[num], sigfigs)
                            except:
                                newStr = after[num][3:]
                                after[num] = "xs-" + str(round_to_n(float(newStr), sigfigs))
               
                #Error handling!
                if temp > 2:
                    await ctx.send("Error! Too many givens! Make sure you have a maximum of two given masses in your data! (The part after the '|') ")
                    return
               
                #Puts the "xs" in the list, since we need that for the table
                x = 0
                for item in newMass:
                    if item == "xs":
                        before[x] = "xs"
                        after[x] = "xs" + str(changes[x])
                    x += 1
                    
                    
                
                #Formats things
                prettyBefore  = []
                prettyChanges = []
                prettyAfter   = []
                for x in range(0, len(before)):
                    if before[x] == "xs":
                        prettyBefore.append("xs")
                    else:
                        try:
                            prettyBefore.append(str(float(before[x])))
                            if self.find_sigfigs(prettyBefore[x]) < sigfigs:
                                prettyBefore[x] += "0" * (sigfigs - self.find_sigfigs(prettyBefore[x]))
                        except:
                            pass
                for x in range(0, len(changes)):
                    try:
                        prettyChanges.append(str(float(changes[x])))
                        if self.find_sigfigs(prettyChanges[x]) < sigfigs:
                            prettyChanges[x] += "0" * (sigfigs - self.find_sigfigs(prettyChanges[x]))
                    except:
                        pass
                    if x >= len(reactants):
                        prettyChanges[x] = "+" + prettyChanges[x]
                for x in range(0, len(after)):
                    if str(after[x])[:2] == "xs":
                        prettyAfter.append(after[x])
                    else:
                        try:
                            prettyAfter.append(str(float(after[x])))
                            if self.find_sigfigs(prettyAfter[x]) < sigfigs:
                                prettyAfter[x] += "0" * (sigfigs - self.find_sigfigs(prettyAfter[x]))
                        except:
                            pass
                  
                gramsAfter = []
                for x in range(0, len(after)):
                    if prettyAfter[:2] == "xs":
                        gramsAfter.append("N/A")
                    else:
                        try:
                            gramVal = float(after[x]) * molarmass[x] 
                            if gramVal > 0:
                                gramVal = round_to_n(gramVal, sigfigs)
                            try:
                                gramsAfter.append(str(float(gramVal)))
                                if self.find_sigfigs(gramsAfter[x]) < sigfigs:
                                    gramsAfter[x] += "0" * (sigfigs - self.find_sigfigs(gramsAfter[x]))
                            except:
                                gramsAfter.append("N/A")
                        except:
                            gramsAfter.append("N/A")
                          
                print(gramsAfter)   
                #Data table
                pTable = PrettyTable()
                pTable.field_names = [""] + reactants + products
                pTable.add_row(["Before:"] + prettyBefore)
                pTable.add_row(["Change:"] + prettyChanges)
                pTable.add_row(["After:"] + prettyAfter)
                pTable.add_row([""] + [""]*len(prettyBefore))
                pTable.add_row(["After (g):"] + gramsAfter)
                pTable.add_row(["Molar Mass:"] + molarmass)
                pTable.align = "r"
                
                #Embed creation
                BCAembed=discord.Embed(title="Equation: `" + userInput.split("|")[0] + "`", description="```\n" + str(pTable) + "\n```", color = 0x00FF00)
                BCAembed.set_author(name=ctx.message.author.name + "'s BCA Table", icon_url=ctx.message.author.avatar_url)
                BCAembed.set_footer(text="Make sure you entered information correctly! I can't check your work for you. Use ?makeBCA help for more information.")
                if limitingReactant != "None":
                    BCAembed.add_field(name="Limiting Reactant:", value=compounds[limitingReactant])
                else:
                    BCAembed.add_field(name="Limiting Reactant:", value=limitingReactant)
                await ctx.send(embed=BCAembed)
            except Exception as e:
                await ctx.send("Uh oh! An error occurred! Make sure you inputted your data correctly! If you're 100% sure you didn't make a mistake, contact my master with this error code:")
                await ctx.send("```css\n[" + str(e) + "]\n```")
        else:
            #Help function
            descriptionStr = """
                             Input a *balanced* chemical equation, along with the known masses, and this command will give you a BCA table for it!
                             **Format:** `Reactant1 + Reactant2 -> Product1 + Product2 | 1stMass + 2ndMass -> 3rdMass + 4thMass`
                             **Example:** `Cu + 2AgNO3 -> 2Ag + Cu(NO3)2 | 2.93g + 1.41g -> x + x`
                             If you do not know a mass, put `x` instead of a mass. If it's the excess reactant, make it `xs` instead.
                             **Advice:**
                             -Don't forget to put `g` or `m` after the mass depending on if it's grams or moles!
                             -Double check your input! I don't check your correctness when I calculate things.
                             -If things aren't capitalized right, then this function will not work as expected.
                             -Coefficients go at the beginning of each compound, and the subscripts go at the end/middle.
                             -Use parentheses to signify nested coefficients.
                             -This function works with any number of reactants and products!
                             -Enter Sig Figs correctly; this function takes them into account.
                             """
            
            BCAembed=discord.Embed(title="How to format this command:", description=descriptionStr, color = 0x00FF00)
            BCAembed.set_author(name=ctx.message.author.name + "'s BCA Table Help", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=BCAembed)



























def setup(bot):
    bot.add_cog(Misc(bot))