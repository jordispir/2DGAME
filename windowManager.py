import pygame
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

xWindow, yWindow = 1200, 720
xWindowMaximized, yWindowMaximized = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

xWindow, yWindow = 1200, 720
window = pygame.display.set_mode((xWindow, yWindow), pygame.RESIZABLE)


class Window:
    def __init__(self):
        self.time = pygame.time.Clock()

    def startFrameWork(self):
        window.fill(pygame.Color("gray"))

    def updateFrameWork(self):
        pygame.display.flip()
        self.time.tick(27)

    def updateWindow(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    window = pygame.display.set_mode((xWindowMaximized, yWindowMaximized))
                    print ("a")


    def endFrameWork(self):
        out = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                out = True
            return out