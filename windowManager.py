import pygame
pygame.init()

global window, xWindow, yWindow, xWindowMaximized, yWindowMaximized, fullscreen

monitorSize = pygame.display.Info()

xWindow, yWindow = 1200, 720

xWindowMaximized, yWindowMaximized = monitorSize.current_w, monitorSize.current_h
print (monitorSize.current_w, monitorSize.current_h)

window = pygame.display.set_mode((xWindow, yWindow), pygame.RESIZABLE)
fullscreen = False

def updateWindow():
    global window, xWindow, yWindow, xWindowMaximized, yWindowMaximized, fullscreen

    key = pygame.key.get_pressed()
    event = pygame.event.poll()

    if event.type == pygame.VIDEORESIZE:
        if not fullscreen:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
    if key[pygame.K_f]: 
        fullscreen = not fullscreen
        if fullscreen:
            window = pygame.display.set_mode((xWindowMaximized, yWindowMaximized), pygame.FULLSCREEN)
            xWindow, yWindow = xWindowMaximized, yWindowMaximized
        else:
            window = pygame.display.set_mode((xWindow, yWindow), pygame.RESIZABLE)
        
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