#Save as battle.py
from player import Player
from enemy import Enemy

#Battle Menu Dictionary- This is what the player chooses from to attack, defend, use an item, etc.
battle_menu = {
    


    }
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
        try:
            menuSelection = int(raw_input("What menu item?"))
            if menuSelection == 1:
                self.enemy1.getDamaged(self.player1.attackEnemy())
                print "Player 1 does things!"
        except:
            print "Try again!"
        

    def enemy1Turn(self):
        self.player1.getDamaged(self.enemy1.attackPlayer())
        print "Enemy 1 does things!"
        
    def doBattle(self):
        exitLoop = False
        winner = 0
        turnNumber = 1
        while exitLoop != True:
            #Displays HP, etc.
            print self.player1.hitPoints
            print self.enemy1.hitPoints
            #Takes a turn
            if turnNumber == 1:
                self.player1Turn()
                turnNumber= turnNumber + 1
            elif turnNumber == 2:
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
            
