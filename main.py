import pygame
import sprite

pygame.init()


window = sprite.Window() 
player = sprite.Player()
enemySurface = sprite.EnemySurface()
enemy = sprite.Enemy(enemySurface)


while not window.endFrameWork():
    window.startFrameWork()
    player.playerMovement(enemy)
    player.draw()
    enemy.enemyDrop(player, enemySurface)
    enemy.enemyMovement(player, enemySurface)
    enemy.drawMovement(player, enemySurface)
    enemySurface.draw()
    window.updateFrameWork()


pygame.quit()
    
