#Save as main.py
from battle import Battle
from player import Player

#Create a player
#Format: Player(hitPoints, attackPower)
player1 = Player(15, 2)

#Do a battle
myBattle = Battle(player1, "Test_Enemy")
myBattle.doBattle()




