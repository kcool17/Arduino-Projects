#Save as player.py
import random


class Player():

    def __init__(self, hitPoints=10, attackPower=1):
        self.hitPoints = hitPoints
        self.attackPower = attackPower
        self.startHitPoints = hitPoints
        self.startAttackPower = attackPower
        self.maxHitPoints = hitPoints
        self.maxAttackPower = attackPower
        self.regenTurns = 0
        self.attUpTurns = 0
        self.defUpTurns = 0
        self.inventory = {
        "healPot":0, #Heals 10 HP
        "regenPot":0, #Regens 5 HP per turn for 2 turns
        "defPot":0, #Decreases damage by 1 for 2 turns
        "attackPot":0, #Increase damage dealt by 1 for 2 turns
        "superHealPot":0 #Heals to full
        }

    def getDamaged(self, damage=1): #Function for when player gets damaged
        self.hitPoints = self.hitPoints-damage
        if self.hitPoints<0:
            self.hitPoints=0

    def getHealed(self, healing=0, maxHeal=False): #Function for when the player heals
        if maxHeal==True:
            self.hitPoints = self.maxHitPoints
            return True
        elif (healing + self.hitPoints) >= self.maxHitPoints:
            self.hitPoints = self.maxHitPoints
            return True
        else:
            self.hitPoints = self.hitPoints + healing
            return False

    def removeInventory(self, item):
        try:
            if self.inventory[item]>0:
                self.inventory[item]-=1
                return True
        except:
            pass
        return False
    
    def attackEnemy(self): #Function for when the player attacks an enemy
        toAttack = self.attackPower + (random.choice([-1, 1]) * random.randint(0, int(self.attackPower*0.5)))
        if toAttack == 0:
            toAttack = 1
        return toAttack

    def lostBattle(self): #Checks if it lost a battle
        if self.hitPoints<=0:
            return True
        else:
            return False
