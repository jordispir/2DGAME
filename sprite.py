import pygame
import time

xWindow, yWindow = 600, 400
window = pygame.display.set_mode((xWindow, yWindow)) #WINDOW MUST GO OUT!

bg = pygame.image.load('background/bg.jpg')
bullets = []

class Window:
    def __init__(self):
        self.time = pygame.time.Clock()

    def startFrameWork(self):
        window.fill(pygame.Color("gray"))
        window.blit(bg, (0, 0))

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
        self.x, self.y = 0, 0 
        self.width, self.height = 64, 64
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

        if self.y == yWindow - self.height:  #can't move until touching the ground
            self.startMovement = True

        elif self.startMovement == False:
            self.y += self.velocidad   
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


    #Solo se queda con 400 en la Y. OK -> La altura y anchura del personaje es de 64 x 64, se debe convertir con pygame.transform.scale
    #get_size() -> image.get_size() -> print variable