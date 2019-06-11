#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands
import asyncio
import os
import json
import random



class Misc(commands.Cog):
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
        if user[0] == "<":
            if user[0:3] == "<@!":
                member = ctx.guild.get_member(int(user[3:len(user)-1]))
            else:
                member = ctx.guild.get_member(int(user[2:len(user)-1]))
            if member is not None:
                return member
        
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
    
    
    
    @commands.command()
    @commands.check(check_owner)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ownertest(self, ctx):
        '''Checks if you're the owner of the server'''
        my_file = open("botdata" + os.sep + "devs.txt", "r")
        devs = my_file.read().split("\n")
        if ctx.author.id in devs:
            await ctx.send("The owner here is {}, sir. *Do what you must with that information.*".format(str(ctx.guild.owner)))
        else:
            await ctx.send("Yes, you are the owner here. *Don't let the peasants revolt.*")
    
    @commands.command()
    @commands.check(check_admin)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def admintest(self, ctx):
        '''Checks if you have administrator privileges in the server'''
        if ctx.guild.owner == ctx.message.author:
            await ctx.send("Congratulations on being an admin. And an owner. *How does it feel being better than everyone else?*")
        else:
            await ctx.send("Congratulations on being an admin. *You better hope you don't lose those privileges.*")
    
    @commands.command(aliases = ["moderatortest"])
    @commands.check(check_moderator)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def modtest(self, ctx):
        '''Checks if you're a moderator in the server'''
        if ctx.author.guild_permissions.administrator:
            await ctx.send("*Hey, you're a moderator here! Also an admin. *You're better than the other mods, aren't you? Do you enjoy that?*")
        await ctx.send("Hey, you're a moderator here! *How does it feel being a lesser admin?*")
    
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mentionuser(self, ctx, *, user : str):
        '''Mentions the inputted user (accepts mentions, names, nicknames, and portions of each)'''
        member = await self.get_users(ctx, user)
        if member == None:
            return
        await ctx.send(member.mention)
        
        
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
                    my_roll = random.randint(1, limit)
                    if r == 0:
                        result = str(my_roll)
                    else:
                        result = (result + ', ') + str(my_roll)
                    total = total + my_roll
                await ctx.send(result)
                await ctx.send('The total of your rolls is: ' + str(total))
            else:
                await ctx.send(random.randint(1, limit))

    @commands.command(description='Have as many options as you want after "?choose", with a space in between each one. One will be randomly chosen.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def choose(self, ctx, *choices: str):
        '''Chooses a random argument you give.'''
        new_choice = random.choice(choices)
        choice_embed = discord.Embed(title=str(ctx.author) + "'s Choices", description = new_choice, color=0x00FF00)
        await ctx.send(embed=choice_embed)
    
    
    
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def findid(self, ctx, *, user : str = None):
        if user == None:
            member = ctx.author
        else:
            member = await self.get_users(ctx, user)
        my_embed = discord.Embed(title="User Data", description = "Server: {} \n Channel: {} \n Member: {}".format(str(ctx.guild.id), str(ctx.channel.id), str(member.id)))
        my_embed.set_author(name=str(member), icon_url=member.avatar_url)
        await ctx.send(embed=my_embed)
    
    
    @commands.command(description="Make an Embed with the info given. Use RRRGGGBBB format for color (0-256 for R, 0-256 for G, etc.), and name::value format for fields.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def embed(self, ctx, my_title = "", my_description= "", my_color = 0x000000, *name_value):
        """Creates an Embed with the info given."""
        my_names = []
        my_values = []
        for item in name_value:
            try:
                (my_name, my_value) = map(str, item.split('::'))
                my_names.append(my_name)
                my_values.append(my_value)
            except:
                pass
                
        try:
            my_embed=discord.Embed(title=my_title, description=my_description, color=my_color)
        except:
            myEmbed=discord.Embed(title=my_title, description=my_description, color=0x000000)
        x=0
        for item in my_names:
            my_embed.add_field(name=item, value=my_values[x], inline=False)
            x+=1
        await ctx.send(embed=my_embed)
    
    
    @commands.command(name = "convert-to-owo", aliases = ["OWO", "OwO", "converttoowo", "convert-to-OwO", "converttoOwO", "owo"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def convert_to_owo(self, ctx, *, to_convert : str):
        """A disgusting command. I don't even know why this needs to exist."""
        new_str = ''
        for letter in to_convert:
            if letter == 'a':
                new_str = new_str + 'awa'
            elif letter == 'e':
                new_str = new_str + 'ewe'
            elif letter == 'i':
                new_str = new_str + 'iwi'
            elif letter == 'o':
                new_str = new_str + 'owo'
            elif letter == 'u':
                new_str = new_str + 'uwu'
            elif letter == 'A':
                new_str = new_str + 'AWA'
            elif letter == 'E':
                new_str = new_str + 'EWE'
            elif letter == 'I':
                new_str = new_str + 'IWI'
            elif letter == 'O':
                new_str = new_str + 'OWO'
            elif letter == 'U':
                new_str = new_str + 'UWU'
            else:
                new_str = new_str + letter
        embed = discord.Embed(title=str(ctx.author) + "'s Horrible Translation", description = new_str, color=0xDC143C)
        await ctx.send(embed = embed)
    
    
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def makeBCA(self, ctx, *, userInput : str):
        """Creates a BCA table based on your input. Use ?makeBCA help to see how to format it properly."""
        #Yes, I know this is using camelCase. I'm not rewriting it; it was a convoluted experiment. Use at your own risk.
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