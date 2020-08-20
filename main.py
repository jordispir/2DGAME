import pygame
import sprite

pygame.init()


window = sprite.Window() 
player = sprite.Player()


while not window.endFrameWork():
    window.startFrameWork()
    player.playerMovement()
    player.draw()
    window.updateFrameWork()


pygame.quit()
    
