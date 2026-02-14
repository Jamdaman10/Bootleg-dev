import pygame
import math
import random

pygame.init()
width, height = 1200, 600

win = pygame.display.set_mode((width, height))

res = 10
angle = 0
class spinner:
    def __init__(self, inputs):
        self.inputs = inputs
    def draw(self):
        pygame.draw.circle(win, (128, 128, 128), (width/2, height/2), 202)
        index = 0
        for i in self.inputs:
            myAngle = angle + ((index / len(self.inputs)) * 360)
            myAngle *= (math.pi / 180)
            angleDifferance = (180 / len(self.inputs)) * (math.pi / 180)

            points = [(width/2, height/2)]
            maxAngleDiff = angleDifferance / res
            points.append(((width/2) + math.cos(myAngle - angleDifferance) * 200, (height/2) + math.sin(myAngle - angleDifferance) * 200))
            for e in range(res):
                a = myAngle - (maxAngleDiff * (res - e))
                points.append(((width/2) + math.cos(a) * 200, (height/2) + math.sin(a) * 200))
            points.append(((width/2) + math.cos(myAngle) * 200, (height/2) + math.sin(myAngle) * 200))
            for e in range(res):
                a = myAngle + (maxAngleDiff * e)
                points.append(((width/2) + math.cos(a) * 200, (height/2) + math.sin(a) * 200))
            points.append(((width/2) + math.cos(myAngle + angleDifferance) * 200, (height/2) + math.sin(myAngle + angleDifferance) * 200))

            pygame.draw.polygon(win, i[0], points)
            index += 1
        midX = width/2
        midY = height/2
        pygame.draw.polygon(win, (255,255,255), [(midX + 200, midY), (midX + 220, midY + 5), (midX + 220, midY - 5)])
        closest = 999999999
        found = None
        index = 0
        maxRadian = 360 * (math.pi / 180)
        for i in self.inputs:
            myAngle = (angle + ((index / len(self.inputs)) * 360)) * (math.pi/180) 
            if (myAngle + ((180 / (len(self.inputs))) * (math.pi/180)))%maxRadian < closest:
                closest = (myAngle + ((180 / (len(self.inputs))) * (math.pi/180)))%maxRadian
                found = i[0]
            index += 1
        
        pygame.draw.rect(win, found, (300, 300, 20, 20))
v = spinner([[(255, 0, 0)], [(0, 255, 0)], [(0, 255, 0)]])
for i in range(100):
    v.inputs.append([(0, 255, 0)])

done = False
angleSpeed = 0
estematedEnd = angle
run = True
clock = pygame.time.Clock()
while run:
    win.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    v.draw()
    angle += angleSpeed
    angleSpeed *= 0.995

    #if abs(angleSpeed) < 0.4:
    #    angleSpeed *= 0.98
    if abs(angleSpeed) < 0.03:
        angleSpeed = 0
        done = True
    if abs(angleSpeed) > 10 and not mouseDown[0]:
        done = False
    
    angle = angle % 360
    mousePos = pygame.mouse.get_pos()
    mouseDown = pygame.mouse.get_pressed()

    if mouseDown[0] and math.dist((width/2, height/2), (mousePos[0], mousePos[1])) < 200 and done:
        angleSpeed = (math.atan2(mousePos[1] - height/2, mousePos[0] - width/2) - math.atan2(oldMouseY - height/2, oldMouseX - width/2)) * (180 / math.pi)
    if abs(angleSpeed) > 2:
        difference = (-estematedEnd + 360) % 360
        if difference > 180:
            difference -= 360
        angleSpeed += 0.002*math.copysign(1, difference)
    estematedEnd = angle
    for i in range(100000000000000000000000000000000):
        estematedEnd += (angleSpeed * pow(0.995, i))
        if abs(angleSpeed * pow(0.995, i)) < 0.03:
            break
    pygame.draw.line(win, (255,255,255), (800, 100), (800 + math.cos(angle * (math.pi/180))*20, 100 + math.sin(angle * (math.pi/180))*20))

    pygame.draw.line(win, (255,255,0), (800, 100), (800 + math.cos(estematedEnd * (math.pi/180))*20, 100 + math.sin(estematedEnd * (math.pi/180))*20))

    oldMouseX = mousePos[0]
    oldMouseY = mousePos[1]
    pygame.display.flip()
    clock.tick(60)
pygame.quit()