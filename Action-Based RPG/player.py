#Save as player.py
#Imports
import pygame
import os, sys
from pygame.locals import *

#Constants
UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'

#Other Variables
iteration = 1

class Player(object):

    def __init__(self, spriteFolder = 'test-sprite', hitPoints = 10, attackPower = 1):
        self.spriteFolder = spriteFolder
        self.currentSprite = 'images\\' + self.spriteFolder + '\\idle-right.png'
        self.hitPoints = hitPoints
        self.defense = 0
        self.xPos = 0
        self.yPos = 0
        self.attackPower = attackPower
        self.defensePoints = 0
        self.visible = False
        self.direction = 'u'
        self.isMoving = False
        self.moveAllowed = 0

    def change_sprite(self, spriteType = 'idle-right'):
        self.currentSprite = 'images\\' + self.spriteFolder + '\\'+spriteType+'.png'

    def direction_set(self, direction):
        if direction == UP:
            return 'back'
        elif direction == DOWN:
            return 'front'
        elif direction == LEFT:
            return 'left'
        elif direction == RIGHT:
            return 'right'
        else:
            print "Ya dun goofed (You gave direction_set() an invalid direction, stupid. Fix your code."
    def move_sprite(self):
        if self.isMoving:
            global iteration
            """self.change_sprite('move-' + str(iteration) + '-'+self.direction_set(self.direction))
            if iteration == 2:
                iteration = 1
            else:
                iteration = iteration + 1
            for i in range(200):
                if self.isMoving == False:
                    print "Stop"
                    break
                else:
                    pygame.time.wait(1)"""
            if iteration <10:
                self.change_sprite('move-1-'+self.direction_set(self.direction))
            elif iteration <20:
                self.change_sprite('move-2-'+self.direction_set(self.direction))
            else:
                iteration = 0
            iteration = iteration + 1
            print iteration
            pygame.time.wait(1)
        else:
            global iteration
            iteration = 0
            self.change_sprite('idle-'+self.direction_set(self.direction))
    
