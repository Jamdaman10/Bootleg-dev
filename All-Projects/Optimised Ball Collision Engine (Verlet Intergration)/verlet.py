import pygame
import random
import math
import cProfile

pygame.init()
width, height = 1200, 600
win = pygame.display.set_mode((width, height))
gravity = 0.51
bounce = 0.8
drag = 0.999
friction = 0.8

DT = 0.25
GRIDSIZE = 14
gWidth = math.ceil(width / GRIDSIZE)
gHeight = math.ceil(height / GRIDSIZE)

gridArangments = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

balls = []
for i in range(gHeight):
    collum = []
    for i in range(gWidth):
        collum.append([])
    balls.append(collum)


for i in range(1000):
    x = random.uniform(0,width)
    y = random.uniform(0,height)
    r = random.randrange(2, 255)
    g = random.randrange(1, r)
    b = random.randrange(0, g)
    balls[5][5].append([x, y, x, y, 7, (b, g, r)])#ball : x, y, oldX, oldY, radius, color
def speedyDist(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return ((dx**2) + (dy**2))

def updateBalls():
    for gY in balls:
        for gX in gY:
            for i in gX:
                xVel = i[0] - i[2]
                yVel = i[1] - i[3]

                i[2] = i[2] + (i[0] - i[2]) * DT
                i[3] = i[3] + (i[1] - i[3]) * DT

                i[0] += xVel * DT
                i[1] += yVel * DT
                i[1] += gravity * DT

def constrain():
    y = 0
    for gY in balls:
        x = 0
        for gX in gY:
            for i in gX:
                xVel = i[0] - i[2]
                yVel = i[1] - i[3]

                if (i[0] + i[4] > width):
                    i[0] = width - i[4]
                    i[2] = i[0] + xVel * bounce
                    yVel *= friction
                elif (i[0]-i[4] < 0):
                    i[0] = i[4]
                    i[2] = i[0] + xVel * bounce
                    yVel *= friction

                if (i[1] + i[4] > height):
                    i[1] = height - i[4]
                    i[3] = i[1] + yVel * bounce
                    xVel *= friction
                elif (i[1] - i[4] < 0):
                    i[1] = i[4]
                    i[3] = i[1] + yVel * bounce
                    xVel *= friction
                for g in gridArangments:
                    if x < 1 and g[0] < 0:
                        continue
                    elif x > gWidth-2 and g[0] > 0:
                        continue
                    elif y < 1 and g[1] < 0:
                        continue
                    elif y > gHeight-2 and g[1] > 0:
                        continue

                    #print(x)
                    #print(y)
                    #print(g)
                    for e in balls[y + g[1]][x + g[0]]:
                        if i is e:
                            continue
                        dx = e[0] - i[0]
                        dy = e[1] - i[1]
                        dist = dx*dx + dy*dy
                        if dist == 0:
                            continue
                        if dist < (e[4] + i[4]) ** 2:
                            dist = math.sqrt(dist)
                            dX = e[0] - i[0]
                            dY = e[1] - i[1]
                            minDist = i[4] + e[4]
                            displacementX = dX / dist
                            displacementY = dY / dist

                            delta = minDist - dist

                            i[0] -= delta * displacementX * 0.5 * bounce
                            i[1] -= delta * displacementY * 0.5 * bounce
                            e[0] += delta * displacementX * 0.5 * bounce
                            e[1] += delta * displacementY * 0.5 * bounce
            x += 1
        y += 1
def updateGrid():
    y = 0
    for gY in balls:
        x = 0
        for gX in gY:
            for i in gX:
                newGX = int(i[0] / GRIDSIZE)
                newGY = int(i[1] / GRIDSIZE)
                if newGX > gWidth-1 or newGX < 0:
                    continue
                elif newGY > gHeight-1 or newGY < 0:
                    continue
                if newGX != x or newGY != y:
                    balls[newGY][newGX].append(i)
                    if i in balls[y][x]:
                        balls[y][x].remove(i)
            x += 1
        y += 1

run = True
clock = pygame.time.Clock()
t = 0
while run:
    win.fill((0,0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in range(round(1 / DT)):
        updateBalls()
        updateGrid()
        constrain()
    y = 0
    for gY in balls:
        x = 0
        for gX in gY:
            for i in gX:
                pygame.draw.circle(win, i[5], (i[0], i[1]), i[4])
            x += 1
        y += 1
    #if t % 4 == 0:
        #balls[round(gHeight/2)][1].append([width/2, 10, width/2-10, 10, 8, (abs(math.sin(t/100)) * 255, abs(math.sin(t/50)) * 255, abs(math.sin(t/20)) * 255)])
    t += 1
    pygame.display.update()
    clock.tick(60)
pygame.quit()