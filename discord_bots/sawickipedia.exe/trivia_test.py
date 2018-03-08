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

if rawType == 'multiple':
    if type(rawCorrect) is str: #Standard multiple choice
        #Display Question
        print(rawQuestion)
        print()
        #Display Answers
        correct = random.randint(0, len(rawIncorrect))
        correctSaid = False
        for x in range(0, len(rawIncorrect)+1):
            if x == correct:
                print(str(x+1)+ ": " + rawCorrect)
                correct = 100
                correctSaid = True
            else:
                if correctSaid:
                    print(str(x+1)+ ": " + rawIncorrect[x-1])
                else:
                    print(str(x+1)+ ": " + rawIncorrect[x])
            
    else: #Multiple answers possible
        foo = 0
        
    
print()
print(rawCorrect)
print(rawIncorrect)
    
        
