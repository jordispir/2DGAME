import pygame
import random
import time

xWindow, yWindow = 1280, 720 
window = pygame.display.set_mode((xWindow, yWindow)) #WINDOW MUST GO OUT!

bullets = []

class Window:
    def __init__(self):
        self.time = pygame.time.Clock()

    def startFrameWork(self):
        window.fill(pygame.Color("gray"))

    def updateFrameWork(self):
        pygame.display.flip()
        self.time.tick(27)

    def endFrameWork(self):
        out = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                out = True
            return out
            
    

class Player:
    def __init__(self): 
        self.window = Window()
        self.width, self.height = 64, 64
        self.x, self.y = (xWindow/2 - self.width/2), 0 
        self.dropVelocity = 8
        self.velocidad = 6
        self.jumpCount = 10
        self.walkCount = 0
        self.walkRight = [pygame.image.load('personaje/R1.png'), pygame.image.load('personaje/R2.png'), pygame.image.load('personaje/R3.png'), pygame.image.load('personaje/R4.png'), pygame.image.load('personaje/R5.png'), pygame.image.load('personaje/R6.png'), pygame.image.load('personaje/R7.png'), pygame.image.load('personaje/R8.png'), pygame.image.load('personaje/R9.png')]
        self.walkLeft = [pygame.image.load('personaje/L1.png'), pygame.image.load('personaje/L2.png'), pygame.image.load('personaje/L3.png'), pygame.image.load('personaje/L4.png'), pygame.image.load('personaje/L5.png'), pygame.image.load('personaje/L6.png'), pygame.image.load('personaje/L7.png'), pygame.image.load('personaje/L8.png'), pygame.image.load('personaje/L9.png')]
        self.standing = True
        self.left = False
        self.right = False
        self.Jump = False
        self.startMovement = False
        

    def playerMovement(self):
        key = pygame.key.get_pressed()

        if self.y == (yWindow - self.height):  #can't move until touching the ground / -2 (yWindow- self.height never will be = )
            self.startMovement = True

        elif self.startMovement == False:
            self.y += self.dropVelocity
            self.right = True

        if key[pygame.K_SPACE] and self.startMovement: 
            bullets.append(Projectile(self.x + self.width//2, self.y + self.height//2, (0, 0, 0), 5, (8 if self.right else -8)))
                    
        for bullet in bullets:
            bullet.movement()

        if key[pygame.K_LEFT] and self.x >= 0 and self.startMovement:
            self.x -= self.velocidad
            self.left = True
            self.right = False
            self.standing = False

        elif key[pygame.K_RIGHT] and self.x <= (xWindow - self.width)  and self.startMovement:
            self.x += self.velocidad
            self.left = False
            self.right = True
            self.standing = False

        else:
            self.standing = True
            self.walkCount = 0

        if self.Jump == False:
            if key[pygame.K_UP]:
                self.Jump = True
        else:
            if self.jumpCount >= -10 and self.startMovement:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
                
            else: # This will execute if our jump is finished
                self.jumpCount = 10
                self.Jump = False


        #print (self.walkRight[0].get_size())
        #print ("Y personaje = " + str(self.y))

    def draw(self):
        
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
            else:
               window.blit(self.walkLeft[0], (self.x, self.y))


class Projectile:
    def __init__(self, x, y, color, size, velocity):
        self.window = Window()
        self.x = x
        self.y = y
        self.xInicial = self.x
        self.yInicial = self.y
        self.color = color
        self.size = size 
        self.velocity = velocity
        self.shoot = False

    def draw(self):
        pygame.draw.circle(window, (self.color), ( int(self.x), int(self.y) ), self.size)  

    def movement(self):
        for bullet in bullets:
            if self.x == xWindow and self.x == 0: 
                bullets.pop(bullets.index(bullet)) #Delete bullet image

        self.x += self.velocity
        self.draw()
            
class Enemy:
    def __init__(self, enemySurface):
        self.width, self.height = 64, 64
        self.starterX = random.choice((enemySurface.DerechaX, enemySurface.IzquierdaX)) 
        self.mueveIzquierda, self.mueveDerecha = -4, 4 

        #Depende del random.choice starterX será en la izquierda o derecha y también cambiará el incremento y la Y.
        if self.starterX == enemySurface.DerechaX:
            self.starterX = enemySurface.DerechaX + 100
            self.starterY = enemySurface.DerechaY - self.height
            self.incremento = self.mueveIzquierda 

        elif self.starterX == enemySurface.IzquierdaX: 
            self.starterX = enemySurface.IzquierdaX - 100
            self.starterY = enemySurface.IzquierdaY - self.height
            self.incremento = self.mueveDerecha

        self.x, self.y = self.starterX, self.starterY

        self.walkCount = 0
        self.walkLeft = [pygame.image.load("enemy/L1E.png"), pygame.image.load("enemy/L2E.png"), pygame.image.load("enemy/L3E.png"), pygame.image.load("enemy/L4E.png"), pygame.image.load("enemy/L5E.png"), pygame.image.load("enemy/L6E.png"), pygame.image.load("enemy/L7E.png"), pygame.image.load("enemy/L8E.png"), pygame.image.load("enemy/L9E.png"), pygame.image.load("enemy/L10E.png"), pygame.image.load("enemy/L11E.png")]
        self.walkRight = [pygame.image.load("enemy/R1E.png"), pygame.image.load("enemy/R2E.png"), pygame.image.load("enemy/R3E.png"), pygame.image.load("enemy/R4E.png"), pygame.image.load("enemy/R5E.png"), pygame.image.load("enemy/R6E.png"), pygame.image.load("enemy/R7E.png"), pygame.image.load("enemy/R8E.png"), pygame.image.load("enemy/R9E.png"), pygame.image.load("enemy/R10E.png"), pygame.image.load("enemy/R11E.png")]
        self.dropVelocity = 8
        self.left = False
        self.right = False
        self.startMovementEnemy = False
        self.endMovement = False
        
        #print (self.starterX, self.starterY)

    def enemyDrop(self, player, enemySurface):
        if self.starterX == enemySurface.DerechaX + 100:
            if self.x < (enemySurface.DerechaX - enemySurface.width + self.width) - 20: #Out of the surface
                if self.y >= (yWindow - self.height): 
                    self.startMovementEnemy = True
                    self.endMovement = True

                elif self.startMovementEnemy == False:
                    self.left = False
                    self.y += self.dropVelocity 
                    self.drawPlayerFalling(enemySurface)

            else:
                if player.startMovement and not (self.endMovement): #mientras endMovement siga siendo False el enemigo se moverá hacia la izquierda, 
                    self.left = True                                #cuando endMovement sea True no se sumará el mueveIzquierda y tampoco impedirá avanzar en el enemyMovement.
                    self.x += self.mueveIzquierda   
        
        elif self.starterX == enemySurface.IzquierdaX - 100:
            if self.x > (enemySurface.IzquierdaX + enemySurface.width - self.width) + 40: 
                if self.y >= (yWindow - self.height): 
                    self.startMovementEnemy = True
                    self.endMovement = True

                elif self.startMovementEnemy == False:
                    self.right = False
                    self.y += self.dropVelocity 
                    self.drawPlayerFalling(enemySurface)

            else:
                if player.startMovement and not (self.endMovement): 
                    self.right = True                         
                    self.x += self.mueveDerecha

        #print (self.startMovementEnemy)
        print (self.x, self.y)
        #time.sleep(0.1)

    def enemyMovement(self, player, enemySurface):
        if self.startMovementEnemy and player.startMovement:
            if self.incremento == self.mueveDerecha:
                self.right, self.left = True, False

                if self.x < (xWindow - self.width):
                    self.x += self.incremento

                else:
                    self.incremento = self.mueveIzquierda

            else:
                self.right, self.left = False, True

                if self.x >= 0:
                    self.x += self.incremento #TODO Player does not touch the xWindow. 
                
                else:
                    self.incremento = self.mueveDerecha

        #print (self.x)
        #print ("xWindow - self.width = " + str(xWindow- self.width))
        #print (self.left, self.right)
        #print (self.mueveIzquierda, self.mueveDerecha)

    def drawPlayerFalling(self, enemySurface):
            if self.starterX == enemySurface.DerechaX + 100:
                window.blit(self.walkLeft[0], (self.x, self.y))
            elif self.starterX == enemySurface.IzquierdaX - 100:
                window.blit(self.walkRight[6], (self.x, self.y))

    def drawMovement(self, player, enemySurface):
        if player.startMovement:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if self.left:
                window.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            window.blit(self.walkLeft[0], (self.x, self.y))
            
        

class EnemySurface:
    def __init__(self):
        self.DerechaX, self.DerechaY = xWindow - 100, random.randrange(100, 500)
        self.IzquierdaX, self.IzquierdaY = 0, random.randrange(100, 500)
        self.width, self.height = 100, 5
        self.color = (0, 0, 0)
    
    def draw(self):
        pygame.draw.rect(window, self.color, (self.DerechaX, self.DerechaY, self.width, self.height))
        pygame.draw.rect(window, self.color, (self.IzquierdaX, self.IzquierdaY, self.width, self.height))

    #TODO Make a phisics motor for Enemy. OK 50%
    #TODO Encontrar optimitzación para el error. (línea 156) | con  >=   OK! (se pasará por un mínimo)
    #TODO Crear varios personajes que aparezcan en diferentes posiciones. 50%

    #get_size() -> image.get_size() -> print variable
    #Solo se queda con 400 en la Y. OK -> La altura y anchura del personaje es de 64 x 64, se debe convertir con pygame.transform.scale