class Player():

    def __init__(self, moveType=0):
        self.inBattle = False
        #Movetypes: 0=Wings
        self.moveType = moveType
        self.xPos = 0
        self.yPos = 0
        self.xSpeed = SPEED
        self.ySpeed = SPEED
