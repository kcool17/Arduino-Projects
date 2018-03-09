import urllib.request
import random
import ast
import html.parser
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

rawData = str(urllib.request.urlopen(url).read())
rawCategory = html_parser.unescape(getInfo(rawData, 'category":"', '","type'))
rawType = getInfo(rawData, '"type":"', '","difficulty')
rawDifficulty = getInfo(rawData, '"difficulty":"', '","question"')
rawQuestion = html_parser.unescape(getInfo(rawData, '"question":"', '","correct_answer"'))
rawCorrect = html_parser.unescape(getInfo(rawData, '"correct_answer":', ',"incorrect_answers"'))
rawCorrect = ast.literal_eval(rawCorrect)
rawIncorrect = html_parser.unescape(getInfo(rawData, '"incorrect_answers":', "}]}'"))
rawIncorrect = ast.literal_eval(rawIncorrect)
#Display info/question:
print("Category: " + rawCategory + ", Difficulty: " + rawDifficulty.capitalize())
print("Question: " + rawQuestion)
print()
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
                print(letter+ ": " + rawCorrect)
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
                    print(letter+ ": " + rawIncorrect[x-1])
                else:
                    print(letter+ ": " + rawIncorrect[x])

        #Get user guess
        print("What is your guess?")
        guess = input().lower()
        while guess !="1" and guess !="2" and guess !="3" and guess !="4" and guess !="a" and guess !="b" and guess !="c" and guess !="d":
            print("Guess again! That's not a valid input!")
            guess = input()
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
            
        #Determine if user is right
        if guess == correctLoc:
            print("Correct!")
        else:
            print("Wrong! The right answer was: " + correctLetter + ": " + rawCorrect)
    else: #Multiple answers possible
        print("Sorry! An error occurred. Please try asking again! Error: -2")
        
elif rawType == 'boolean': # True/False
    #Display answers
    print("A. True")
    print("B. False")
    #Get user guess
    print("What is your guess?")
    guess = input().lower()
    while guess !="1" and guess !="2" and guess !="t" and guess !="f" and guess !="true" and guess != "false" and guess !="a" and guess != "b":
        print("Guess again! That's not a valid input!")
        guess = input()
    if guess == "1" or guess == "t" or guess == "true" or guess == "a":
        guess = "true"
    else:
        guess = "false"
    #Determine if user is right
    if guess == rawCorrect.lower():
        print("Correct!")
    else:
        print("Wrong!")
else:
    print("Sorry! An error occurred. Please try asking again! Error: -1")
    

    
        
