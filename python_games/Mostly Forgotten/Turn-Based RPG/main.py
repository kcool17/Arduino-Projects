"""
Turn-Based RPG- By: Kyle Sawicki
-----------------------------------------------------------------
In this game, you are a person who starts with 30 HP and 2 ATK
You have to try and beat as many enemies as you can, before getting a Game Over
On your turn, choose an option for what to do.
You can attack, flee, or use an item.
Good luck! Try and beat as many enemies as you can!
-----------------------------------------------------------------

"""
#Save as main.py
from battle import Battle
from player import Player
import random
import time

#Create a player
#Format: Player(hitPoints, attackPower)
player1 = Player(30, 2)
#Enemy list (Note: multiple instances of the same enemy is designed to make it more common than others):
enemyList = ["Weak_Enemy", "Weak_Enemy", "Weak_Enemy", "Weak_Enemy", "Weak_Enemy",
             "Strongish_Enemy", "Strongish_Enemy", "Strongish_Enemy", "Strongish_Enemy",
             "Equal_Enemy", "Equal_Enemy", "Equal_Enemy",
             "Super_Enemy", "Super_Enemy",
             "OP_Enemy", "OP_Enemy",
             "Me_Enemy",
             ]
#Starting Items:
player1.inventory["healPot"] = 3
player1.inventory["regenPot"] = 2
player1.inventory["defPot"] = 2
player1.inventory["attackPot"] = 2
player1.inventory["superHealPot"] = 1


#Instructions:
print("Instructions")
print("In this game, you are a person who starts with 30 HP and 2 ATK.")
print("You have to try and beat as many enemies as you can, before getting a Game Over.")
print("On your turn, choose an option for what to do.")
print("You can attack, flee, or use an item.")
print("Good luck! Try and beat as many enemies as you can!")
time.sleep(5)
#Battles
done = False
lives = 3
wins = 0
while not done:#Main Loop
    #Start Battle
    theEnemy = random.choice(enemyList)
    time.sleep(1)
    print()
    print("Lives: " + str(lives))
    print("Level: " + str(wins))
    time.sleep(1)
    print("Ready to fight?")
    time.sleep(1)
    myBattle = Battle(player1, theEnemy)
    result = myBattle.doBattle()
    if not result:#Lost
        print("Uh, oh! You lose one life!")
        lives -= 1
        player1.getHealed(0, True)
    elif result == True:#Won
        print("Nice! you leveled up! Also, 10 more HP, and 1 more ATK!")
        player1.maxHitPoints +=10
        player1.attackPower +=1
        player1.getHealed(10)
        wins+=1
    else:#Flee
        print("You ran away. Nothing for you.")
    if lives == 0:#Game over
        time.sleep(2)
        print("Game Over! You beat " + str(wins) + " enemies!")
        userInput = input("Play again? (y/n)")
        if userInput.lower() != "y" or userInput.lower != "yes":
            done = True





