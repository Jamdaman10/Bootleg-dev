import pygame
import random
import math

pygame.init()
width, height = 1200, 600
win = pygame.display.set_mode((width, height))

ANTSIZE = 2
WANDERSTRENGTH = 0.9
ANTSPEED = 1
FOODSIZE = 2

MAXVISION = 60
PHEROMONESIZE = 2

PHEROMONEDETECTION = 12
PHEROMONEDETECTIONANGLE = math.pi / 3
PHEROMONEDETECTIONDIST = 70

def sDist(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return dx*dx + dy*dy

class ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, math.tau)
        self.targetDir = random.uniform(0, math.tau)

        self.food = None
        self.time = 0
    def update(self):
        global dirtyGrid
        self.x += math.cos(self.angle) * ANTSPEED
        if self.x > width or self.x < 0:
            self.x -= math.cos(self.angle) * ANTSPEED

            normal = math.pi
            self.angle = 2 * normal - self.angle - math.pi
            self.targetDir = (2 * normal - self.angle - math.pi) + random.uniform(-0.3, 0.3)

        self.y += math.sin(self.angle) * ANTSPEED
        if self.y > height or self.y < 0:
            self.y -= math.sin(self.angle) * ANTSPEED

            normal = math.pi / 2
            self.angle = 2 * normal - self.angle - math.pi
            self.targetDir = (2 * normal - self.angle - math.pi) + random.uniform(-0.3, 0.3)

        for i in obstacles:
            if sDist(self.x, self.y, i[0], i[1]) < (i[2] + ANTSIZE)**2:
                self.x -= math.cos(self.angle) * ANTSPEED
                self.y -= math.sin(self.angle) * ANTSPEED
                normal = math.atan2(i[1] - self.y, i[0] - self.x)

                self.angle = 2 * normal - self.angle - math.pi
                self.targetDir = 2 * normal - self.angle - math.pi + random.uniform(-0.3, 0.3)


        self.angle = self.angle % math.tau
        difference = (self.angle-self.targetDir + math.pi) % math.tau
        if difference > math.pi:
            difference -= math.tau
        self.angle += math.copysign(0.09, difference)

        if self.food == None:
            self.findFood()
            self.moveToFood()
            if self.time % 20 == 1 and self.x > 0 and self.x < width-1 and self.y > 0 and self.y < height-1:
                close = False
                for i in getPheromonesAtPos(self.x, self.y, "pHome"):
                    if sDist(self.x, self.y, i[0], i[1]) < (PHEROMONESIZE+PHEROMONESIZE)**2:
                        i[2] += 2000
                        i[0] = self.x
                        i[1] = self.y
                        close = True
                        break
                if not close:
                    homePheromones.append([self.x, self.y, 2000])
                dirtyGrid = True
        else:
            self.findHome()
            if self.time % 20 == 1 and self.x > 0 and self.x < width-1 and self.y > 0 and self.y < height-1:
                close = False
                for i in getPheromonesAtPos(self.x, self.y, "pFood"):
                    if sDist(self.x, self.y, i[0], i[1]) < (PHEROMONESIZE+PHEROMONESIZE)**2:
                        i[2] += 2000
                        i[0] = self.x
                        i[1] = self.y
                        close = True
                        break
                if not close:
                    foodPheromones.append([self.x, self.y, 2000])
                dirtyGrid = True
            if sDist(home[0], home[1], self.x, self.y) < (ANTSIZE + 10)**2:
                self.food = None
                #ants.append(ant(width/2, height/2))
        self.targetDir += random.uniform(-WANDERSTRENGTH, WANDERSTRENGTH)
        self.time += 1
    def moveToFood(self):
        clump = None
        index = 0
        for i in foodClumps:
            if sDist(self.x, self.y, i[0], i[1]) < (i[2] + MAXVISION)**2:
                clump = index
                break
            index += 1
        if clump == None:
            return

        closest = None
        smallest = 99999999999999
        for i in food[index]:
            d = sDist(self.x, self.y, i[0], i[1])
            if d > MAXVISION**2:
                continue
            if d < smallest:
                smallest = d
                closest = i
                if d < (ANTSIZE + FOODSIZE)**2:
                    self.food = closest
                    food[index].remove(closest)
                    self.targetDir -= math.pi
                    self.angle -= math.pi
        if closest != None:
            self.targetDir = math.atan2(closest[1] - self.y, closest[0] - self.x)
    def samplePoint(self, target, a, dist):
        ammount = 0
        x = self.x + math.cos(a) * dist
        y = self.y + math.sin(a) * dist
        for i in getPheromonesAtPos(x, y, target):
            if sDist(x, y, i[0], i[1]) < (PHEROMONESIZE + PHEROMONEDETECTION)**2:
                ammount += i[2]
        #pygame.draw.circle(win, (255, 0, 0), (x, y), PHEROMONEDETECTION, 1)
        return ammount
    def findFood(self):
        left = self.samplePoint("pFood", -PHEROMONEDETECTIONANGLE + self.angle, PHEROMONEDETECTIONDIST)
        center = self.samplePoint("pFood", self.angle, PHEROMONEDETECTIONDIST)
        right = self.samplePoint("pFood", PHEROMONEDETECTIONANGLE + self.angle, PHEROMONEDETECTIONDIST)

        if left < 0 and right < 0 and center < 0:
            return
        if left > center and left > right:
            self.targetDir = self.angle - PHEROMONEDETECTIONANGLE
        elif right > center and right > left:
            self.targetDir = self.angle + PHEROMONEDETECTIONANGLE
        else:
            return
    def findHome(self):
        left = self.samplePoint("pHome", -PHEROMONEDETECTIONANGLE + self.angle, PHEROMONEDETECTIONDIST)
        center = self.samplePoint("pHome", self.angle, PHEROMONEDETECTIONDIST)
        right = self.samplePoint("pHome", PHEROMONEDETECTIONANGLE + self.angle, PHEROMONEDETECTIONDIST)

        if left < 0 and right < 0 and center < 0:
            return
        if sDist(home[0], home[1], self.x, self.y) < (10 + MAXVISION)**2:
            self.targetDir = math.atan2(home[1] - self.y, home[0] - self.x)
            return
        if left > center and left > right:
            self.targetDir = self.angle - PHEROMONEDETECTIONANGLE
        elif right > center and right > left:
            self.targetDir = self.angle + PHEROMONEDETECTIONANGLE
        else:
            return

    def draw(self):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), ANTSIZE)
        if self.food != None:
            pygame.draw.circle(win, (0, 255, 0), (self.x + math.cos(self.angle)*5, self.y + math.sin(self.angle)*5),FOODSIZE)

gridArangments = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

ants = []
foodPheromones = []
homePheromones = []
obstacles = []

for i in range(64):
    x, y, r = random.randrange(0, width), random.randrange(0, height), random.randrange(5, 80)
    while sDist(x, y, width/2, height/2) < (r + 10)**2:
        x, y, r = random.randrange(0, width), random.randrange(0, height), random.randrange(5, 80)
    obstacles.append((x, y, r))

gPheromones = []
GRIDSIZE = PHEROMONEDETECTION
gWidth = math.ceil(width / GRIDSIZE)
gHeight = math.ceil(height / GRIDSIZE)

for i in range(gHeight):
    collum = []
    for i in range(gWidth):
        collum.append([])
    gPheromones.append(collum)

def updateGrid():
    for y in range(gHeight):
        for x in range(gWidth):
            gPheromones[y][x] = []
    index = 0
    for i in homePheromones:
        gX, gY = int(i[0] / GRIDSIZE), int(i[1] / GRIDSIZE)
        gPheromones[gY][gX].append([index, "pHome"])
        index += 1
    
    index = 0
    for i in foodPheromones:
        gX, gY = int(i[0] / GRIDSIZE), int(i[1] / GRIDSIZE)
        gPheromones[gY][gX].append([index, "pFood"])
        index += 1
    return gPheromones

def getPheromonesAtPos(x, y, type):
    pheromones = []
    gX, gY = int(x / GRIDSIZE), int(y / GRIDSIZE)
    for i in gridArangments:
        if gX + i[0] > gWidth-1 or gX + i[0] < 0 or gY + i[1] > gHeight-1 or gY + i[1] < 0:
            continue
        cell = gPheromones[gY + i[1]][gX + i[0]]
        for c in cell:
            if type == "pHome" and c[1] == "pHome":
                pheromones.append(homePheromones[c[0]])
            elif type == "pFood" and c[1] == "pFood":
                pheromones.append(foodPheromones[c[0]])
        #pygame.draw.rect(win, (0, 255, 0), ((gX + i[0]) * GRIDSIZE, (gY + i[1]) * GRIDSIZE, GRIDSIZE, GRIDSIZE), 1)
    return pheromones
food = []

foodClumps = ((500, 500, 50, 1000), (200, 200, 10, 100))# x, y, radius, count

index = 0
for v in foodClumps:
    food.append([])
    for i in range(v[3]):
        safe = False
        safety = 0
        while not safe:
            f = (random.uniform(-v[2], v[2]) + v[0], random.uniform(-v[2], v[2]) + v[1])
            kill = False
            for o in obstacles:
                if sDist(o[0], o[1], f[0], f[1]) < (o[2] + FOODSIZE)**2:
                    if safety > 500:
                        obstacles.remove(o)
                        break
                    kill = True
                    break
            if not kill:
                safe = True
            safety += 1
        
        food[index].append(f)
    index += 1

home = (width/2, height/2)

for i in range(500):
    ants.append(ant(width/2, height/2))

dirtyGrid = False

run = True
clock = pygame.time.Clock()
t = 0
while run:
    win.fill((128, 128, 128))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    mouse = pygame.mouse.get_pos()
    for i in ants:
        i.update()
    for i in homePheromones:
        i[2] -= math.ceil(i[2] / 2000)#make sure pheromone dissapation is even
        if i[2] <= 0:
            homePheromones.remove(i)
            dirtyGrid = True
        if i[2] < 8000:
            continue
        zi = max(min(i[2] / 128000, 1), 0)
        nZi = 1 - zi
        pygame.draw.circle(win, (128 * nZi, 128 * nZi, 255*zi + 128*nZi), (i[0], i[1]), PHEROMONESIZE)

    for i in foodPheromones:
        i[2] -= math.ceil(i[2] / 2000)#make sure pheromone dissapation is even
        if i[2] <= 0:
            foodPheromones.remove(i)
            dirtyGrid = True
        if i[2] < 8000:
            continue
        zi = max(min(i[2] / 128000, 1), 0)
        nZi = 1 - zi
        pygame.draw.circle(win, (255*zi + 128*nZi, 128 * nZi, 128 * nZi), (i[0], i[1]), PHEROMONESIZE)
    if dirtyGrid:
        gPheromones = updateGrid()
    for i in ants:
        i.draw()
    for i in obstacles:
        pygame.draw.circle(win, (128, 96, 64), (i[0], i[1]), i[2])
    for i in food:
        for f in i:
            pygame.draw.circle(win, (0, 255, 0), f, FOODSIZE)
    pygame.draw.circle(win, (64, 64, 64), home, 10)
    pygame.display.update()
    #clock.tick(60)
pygame.quit()