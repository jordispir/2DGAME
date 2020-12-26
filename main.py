import pygame
import sprite
import windowManager 

pygame.init()

window =  windowManager.Window()
spaceShip = sprite.spaceShip()
player = sprite.Player(spaceShip)
enemySurface = sprite.EnemySurface()
enemy = sprite.Enemy(enemySurface)

while not window.endFrameWork():
    window.startFrameWork()
    windowManager.updateWindow()

    #space
    spaceShip.spaceIntro()
    spaceShip.draw()

    #player
    player.playerMovement(enemy, spaceShip)
    player.playerDrop(spaceShip)
    player.collision()
    player.drawPlayer()

    #enemy
    enemy.enemyDrop(spaceShip, enemySurface)
    enemy.enemyMovement(spaceShip, enemySurface)
    enemy.drawMovement(spaceShip, enemySurface)
    enemySurface.draw()
    
    window.updateFrameWork()


pygame.quit()
    

