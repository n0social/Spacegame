#pygame basics 

#Objectives - Draw on Screen, Play Sound Effects, Handle User Input, Implement Event Loops, Describe game programming works.

#This program creates a window, fills the background with white, and draws a blue circle in the middle of it.


#Hello World!

import pygame
pygame.init()


#Setup the drawing window
screen = pygame.display.set_mode([500, 500])

#Run until the user asks to quit
running = True
while running:
    
    #Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Fill the background with white
    screen.fill((255, 255, 255))
    
    #Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0,0,255), (250, 250), 75)
    
    #Flip the display
    pygame.display.flip()
    
#Done, time to die.
pygame.quit()