#Save as battle.py
from player import Player
from enemy import Enemy


#Enemy Dictionary- Contains all of the info about the enemies in the game, to be input into the class
#Format: "Enemy_Name: [healthPoints, attackPower]"
enemy_dictionary = {
    "Default_Enemy": [5, 1],
    "Test_Enemy": [7, 2],
    
    }

class Battle():

    def __init__(self, player1, enemyType1 = "Default_Enemy"):
        enemyList1 = enemy_dictionary[enemyType1]
        self.enemy1 = Enemy(enemyList1[0], enemyList1[1])
        self.player1 = player1

    def player1Turn(self):
        exitLoop = False
        while exitLoop == False:
            try:
                menuSelection = int(raw_input("What menu item?"))
                if menuSelection == 1:
                    self.enemy1.getDamaged(self.player1.attackEnemy())
                    print "Player 1 does things!"
                    exitLoop = True
                else:
                    print "Not a Vaild Selection, Try again!"
            except:
                print "Not a Valid Selection, Try again!"
        

    def enemy1Turn(self):
        self.player1.getDamaged(self.enemy1.attackPlayer())
        print "Enemy 1 does things!"

    def printMenu(self, playerTurn):
        #Battle Menu Dictionary- This is what the player chooses from to attack, defend, use an item, etc.
        battle_menu = {
        "player1HP":"Player 1 HP: "+str(self.player1.hitPoints),
        "enemy1HP":"Enemy 1 HP: "+str(self.enemy1.hitPoints),


        }
        #Prints Battle Menu
        for item in battle_menu:
            print battle_menu[item]

     
    def doBattle(self):
        exitLoop = False
        winner = 0
        turnNumber = 1
        while exitLoop != True:
            #Takes a turn
            if turnNumber == 1:
                self.printMenu(True)
                self.player1Turn()
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
        print "Winner: " + str(winner)
            
