#Save as battle.py
from player import Player
from enemy import Enemy
import time
import random
import os

#Enemy Dictionary- Contains all of the info about the enemies in the game, to be input into the class
#Format: "Enemy_Name: [healthPoints, attackPower]"
enemy_dictionary = {
    "Default_Enemy": ["Defaulter", 5, 2],
    "Test_Enemy": ["TestThingy", 7, 2],
    "Weak_Enemy": ["George, the Standard Monkey", 10, 2],
    "Strongish_Enemy": ["Bill, the Hu-man", 15, 3],
    "Equal_Enemy": ["GLaDOS, the Sentient AI", 30, 3],
    "Super_Enemy": ["Smaug, the Dragon", 40, 4],
    "OP_Enemy": ["Ganon, the Calamity", 50, 5],
    "Me_Enemy": ["Dr. Sawickipedia, the Winner", 100, 10],
    }

class Battle():

    def __init__(self, player1, enemyType1 = "Default_Enemy"):
        enemyList1 = enemy_dictionary[enemyType1]
        self.enemy1 = Enemy(enemyList1[0], enemyList1[1], enemyList1[2])
        self.player1 = player1
        print("You'll be fighting " + self.enemy1.name + "!")
        print()
        time.sleep(1)

    def player1Turn(self): #Player's turn
        exitLoop = False
        #Checks for status effects:
        if self.player1.regenTurns>0:
            self.player1.regenTurns-=1
            self.player1.getHealed(5)
            time.sleep(0.5)
            print()
            print("You healed 5 HP!")
        if self.player1.attUpTurns>0:
            self.player1.attUpTurns-=1
            self.player1.attackPower = self.player1.startAttackPower + 1
            print()
            print("Attack up this turn!")
        else:
            self.player1.attackPower = self.player1.startAttackPower
        
            
        time.sleep(0.5)
        while exitLoop == False:
            print()
            try:
                menuSelection = int(input("What menu item?"))
                if menuSelection == 1: #If player decides to attack
                    attackPow = self.player1.attackEnemy()
                    self.enemy1.getDamaged(attackPow)
                    time.sleep(1.5)
                    print()
                    print("You deal " + str(attackPow) + " damage!")
                    print()
                    time.sleep(1.5)
                    exitLoop = True
                elif menuSelection == 2: #If player decides to use an item
                    print()
                    print("1. Healing Potions: " + str(self.player1.inventory["healPot"]))
                    print("2. Regeneration Potions: " + str(self.player1.inventory["regenPot"]))
                    print("3. Defense Potions: " + str(self.player1.inventory["defPot"]))
                    print("4. Attack Potions: " + str(self.player1.inventory["attackPot"]))
                    print("5. Full Heal Potions: " + str(self.player1.inventory["superHealPot"]))
                    print("6. Go Back")
                    print()
                    choseItem = False
                    while not choseItem:
                        userInput = input("What item do you want to use?")
                        try:
                            userInput = int(userInput)
                            time.sleep(1.5)
                            if userInput < 1 or userInput > 6:
                                print("Not a valid option, please try again.")
                            elif userInput == 1: #1. Healing Potion
                                if self.player1.removeInventory("healPot"):
                                    if self.player1.hitPoints == self.player1.maxHitPoints:
                                        print("You're already at max HP! Do something else.")
                                    elif self.player1.getHealed(10):
                                        print("Healed to Max!")
                                        choseItem = True
                                    else:
                                        print("Healed 10 HP!")
                                        choseItem = True
                                else:
                                    print("You don't have any!")
                            elif userInput == 2: #2. Regeneration Potion
                                if self.player1.removeInventory("regenPot"):
                                    self.player1.regenTurns = 2
                                    choseItem = True
                                else:
                                    print("You don't have any!")
                            elif userInput == 3: #3. Defense Potion
                                if self.player1.removeInventory("defPot"):
                                    self.player1.defUpTurns = 2
                                    choseItem = True
                                else:
                                    print("You don't have any!")
                            elif userInput == 4: #4. Attack Potion
                                if self.player1.removeInventory("attackPot"):
                                    self.player1.attUpTurns = 2
                                    choseItem = True
                                else:
                                    print("You don't have any!")
                            elif userInput == 5: #6. Max Healing Potion
                                if self.player1.removeInventory("superHealPot"):
                                    if self.player1.hitPoints == self.player1.maxHitPoints:
                                        print("You're already at max HP! Do something else.")
                                    else:
                                        self.player1.getHealed(0, True)
                                        print("Healed to Max!")
                                        choseItem = True
                                else:
                                    print("You don't have any!")
                            else:#Exit out of inventory
                                print("Exiting inventory...")
                                break
                        except:
                             print("Invalid input, please try again!")
                    time.sleep(1.5)
                    if choseItem:
                        exitLoop = True
                    else:
                        self.printMenu(True)

                elif menuSelection == 3: #Attempt to flee the battle (50% chance)
                    time.sleep(2)
                    didFlee = random.choice([0, 1])
                    if didFlee == 1:
                        return True
                    else:
                        print("You failed. You're stuck here.")
                        exitLoop = True
                elif menuSelection == 4: #Do nothing
                    time.sleep(1)
                    print("Probably not the best decision, but you did nothing here.")
                    exitLoop = True
                else:
                    print("Not a Vaild Selection, Try again!")
            except:
                print("Invalid Selection, Try again!")
        

    def enemy1Turn(self): #Enemy's turn
        #Checks for status effects:
        if self.player1.defUpTurns>0:
            self.player1.defUpTurns-=1
            self.enemy1.attackPower = self.enemy1.startAttackPower - 1
            print()
            print("Defense up this turn!")
        else:
            self.enemy1.attackPower = self.enemy1.startAttackPower
            
        attackPow = self.enemy1.attackPlayer()
        self.player1.getDamaged(attackPow)
        time.sleep(1.5)
        print()
        print(self.enemy1.name + " deals " + str(attackPow) + " damage!")
        print()
        time.sleep(1.5)

    def printMenu(self, playerTurn):
        if playerTurn: turnDisp = "Player"
        else: turnDisp = "Enemy"
        #Battle Menu Dictionary- This is what the player chooses from to attack, defend, use an item, etc.
        battle_menu = {
        "turn":"Turn: " + turnDisp,
        "player1HP":"Player 1 HP: "+str(self.player1.hitPoints) + "/" + str(self.player1.maxHitPoints),
        "enemy1HP":self.enemy1.name + " HP: "+str(self.enemy1.hitPoints) + "/" + str(self.enemy1.maxHitPoints),
        "optionTitle":"----OPTIONS----",
        "attack":"1. Attack Enemy",
        "itemUse":"2. Use Item",
        "tryFlee":"3. Try to Flee",
        "doNothing":"4. Do Nothing",
        }
        #Prints Battle Menu
        print ("~" * 25)
        if playerTurn:
            for item in battle_menu:
                print(battle_menu[item])
        else:
            print(battle_menu["turn"])
            print(battle_menu["player1HP"])
            print(battle_menu["enemy1HP"])
     
    def doBattle(self):
        exitLoop = False
        winner = 0
        turnNumber = 1
        while exitLoop != True:
            #Takes a turn
            if turnNumber == 1:
                self.printMenu(True)
                if self.player1Turn():
                    print("You ran away.")
                    time.sleep(1)
                    return 2
                turnNumber= turnNumber + 1
            elif turnNumber == 2:
                self.printMenu(False)
                self.enemy1Turn()
                turnNumber = 1
                
            #Checks for winner
            if self.player1.lostBattle() == True and self.enemy1.lostBattle() == True:
                exitLoop = True
                winner = 0
                break
            elif self.player1.lostBattle() == True:
                exitLoop = True
                winner = 2
                break
            elif self.enemy1.lostBattle() == True:
                exitLoop = True
                winner = 1
                break
        if winner == 1:
            print("You won!")
            time.sleep(1)
            return True
        elif winner == 2:
            print("You lost.")
            time.sleep(1)
            return False
            
