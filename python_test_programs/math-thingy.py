from fractions import Fraction
def mathThing(n):
    myVar = 0.0
    for x in range(1, n+1):
        myFact = 1.0
        for y in range(1,  x+2):
            myFact = myFact * y
        myVar = myVar + (x / myFact)
    return Fraction(myVar).limit_denominator()

for x in range(1, 100):
    print(mathThing(x))
