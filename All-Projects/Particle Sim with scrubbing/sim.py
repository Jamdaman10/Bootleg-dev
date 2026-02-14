import pygame
import random
import math
pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))

particles = []
time = 0
t = 0

class emiter:
    def __init__(self, x, y, count, info, time, spawnDelay):
        self.x = x
        self.y = y
        self.count = count
        self.info = info
        self.time = time
        self.spawnDelay = spawnDelay
        self.positions = []
        self.velocitys = []
        self.accelerations = []
        self.lifeTimes = []
        self.ages = []
        self.startingAges = []
        self.died = []
        self.spawnedFrames = []
    def spawnOneParticle(self, thisTime, x=None, y=None):
        if x == None:
            pass
        else:
            self.x = x
            self.y = y
        self.positions.append((self.x + random.uniform(self.info["minStartX"], self.info["maxStartX"]),self.y + random.uniform(self.info["minStartY"], self.info["maxStartY"])))
        self.velocitys.append((random.uniform(self.info["minVelocity"][0], self.info["maxVelocity"][0]), random.uniform(self.info["minVelocity"][1], self.info["maxVelocity"][1])))
        self.accelerations.append((random.uniform(self.info["minAcceleration"][0], self.info["maxAcceleration"][0]), random.uniform(self.info["minAcceleration"][1], self.info["maxAcceleration"][1])))
        self.lifeTimes.append(random.uniform(self.info["minLifeTime"], self.info["maxLifeTime"]))
        self.startingAges.append(time + (thisTime * self.spawnDelay))
        self.ages.append(0)
        if self.info["deathEmmiter"] != None:
            x = self.positions[-1][0] + (self.velocitys[-1][0] * self.lifeTimes[-1]) + (self.accelerations[-1][0] * self.lifeTimes[-1] * self.lifeTimes[-1])
            y = self.positions[-1][1] + (self.velocitys[-1][1] * self.lifeTimes[-1]) + (self.accelerations[-1][1] * self.lifeTimes[-1] * self.lifeTimes[-1])
            
            self.info["deathEmmiter"].emmit(x, y, self.startingAges[-1] + self.lifeTimes[-1])
        
        if self.info["frameEmmiter"] != None:
            for i in range(round(self.lifeTimes[-1])):
                x = self.positions[-1][0] + (self.velocitys[-1][0] * i) + (self.accelerations[-1][0] * i * i)
                y = self.positions[-1][1] + (self.velocitys[-1][1] * i) + (self.accelerations[-1][1] * i * i)
                self.info["frameEmmiter"].emmit(x, y, self.startingAges[-1] + i)

    def emmit(self, x, y, startingTime):
        for e in range(self.time):
            for i in range(self.count):
                self.spawnOneParticle(e + startingTime, x, y)

    def drawParticles(self):
        for i in range(len(self.positions)):
            self.ages[i] = time - self.startingAges[i]

            if self.ages[i] < self.lifeTimes[i] and self.ages[i] > 0:
                zi = self.ages[i] / self.lifeTimes[i] + 0.00000001
                distance = (self.info["endColor"][0] - self.info["startColor"][0], self.info["endColor"][1] - self.info["startColor"][1], self.info["endColor"][2] - self.info["startColor"][2])
                position = ((self.positions[i][0] + (self.velocitys[i][0] * self.ages[i]) + (self.accelerations[i][0] * self.ages[i] * self.ages[i]), self.positions[i][1] + (self.velocitys[i][1] * self.ages[i]) + (self.accelerations[i][1] * self.ages[i] * self.ages[i])))
                col = (self.info["startColor"][0] + (distance[0] * zi), self.info["startColor"][1] + (distance[1] * zi), self.info["startColor"][2] + (distance[2] * zi))
                pygame.draw.circle(win,col ,position, self.info["startSize"] + ((self.info["endSize"] - self.info["startSize"]) * zi))
            else:
                pass
death = {"maxStartX": 0,
        "minStartX": 0,
        "maxStartY": 0,
        "minStartY": 0,
        "startColor": (255, 255 ,255),
        "endColor": (128, 128, 0),
        "startSize": 2,
        "endSize": 1,
        "maxVelocity": (3, 3),
        "minVelocity": (-3, -3),
        "maxAcceleration": (0, 0.05),
        "minAcceleration": (0, 0.05),
        "minLifeTime": 40,
        "maxLifeTime": 50,
        "deathEmmiter": None,
        "frameEmmiter": None,
        }
deathEmmiter = emiter(0, 0, 10, death, 1, 1)
trailEffect = {"maxStartX": 0,
        "minStartX": 0,
        "maxStartY": 0,
        "minStartY": 0,
        "startColor": (255, 255 ,0),
        "endColor": (255, 255, 255),
        "startSize": 2,
        "endSize": 1,
        "maxVelocity": (0, 0),
        "minVelocity": (0, 0),
        "maxAcceleration": (0, 0),
        "minAcceleration": (0, 0),
        "minLifeTime": 10,
        "maxLifeTime": 10,
        "deathEmmiter": None,
        "frameEmmiter": None,
        }
trailEmmiter = emiter(0, 0, 5, trailEffect, 1, 1)
particleInfo = {"maxStartX": 0,
                "minStartX": 0,
                "maxStartY": 0,
                "minStartY": 0,
                "startColor": (0, 0, 255),
                "endColor": (255, 255, 200),
                "startSize": 2,
                "endSize": 3,
                "maxVelocity": (3, -5),
                "minVelocity": (-3, -5),
                "maxAcceleration": (0, 0.02),
                "minAcceleration": (0, 0.02),
                "minLifeTime": 80,
                "maxLifeTime": 120,
                "deathEmmiter": deathEmmiter,
                "frameEmmiter": None,
                }

fire = emiter(width/2, height/2 + 200, 1, particleInfo, 100, 10)
fire.emmit(None, None, 0)
trailEmmiter.emmit(255,255, 0)

clock = pygame.time.Clock()
run = True
while run:
    win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    t += 1
    time += (pygame.mouse.get_pos()[0] / width) * 2 - 1
    time = max(0, time)
    fire.drawParticles()
    deathEmmiter.drawParticles()
    trailEmmiter.drawParticles()
    pygame.display.update()
    clock.tick(60)
pygame.quit()