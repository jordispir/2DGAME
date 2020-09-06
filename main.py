import pygame
import sprite
import windowManager

pygame.init()

window =  windowManager.Window()
player = sprite.Player()
enemySurface = sprite.EnemySurface()
enemy = sprite.Enemy(enemySurface)


while not window.endFrameWork():
    window.startFrameWork()
    player.playerMovement()
    player.draw()
    enemy.enemyDrop(player, enemySurface)
    enemy.enemyMovement(player, enemySurface)
    enemy.drawMovement(player, enemySurface)
    enemySurface.draw()
    window.updateWindow()
    window.updateFrameWork()


pygame.quit()
    

