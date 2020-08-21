import pygame
import sprite

pygame.init()


window = sprite.Window() 
player = sprite.Player()
enemy = sprite.Enemy()


while not window.endFrameWork():
    window.startFrameWork()
    player.playerMovement()
    player.draw()
    enemy.enemyMovement(player)
    enemy.draw(player)
    window.updateFrameWork()


pygame.quit()
    
