import pygame
import sprite

pygame.init()


window = sprite.Window() 
player = sprite.Player()
enemySurface = sprite.EnemySurface()
enemy = sprite.Enemy(enemySurface)


while not window.endFrameWork():
    window.startFrameWork()
    player.playerMovement()
    player.draw()
    enemy.enemyMovement(player, enemySurface)
    enemy.draw(player)
    enemySurface.draw()
    window.updateFrameWork()


pygame.quit()
    
