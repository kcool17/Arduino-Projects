from fractions import Fraction
def mathThingy(n):
    myVar = 0.0
    for x in range(1, n+1):
        myFact = 1.0
        for y in range(1,  x+2):
            myFact = myFact * y
        myVar = myVar + (x / myFact)
    return Fraction(myVar).limit_denominator()

def mathThingy2(x, y, n):
    total = 0
    for myPow in range(0, n):
        total = total + (pow(x, n) * pow(y, myPow))
    return total

def mathThingy3(n):
    total = 0
    for num in range(1, n + 1):
        print(pow(num, 4))
        total = total + pow(num, 4)
    return total


for x in range(1, 10):
    print("____________________________")
    print(mathThingy3(x))

