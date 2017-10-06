#Save as main.py
#Imports
import pygame
import os, sys
from pygame.locals import *
from player import Player
import threading


    
#Constants



#Kills all threads and program if run
killAll = False
def kill_all():
    done = True
    killAll = True
    pygame.display.quit()
    pygame.quit()
    os._exit(0)

#Pygame Init
pygame.init()
size = (1024, 576)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

#Variables
keyPressed = pygame.key.get_pressed()
global keyPressed


#Image Dictionary
image_library = {}
#Image retriever
def get_image(path):
        global image_library
        image = image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                image_library[path] = image
        return image

#Creates a player object
player = Player()

#Default Settings
useArrowKeys = False
player.moveAllowed = 0

#For Testing Purposes
player.moveAllowed = 1
player.visible = True

    
#Infinitely updating movement thread
def move_function():
    exitVar = False
    #Makes sure it doesn't change the direction if you press 2 keys at once
    continueVarUp = False
    continueVarDown =False
    continueVarLeft = False
    continueVarRight = False
    while exitVar != True:
        #Changes direction of player with WASD/Arrow Keys
        if player.moveAllowed == 1:#Player moves normally on the map
            if useArrowKeys:
                if keyPressed[K_UP] and not(continueVarDown or continueVarLeft or continueVarRight):
                    continueVarUp = True
                    player.direction = 'u'
                if not keyPressed[K_UP]:
                    continueVarUp = False
                if keyPressed[K_DOWN] and not(continueVarUp or continueVarLeft or continueVarRight):
                    continueVarDown = True
                    player.direction = 'd'
                if not keyPressed[K_DOWN]:
                    continueVarDown = False
                if keyPressed[K_LEFT] and not(continueVarDown or continueVarUp or continueVarRight):
                    continueVarLeft = True
                    player.direction = 'l'
                if not keyPressed[K_LEFT]:
                    continueVarLeft = False
                if keyPressed[K_RIGHT] and not(continueVarDown or continueVarLeft or continueVarUp):
                    continueVarRight = True
                    player.direction = 'r'
                if not keyPressed[K_RIGHT]:
                    continueVarRight = False
            else:
                if keyPressed[K_w] and not(continueVarDown or continueVarLeft or continueVarRight):
                    continueVarUp = True
                    player.direction = 'u'
                if not keyPressed[K_w]:
                    continueVarUp = False
                if keyPressed[K_s] and not(continueVarUp or continueVarLeft or continueVarRight):
                    continueVarDown = True
                    player.direction = 'd'
                if not keyPressed[K_s]:
                    continueVarDown = False
                if keyPressed[K_a] and not(continueVarDown or continueVarUp or continueVarRight):
                    continueVarLeft = True
                    player.direction = 'l'
                if not keyPressed[K_a]:
                    continueVarLeft = False
                if keyPressed[K_d] and not(continueVarDown or continueVarLeft or continueVarUp):
                    continueVarRight = True
                    player.direction = 'r'
                if not keyPressed[K_d]:
                    continueVarRight = False
        
        elif player.moveAllowed == -1: #Player moves in menu screens
            foo = 0
        elif player.moveAllowed == 0: #Player can't move with arrows at all
            foo = 0
        else:
            print "You can't even Python! (You set moveAllowed to an invalid number, you idiot)"
            print "moveAllowed = " + str(player.moveAllowed)


        #Actually moves the player in the direction they are facing
        if player.moveAllowed == 1:
            if useArrowKeys:
                if keyPressed[K_UP] or keyPressed[K_LEFT] or keyPressed[K_DOWN] or keyPressed[K_RIGHT]:
                    player.isMoving = True
                else:
                    player.isMoving = False
            else:
                if keyPressed[K_w] or keyPressed[K_a] or keyPressed[K_s] or keyPressed[K_d]:
                    player.isMoving = True
                    
                else:
                    player.isMoving = False
        if killAll:
            exitVar = True
            thread.exit()
        
move_thread = threading.Thread(target=move_function)
move_thread.daemon = True



#Starts Threads
move_thread.start()

#Forever loop in which the program runs
while not killAll:
    #Kills program if window is closed
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill_all()

    #Checks what keys are pressed, and toggles fullscreen/ALT+F4
    keyPressed = pygame.key.get_pressed()
    if (keyPressed[pygame.K_LALT] or keyPressed[pygame.K_RALT]) and keyPressed[pygame.K_RETURN]:
        if screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode(size)
        else:
            pygame.display.set_mode(size, pygame.FULLSCREEN)
    if (keyPressed[pygame.K_LALT] or keyPressed[pygame.K_RALT]) and keyPressed[pygame.K_F4]:
        kill_all()

    #For Testing Purposes

    
    #Main Program
    if player.visible == True:
        screen.blit(get_image(player.currentSprite), (player.xPos, player.yPos))
    player.move_sprite()

    
    #Updates the screen; keep at end of file
    pygame.display.flip()
    screen.fill((0,0,0))
    clock.tick(60)
