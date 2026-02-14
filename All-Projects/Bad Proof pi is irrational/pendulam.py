import pygame
import math
import random
pygame.init()

width, height = 1200, 600
win = pygame.display.set_mode((width, height))

RES = 2
camSize = 0.1

class line:
    def __init__(self, length, startPos, turnSpeed):
        self.length = length
        self.startPos = startPos
        self.angle = startPos
        self.turnSpeed = turnSpeed
        self.myLine = None
    def update(self):
        self.angle += self.turnSpeed
        if self.myLine != None:
            self.myLine.update()
    def draw(self, sX, sY):
        self.x = math.cos(self.angle) * self.length
        self.y = math.sin(self.angle) * self.length
        pygame.draw.line(win, (255, 255, 255), (sX, sY), (sX + self.x, sY + self.y), 1)
        if self.myLine != None:
            self.myLine.draw(sX + self.x, sY + self.y)
        self.x = self.x + sX
        self.y = self.y + sY
class pendulum:
    def __init__(self, count):
        self.count = count
        self.trail = []
        self.lines = []
        """
        for i in range(count):
            self.lines.append(line(100 + (math.pi * i), 0, math.tau / ((360 * RES) / (i + 1))))
            if i > 0:
                self.lines[-2].myLine = self.lines[-1]"""
        self.lines.append(line(100, 0, math.tau / (360 * RES)))
        self.lines.append(line(100, math.pi, math.tau / (360 * RES * math.pi)))
        self.lines[0].myLine = self.lines[1]
    def update(self):
        self.lines[0].update()
    def draw(self):
        self.lines[0].draw(0, 0)
        self.trail.append((self.lines[-1].x, self.lines[-1].y))
        for i in range(len(self.trail)):
            if i == 0:
                continue
            x = (self.trail[i][0] / camSize) + width/2
            y = (self.trail[i][1] / camSize) + height/2

            x2 = (self.trail[i-1][0] / camSize) + width/2
            y2 = (self.trail[i-1][1] / camSize) + height/2
            pygame.draw.line(win, (255, 0, 0), (x, y), (x2, y2), 1)
p = pendulum(2)

clock = pygame.time.Clock()
run = True
while run:
    win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for i in range(RES):
        for i in range(20):
            p.update()
        p.draw()
    pygame.display.update()
    #clock.tick(60)
pygame.quit()