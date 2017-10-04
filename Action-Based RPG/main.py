#Imports
import pygame
import os, sys
from pygame.locals import *

#Pygame Init
pygame.init()
size = (1024, 576)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
done = False
clock = pygame.time.Clock()

#Image Dictionary
image_library = {}
#Image retriever
def get_image(path):
        image = image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                image_library[path] = image
        return image


#Forever loop in which the program runs
while not done:
    #Ends the program if the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.display.quit()
            pygame.quit()
            
    #Checks what keys are pressed, and toggles fullscreen/ALT+F4
    keyPressed = pygame.key.get_pressed()
    if (keyPressed[pygame.K_LALT] or keyPressed[pygame.K_RALT]) and keyPressed[pygame.K_RETURN]:
        if screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode(size)
        else:
            pygame.display.set_mode(size, pygame.FULLSCREEN)
    if (keyPressed[pygame.K_LALT] or keyPressed[pygame.K_RALT]) and keyPressed[pygame.K_F4]:
        done = True
        pygame.display.quit()
        pygame.quit()

        
    #Main Program

    screen.blit(get_image('images/test_image.png'), (20, 20))

    
    #Updates the screen; keep at end of file
    pygame.display.flip()
    screen.fill((0,0,0))
    clock.tick(60)
