import pygame
import sprite
import windowManager 

pygame.init()

window =  windowManager.Window()
playerSurface = sprite.PlayerSurface()
player = sprite.Player()
enemySurface = sprite.EnemySurface()
enemy = sprite.Enemy(enemySurface)

while not window.endFrameWork():
    window.startFrameWork()
    windowManager.updateWindow()
    player.playerMovement(enemy)
    player.playerCollision(playerSurface)
    player.drawPlayer()
    playerSurface.draw()
    player.drawSpacheShip()
    player.spacheShipMovement()
    enemy.enemyDrop(player, enemySurface)
    enemy.enemyMovement(player, enemySurface)
    enemy.drawMovement(player, enemySurface)
    enemySurface.draw()
    window.updateFrameWork()


pygame.quit()
    

