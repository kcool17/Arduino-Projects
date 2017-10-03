#Save as player.py

class Player():

    def __init__(self, hitPoints=10, attackPower=1):
        self.hitPoints = hitPoints
        self.attackPower = attackPower
        self.startHitPoints = hitPoints
        self.startAttackPower = attackPower
        self.maxHitPoints = hitPoints
        self.maxAttackPower = attackPower

    def getDamaged(self, damage=1):
        self.hitPoints = self.hitPoints-damage
        if self.hitPoints<0:
            self.hitPoints=0

    def getHealed(self, healing=0, maxHeal=False):
        if maxHeal==True:
            self.hitPoints = self.maxHitPoints
        elif (healing + self.hitPoints) >= self.maxHitPoints:
            self.hitPoints = self.maxHitPoints
        else:
            self.hitPoints = self.hitPoints + healing

    def attackEnemy(self):
        return self.attackPower

    def lostBattle(self):
        if self.hitPoints<=0:
            return True
        else:
            return False
