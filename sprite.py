import pygame
import windowManager
import random
import time
import threading
import tools

window = windowManager.window
xWindow, yWindow = windowManager.xWindow, windowManager.yWindow

bullets = []
enemies = pygame.sprite.Group()
players = pygame.sprite.Group()

class spaceShip:
    def __init__(self):
        self.spaceShipImage = pygame.image.load("objetos/spacheShip.png")
        self.spaceShipHeight = self.spaceShipImage.get_height()
        self.spaceShipWidth = self.spaceShipImage.get_width()
        self.spaceShipLight = pygame.image.load("objetos/lighting.png")
        self.xSpaceShip, self.ySpaceShip = -self.spaceShipImage.get_width() , 100
        self.spaceShipVelocity = 4
        self.intro = True
        self.startMovement = False
        self.playerPhy = False
        self.onGround = False

    def spaceIntro(self):
        if self.intro:
            if self.playerPhy:
                if self.onGround or self.startMovement: #fin del condicional.
                    self.startMovement = True
                    if self.xSpaceShip < xWindow:
                        self.xSpaceShip += 10
                    else:
                        self.intro = False
                else:
                    window.blit(self.spaceShipLight, (self.xSpaceShip/2, self.ySpaceShip + (self.spaceShipHeight - 20 )))
            else:
                if self.xSpaceShip > 50:
                    self.playerPhy = True
                else:
                    self.xSpaceShip += self.spaceShipVelocity

    def draw(self):
        window.blit(self.spaceShipImage, (self.xSpaceShip, self.ySpaceShip))

class Player:
    def __init__(self, space):
        self.window = window
        self.width, self.height = 64, 64
        self.x, self.y = 51 + (space.spaceShipWidth/ 2) - 50, 175
        self.walkRight = [pygame.image.load('personaje/R1.png'), pygame.image.load('personaje/R2.png'), pygame.image.load('personaje/R3.png'), pygame.image.load('personaje/R4.png'), pygame.image.load('personaje/R5.png'), pygame.image.load('personaje/R6.png'), pygame.image.load('personaje/R7.png'), pygame.image.load('personaje/R8.png'), pygame.image.load('personaje/R9.png')]
        self.walkLeft = [pygame.image.load('personaje/L1.png'), pygame.image.load('personaje/L2.png'), pygame.image.load('personaje/L3.png'), pygame.image.load('personaje/L4.png'), pygame.image.load('personaje/L5.png'), pygame.image.load('personaje/L6.png'), pygame.image.load('personaje/L7.png'), pygame.image.load('personaje/L8.png'), pygame.image.load('personaje/L9.png')]

        self.player = pygame.sprite.Sprite()

        self.playerImage = self.walkRight[0]
        self.playerHeight = self.playerImage.get_height()
        self.player.rect = self.playerImage.get_rect() 
        self.player.rect.x = self.x
        self.player.rect.y = self.y

        players.add(self.player)

        self.walkCount = 0
        self.dropVelocity = 8
        self.velocidad = 8
        self.jumpCount = 10
        self.standing = True
        self.left = False
        self.right = False
        self.Jump = False

    def playerDrop(self, space):
        if space.playerPhy:
            if self.y < yWindow - self.playerHeight:
                self.right = True
                self.y += self.dropVelocity
            
            else:
                space.startMovement = True
                self.y = yWindow - self.playerHeight

            if self.y == yWindow - self.playerHeight:
                space.onGround = True

        self.player.rect.x = self.x
        self.player.rect.y = self.y

    def playerMovement(self, enemy, space):
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and space.startMovement: 
            if len(bullets) < 1:
                pass

        for bullet in bullets:
            bullet.movement()
            bullet.draw()

        if key[pygame.K_LEFT] and self.x >= 0 and space.startMovement:
            self.x -= self.velocidad
            self.left = True
            self.right = False
            self.standing = False

        elif key[pygame.K_RIGHT] and self.x <= (xWindow - self.width)  and space.startMovement:
            self.x += self.velocidad
            self.left = False
            self.right = True
            self.standing = False

        else:
            self.standing = True
            self.walkCount = 0

        if not self.Jump and key[pygame.K_UP] and space.startMovement:
            if space.onGround:
                self.Jump = True
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
                space.onGround = False

        elif self.Jump:
            if not space.onGround:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else: # This will execute if our jump is finished
                self.jumpCount = 10
                self.Jump = False
        
        #print (space.onGround)

        self.player.rect.x = self.x
        self.player.rect.y = self.y

        #print (self.player.rect.x, self.player.rect.y, self.x, self.y)

    def collision(self):
        if (pygame.sprite.spritecollideany(self.player, enemies)):
            print ("collision")

    def drawPlayer(self):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.standing == False:
            if self.left:
                window.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(self.walkRight[0], (self.x, self.y))
            elif self.left:
                window.blit(self.walkLeft[0], (self.x, self.y))

class Projectile:
    def __init__(self):
        pass

class Enemy:
    def __init__(self, enemySurface):
        self.width, self.height = 64, 64
        self.starterX = random.choice((enemySurface.DerechaX, enemySurface.IzquierdaX)) 
        self.mueveIzquierda, self.mueveDerecha = -4, 4 

        #Depende del random.choice starterX será en la izquierda o derecha y también cambiará el incremento y la Y.
        if self.starterX == enemySurface.DerechaX:
            self.starterX = enemySurface.DerechaX + 100
            self.starterY = enemySurface.DerechaY - self.height

            self.starterX2 = enemySurface.IzquierdaX - 100
            self.starterY2 = enemySurface.IzquierdaY - self.height

            self.incrementoE1 = self.mueveIzquierda 
            self.incrementoE2 = self.mueveDerecha

        elif self.starterX == enemySurface.IzquierdaX: 
            self.starterX = enemySurface.IzquierdaX - 100
            self.starterY = enemySurface.IzquierdaY - self.height

            self.starterX2 = enemySurface.DerechaX + 100
            self.starterY2 = enemySurface.DerechaY - self.height

            self.incrementoE1 = self.mueveDerecha
            self.incrementoE2 = self.mueveIzquierda

        self.x, self.y = self.starterX, self.starterY
        self.x2, self.y2 = self.starterX2, self.starterY2

        self.walkLeft = [pygame.image.load("enemy/L1E.png"), pygame.image.load("enemy/L2E.png"), pygame.image.load("enemy/L3E.png"), pygame.image.load("enemy/L4E.png"), pygame.image.load("enemy/L5E.png"), pygame.image.load("enemy/L6E.png"), pygame.image.load("enemy/L7E.png"), pygame.image.load("enemy/L8E.png"), pygame.image.load("enemy/L9E.png"), pygame.image.load("enemy/L10E.png"), pygame.image.load("enemy/L11E.png")]
        self.walkRight = [pygame.image.load("enemy/R1E.png"), pygame.image.load("enemy/R2E.png"), pygame.image.load("enemy/R3E.png"), pygame.image.load("enemy/R4E.png"), pygame.image.load("enemy/R5E.png"), pygame.image.load("enemy/R6E.png"), pygame.image.load("enemy/R7E.png"), pygame.image.load("enemy/R8E.png"), pygame.image.load("enemy/R9E.png"), pygame.image.load("enemy/R10E.png"), pygame.image.load("enemy/R11E.png")]

        self.enemyLeft = pygame.sprite.Sprite()
        self.enemyImage = self.walkLeft[0]
        self.enemyLeft.rect = self.enemyImage.get_rect()
        self.enemyLeft.rect.x = self.x
        self.enemyLeft.rect.y = self.y

        self.enemyRight = pygame.sprite.Sprite()
        self.enemyRightImage = self.walkRight[0]
        self.enemyRight.rect = self.enemyRightImage.get_rect()
        self.enemyRight.rect.x = self.x2
        self.enemyRight.rect.y = self.y2
        

        enemies.add(self.enemyLeft)
        enemies.add(self.enemyRight)

        self.dropVelocity = 8
        self.left, self.right = False, False
        self.left2, self.right2 = False, False
        self.startMovementE1, self.startMovementE2 = False, False
        self.endMovementE1, self.endMovementE2 = False, False
        self.walkCountE1 = 0
        self.walkCountE2 = 0

    def enemyDrop(self, space, enemySurface):
        if self.starterX == enemySurface.DerechaX + 100:
            if self.x < (enemySurface.DerechaX - enemySurface.width + self.width) - 20: #Out of the surface
                if self.y >= (yWindow - self.height): 
                    self.startMovementE1 = True
                    self.endMovementE1 = True

                elif self.startMovementE1 == False:
                    self.left = False
                    self.y += self.dropVelocity 
                    self.drawPlayerFalling(enemySurface)

            else:
                if space.startMovement and not (self.endMovementE1): #mientras endMovement siga siendo False el enemigo se moverá hacia la izquierda, 
                    self.left = True                                  #cuando endMovement sea True no se sumará el mueveIzquierda y tampoco impedirá avanzar en el enemyMovement.
                    self.x += self.mueveIzquierda   
        
        elif self.starterX == enemySurface.IzquierdaX - 100:
            if self.x > (enemySurface.IzquierdaX + enemySurface.width - self.width) + 40: 
                if self.y >= (yWindow - self.height): 
                    self.startMovementE1 = True
                    self.endMovementE1 = True

                elif self.startMovementE1 == False:
                    self.right = False
                    self.y += self.dropVelocity 
                    self.drawPlayerFalling(enemySurface)

            else:
                if space.startMovement and not (self.endMovementE1): 
                    self.right = True                         
                    self.x += self.mueveDerecha

        if self.starterX2 == enemySurface.DerechaX + 100:
            if self.x2 < (enemySurface.DerechaX - enemySurface.width + self.width) - 20: 
                if self.y2 >= (yWindow - self.height): 
                    self.startMovementE2 = True
                    self.endMovementE2 = True

                elif self.startMovementE2 == False:
                    self.left2 = False
                    self.y2 += self.dropVelocity 
                    self.drawPlayerFalling(enemySurface)

            else:
                if space.startMovement and not (self.endMovementE2): 
                    self.left2 = True
                    self.x2 += self.mueveIzquierda   
        
        elif self.starterX2 == enemySurface.IzquierdaX - 100:
            if self.x2 > (enemySurface.IzquierdaX + enemySurface.width - self.width) + 40: 
                if self.y2 >= (yWindow - self.height):
                    self.startMovementE2 = True
                    self.endMovementE2 = True

                elif self.startMovementE2 == False:
                    self.right2 = False
                    self.y2 += self.dropVelocity 
                    self.drawPlayerFalling(enemySurface)

            else:
                if space.startMovement and not (self.endMovementE2): 
                    self.right2 = True                         
                    self.x2 += self.mueveDerecha

    def enemyMovement(self, space, enemySurface):
        if self.startMovementE1 and space.startMovement:
            if self.incrementoE1 == self.mueveDerecha:
                self.right, self.left = True, False

                if self.x < (xWindow - self.width):
                    self.x += self.incrementoE1

                else:
                    self.incrementoE1 = self.mueveIzquierda

            else:
                self.right, self.left = False, True

                if self.x >= 0:
                    self.x += self.incrementoE1 
                
                else:
                    self.incrementoE1 = self.mueveDerecha

        if self.startMovementE2 and space.startMovement:
            if self.incrementoE2 == self.mueveDerecha:
                self.right2, self.left2 = True, False

                if self.x2 < (xWindow - self.width):
                    self.x2 += self.incrementoE2

                else:
                    self.incrementoE2 = self.mueveIzquierda

            else:
                self.right2, self.left2 = False, True

                if self.x2 >= 0:
                    self.x2 += self.incrementoE2 
                
                else:
                    self.incrementoE2 = self.mueveDerecha
        
        self.enemyLeft.rect.x = self.x
        self.enemyLeft.rect.y = self.y

        self.enemyRight.rect.x = self.x2
        self.enemyRight.rect.y = self.y2

    def drawPlayerFalling(self, enemySurface):
            if self.starterX == enemySurface.DerechaX + 100 and not(self.startMovementE1):
                window.blit(self.walkLeft[0], (self.x, self.y))
            elif self.starterX == enemySurface.IzquierdaX - 100 and not(self.startMovementE1):
                window.blit(self.walkRight[6], (self.x, self.y))
            if self.starterX2 == enemySurface.DerechaX + 100 and not(self.startMovementE2):
                window.blit(self.walkLeft[0], (self.x2, self.y2))
            elif self.starterX2 == enemySurface.IzquierdaX - 100 and not(self.startMovementE2):
                window.blit(self.walkRight[6], (self.x2, self.y2))

    def drawMovement(self, space, enemySurface):
        if space.startMovement:
            if self.walkCountE1 + 1 >= 27:
                self.walkCountE1 = 0

            if self.walkCountE2 + 1 >= 27:
                self.walkCountE2 = 0

            if self.left:
                window.blit(self.walkLeft[self.walkCountE1//3], (self.x, self.y))
                self.walkCountE1 += 1

            elif self.right:
                window.blit(self.walkRight[self.walkCountE1//3], (self.x, self.y))
                self.walkCountE1 += 1

            if self.left2:
                window.blit(self.walkLeft[self.walkCountE2//3], (self.x2, self.y2))
                self.walkCountE2 += 1

            elif self.right2:
                window.blit(self.walkRight[self.walkCountE2//3], (self.x2, self.y2))
                self.walkCountE2 += 1
        else:
            window.blit(self.walkLeft[0], (self.x, self.y))

class EnemySurface:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.DerechaX, self.DerechaY = xWindow - 100, random.randrange(100, 500)
        self.IzquierdaX, self.IzquierdaY = 0, random.randrange(100, 500)
        self.width, self.height = 100, 5
        self.color = (0, 0, 0)
    
    def draw(self):
        pygame.draw.rect(window, self.color, (self.DerechaX, self.DerechaY, self.width, self.height))
        pygame.draw.rect(window, self.color, (self.IzquierdaX, self.IzquierdaY, self.width, self.height))