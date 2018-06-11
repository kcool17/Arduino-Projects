#Save as enemy.py
import random


class Enemy():

    def __init__(self, name = "Defaulter", hitPoints=5, attackPower=1):
        self.name = name
        self.hitPoints = hitPoints
        self.maxHitPoints = hitPoints
        self.attackPower = attackPower
        self.startAttackPower = attackPower
        

    def getDamaged(self, damage=1): #Function for when the enemy gets damaged
        self.hitPoints = self.hitPoints - damage
        if self.hitPoints<0:
            self.hitPoints=0

    def attackPlayer(self): #Function for when it attacks a player
        toAttack = self.attackPower + (random.choice([-1, 1]) * random.randint(0, int(self.attackPower*0.5)))
        if toAttack == 0:
            toAttack = 1
        return toAttack

    def lostBattle(self): #Checks if it lost a battle
        if self.hitPoints<=0:
            return True
        else:
            return False
