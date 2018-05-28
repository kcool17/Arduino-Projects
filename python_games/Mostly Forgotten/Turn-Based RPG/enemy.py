#Save as enemy.py



class Enemy():

    def __init__(self, hitPoints=5, attackPower=1):
        self.hitPoints = hitPoints
        self.attackPower = attackPower

    def getDamaged(self, damage=1):
        self.hitPoints = self.hitPoints - damage
        if self.hitPoints<0:
            self.hitPoints=0

    def attackPlayer(self):
        return self.attackPower

    def lostBattle(self):
        if self.hitPoints<=0:
            return True
        else:
            return False
