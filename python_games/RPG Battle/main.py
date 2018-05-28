#import the pygame module, and the
#sys module for exiting the window we create
import pygame, sys

#import some useful constants
from pygame.locals import *

#initialise the pygame module
pygame.init()

#create a new drawing surface, width=300, height=300
screen = pygame.display.set_mode((300,300))
#give the window a caption
pygame.display.set_caption('RPG Battle')

#loop (repeat) forever
while True:

    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #end the game and close the window
            pygame.quit()
            sys.exit()

    #update the display        
    pygame.display.update()
