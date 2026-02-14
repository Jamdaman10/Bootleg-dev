import math
import pygame
import pygame_shaders
import random

pygame.init()
width, height = 1200, 600
surf = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
win = pygame.Surface((width, height), pygame.SRCALPHA)
particleSurface = pygame.Surface((width, height), pygame.SRCALPHA)

screen_shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "fragment.glsl", win)

GRAVITY = 0.51
PLAYERSIZE = 10
COLLISIONDEPTH = 5
camX = 20
camY = 0
walls = [[0, 576, 1202, 28],
[0, 0, 1234, 28],
[1086, 200, 19, 339],
[1027, 200, 19, 339],
[886, 521, 146, 18],
[885, 399, 100, 18],
[655, 200, 376, 18],
[655, 206, 18, 328],
[529, 204, 18, 328],
[18, 203, 529, 19],
[0, 204, 300, 19],
[1101, 199, 125, 23],
[0, 166, 36, 77],
[1175, 168, 36, 77],
[46, 455, 66, 62],
[194, 421, 19, 123],
[59, 403, 155, 20],
[271, 504, 68, 13],
[410, 460, 68, 13],
[271, 413, 68, 13],
[413, 355, 68, 13],
[273, 316, 68, 13],
[414, 267, 68, 13],
[54, 344, 161, 13],
[759, 147, 67, 23],
[41, 116, 505, 12],
[531, 53, 16, 67],
[532, 60, 16, 67],
[517, 104, 20, 17],
[934, 185, 20, 17],
[969, 185, 20, 17],
[952, 169, 20, 17],
[700, 387, 13, 118],
[739, 389, 13, 118],
[875, 301, 13, 118],
[839, 303, 13, 118],
[741, 303, 112, 19],
[739, 319, 13, 74],
[701, 316, 13, 74],
[881, 391, 18, 13]
]
walls = [[0, 585, 450, 15],
[750, 585, 450, 15], [447, 566, 149, 10],
[589, 545, 149, 10], [2, 391, 890, 11],
[910, 391, 291, 11], [879, 402, 13, 156],
[910, 402, 13, 156], [879, 209, 13, 156],
[910, 209, 13, 156], [3, 209, 889, 14],
[923, 209, 280, 14], [735, 351, 144, 14],
[137, 376, 15, 15], [152, 361, 15, 15],
[167, 376, 15, 15], [0, 0, 17, 614],
[14, 490, 149, 18], [148, 508, 15, 48],
[110, 542, 38, 14], [95, 542, 15, 31],
[821, 293, 23, 22], [573, 182, 45, 13],
[508, 166, 45, 13], [563, 147, 45, 13],
[509, 129, 45, 13], [563, 108, 45, 13],
[506, 95, 45, 13], [561, 72, 45, 13],
[497, 53, 45, 13], [558, 33, 45, 13],
[263, 21, 285, 13], [507, 199, 51, 13],
[1185, 0, 15, 270], [1185, 375, 15, 120],
[1185, 570, 15, 120], [351, 313, 30, 8],
[324, 302, 30, 8], [295, 291, 30, 8],
[267, 279, 30, 8], [239, 267, 30, 8],
[385, 302, 30, 8], [419, 289, 30, 8],
[448, 276, 30, 8], [477, 262, 30, 8],
[498, 269, 9, 123], [239, 273, 9, 76],
[1001, 128, 9, 85], [975, 75, 60, 60],
[105, 150, 30, 60], [90, 75, 60, 60],
[195, 90, 30, 30], [146, 103, 53, 4],
[93, 57, 53, 14], [93, 37, 10, 24],
[115, 35, 10, 24], [135, 36, 10, 24],
[99, 53, 8, 16], [130, 55, 8, 16],
[111, 55, 8, 16], [95, 30, 5, 16],
[117, 30, 5, 16], [138, 31, 5, 16],
[107, 135, 5, 23], [123, 135, 5, 23],
[242, 76, 5, 138], [283, 73, 5, 138],
[246, 87, 40, 5], [246, 102, 40, 5],
[245, 119, 40, 5], [245, 135, 40, 5],
[243, 148, 40, 5], [245, 161, 40, 5],
[245, 177, 40, 5], [244, 194, 40, 5],
[275, 533, 67, 23], [945, 420, 30, 30],
[945, 480, 30, 30], [945, 540, 30, 30],
[1005, 540, 30, 30], [1005, 480, 30, 30],
[1005, 420, 30, 30], [1065, 420, 30, 30],
[1065, 480, 30, 30], [1065, 540, 30, 30],
[1125, 540, 30, 30], [1125, 480, 30, 30],
[1125, 420, 30, 30], [986, 127, 6, 19],
[986, 145, 18, 5], [1005, 137, 24, 5],
[1023, 127, 8, 14], [195, 87, 16, 9],
[690, 150, 45, 30], [740, 150, 45, 30],
[719, 156, 45, 8], [720, 166, 45, 8],
[621, 250, 9, 124], [648, 250, 9, 124],
[649, 250, 69, 7], [555, 250, 69, 7],
[368, 523, 69, 7], [295, 497, 69, 7],
[441, 496, 69, 7], [365, 467, 69, 7],
[439, 445, 69, 7], [295, 448, 69, 7],
[366, 425, 69, 7], [963, 309, 8, 53],
[965, 353, 148, 8], [1103, 305, 10, 49],
[963, 309, 10, 49], [581, 473, 276, 8]
]
#walls = [[0, 500, 10000, 40]]
for i in walls:
    for e in range(4):
        i[e] *= 1.5
projectiles = []
particles = []
class particle:
    def __init__(self, x, y, xVel, yVel, shape, color, size, lifeTime, sizeChange=0, borderColor=None, acceleration=(0, 0), drag=1, fade=0):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.shape = shape
        self.color = color
        self.size = size
        self.sizeChange = sizeChange
        self.borderColor = borderColor
        self.acceleration = acceleration
        self.drag = drag
        self.fade = fade
        self.lifeTime = lifeTime
    def update(self):
        self.x += self.xVel
        self.y += self.yVel
        self.xVel += self.acceleration[0]
        self.yVel += self.acceleration[1]
        self.color[3] -= self.fade
        if self.color[3] < 0:
            self.color[3] = 0
        if self.borderColor != None:
            self.borderColor[3] -= self.fade
            if self.borderColor[3] < 0:
                self.borderColor[3] = 0
        self.size += self.sizeChange
        if self.size < 1:
            self.size = 0
        self.xVel *= self.drag
        self.yVel *= self.drag
        self.lifeTime -= 1
        if self.lifeTime < 1:
            particles.remove(self)
    def draw(self):
        if self.shape == "square":
            pygame.draw.rect(particleSurface, self.color, (self.x-camX, self.y-camY, self.size, self.size))
            if self.borderColor != None:
                pygame.draw.rect(particleSurface, self.borderColor, (self.x-camX, self.y-camY, self.size, self.size), 2)
        elif self.shape == "circle":
            pygame.draw.circle(particleSurface, self.color, (self.x-camX, self.y-camY), self.size)
            if self.borderColor != None:
                pygame.draw.circle(particleSurface, self.borderColor, (self.x-camX, self.y-camY), self.size, 2)

class player:
    def __init__(self, x, y, color, maxHealth, speed, drag, weight, jumpHeight, wallSlidingSpeed, slamForce, abilitys):
        self.x = x
        self.y = y
        self.oldX = x
        self.oldY = y
        self.color = color
        self.maxHealth = maxHealth
        self.speed = speed
        self.drag = drag
        self.weight = weight
        self.jumpHeight = jumpHeight
        self.wallSlidingSpeed = wallSlidingSpeed
        self.slamForce = slamForce
        self.abilitys = abilitys
        self.health = self.maxHealth
        self.canJump = False
        self.climbDirection = None
        self.jumpedLastFrame = False
        self.dead = False
        for i in self.abilitys:
            i.player = self
    def update(self, keys):
        global screenShake
        self.xVel = (self.x - self.oldX) * self.drag
        self.yVel = (self.y - self.oldY)
        if self.x > width*1.5:
            self.x = 0
        elif self.x < 0:
            self.x = width*1.5
        if self.y > height*1.5:
            self.y = 0
        self.oldX = self.x
        self.oldY = self.y
        
        self.oldY -= GRAVITY * self.weight
        if keys["right"]:
            self.oldX -= self.speed
        if keys["left"]:
            self.oldX += self.speed
        if keys["jump"] and self.canJump:
            if self.climbDirection == None:
                self.oldY = self.y + self.jumpHeight
                self.canJump = False
                self.jumpedLastFrame = True
            else:
                if self.climbDirection == "right" and keys["left"] and not keys["right"]:
                    self.oldY = self.y + self.jumpHeight
                    self.canJump = False
                    self.climbDirection = None
                    self.jumpedLastFrame = True
                elif self.climbDirection == "left" and keys["right"] and not keys["left"]:
                    self.oldY = self.y + self.jumpHeight
                    self.canJump = False
                    self.climbDirection = None
                    self.jumpedLastFrame = True
        if keys["slam"]:
            self.oldY -= self.slamForce
        if keys["a1"]:
            self.abilitys[0].use()
        if keys["a2"]:
            self.abilitys[1].use()
        if keys["a3"]:
            self.abilitys[2].use()
        for i in self.abilitys:
            i.update()
        for i in range(2):
            self.x += self.xVel / 2
            for i in walls:
                pRect = pygame.Rect(self.x, self.y, PLAYERSIZE, PLAYERSIZE)
                wRect = pygame.Rect(i[0], i[1], i[2], i[3])
                if pRect.colliderect(wRect):
                    while pRect.colliderect(wRect):
                        self.x -= self.xVel / COLLISIONDEPTH
                        pRect = pygame.Rect(self.x, self.y, PLAYERSIZE, PLAYERSIZE)
                        wRect = pygame.Rect(i[0], i[1], i[2], i[3])
                    if self.xVel > 0 and keys["right"]:
                        self.yVel *= self.wallSlidingSpeed
                        self.canJump = True
                        self.climbDirection = "right"
                        if random.randrange(0, 5) == 4:
                            particles.append(particle(self.x+PLAYERSIZE + 2, self.y, random.uniform(-1, -5), random.uniform(-1, -8), "circle", [100, 100, 100, 255], random.uniform(3, 4), random.uniform(10, 20), -0.3, None, (0, 0.5), 1, 6))
                    elif self.xVel < 0 and keys["left"]:
                        self.yVel *= self.wallSlidingSpeed
                        self.canJump = True
                        self.climbDirection = "left"
                        if random.randrange(0, 5) == 4:
                            particles.append(particle(self.x - 2, self.y, random.uniform(1, 5), random.uniform(-1, -8), "circle", [100, 100, 100, 255], random.uniform(3, 4), random.uniform(10, 20), -0.3, None, (0, 0.5), 1, 6))
            self.y += self.yVel / 2
            for i in walls:
                pRect = pygame.Rect(self.x, self.y, PLAYERSIZE, PLAYERSIZE)
                wRect = pygame.Rect(i[0], i[1], i[2], i[3])
                if pRect.colliderect(wRect):
                    while pRect.colliderect(wRect):
                        self.y -= self.yVel / COLLISIONDEPTH
                        pRect = pygame.Rect(self.x, self.y, PLAYERSIZE, PLAYERSIZE)
                        wRect = pygame.Rect(i[0], i[1], i[2], i[3])
                    if self.yVel > 0 and not self.jumpedLastFrame:
                        self.canJump = True
                        self.climbDirection = None
                    if keys["slam"]:
                        if self.yVel > 10:
                            screenShake += self.yVel / 3
                            for i in range(3):
                                particles.append(particle(self.x+random.uniform(0, PLAYERSIZE),self.y+PLAYERSIZE, random.uniform(-3, 3), random.uniform(-3, -6), "square", [100,100,100,255],random.uniform(6, 8), random.uniform(10,40), -0.1, acceleration=(0, 0.4), fade=3))
                            for i in range(3):
                                particles.append(particle(self.x+random.uniform(0, PLAYERSIZE),self.y+PLAYERSIZE, random.uniform(-8, 8), random.uniform(0, -1), "circle", [128, 128, 128, 128], random.uniform(7, 10), 50, -0.04, drag=0.8, fade=random.uniform(4,5)))
        self.jumpedLastFrame = False
        
    def draw(self):
        pygame.draw.rect(win,self.color, (self.x - camX, self.y - camY, PLAYERSIZE, PLAYERSIZE))
    def drawUI(self):
        if self.dead == False:
            pygame.draw.rect(win, (20, 20, 20), (self.x - 10 - camX, self.y - 10 - camY, 30, 5))
            zi = self.health / self.maxHealth
            pygame.draw.rect(win, (255 - (zi * 255), zi * 255, 0), (self.x - 10 - camX, self.y - 10 - camY, zi * 30, 5))
            for i in self.abilitys:
                i.update()
                i.draw()
    def damage(self, ammount):
        self.health -= ammount
        if self.health < 1:
            self.die()
    def die(self):
        self.dead = True
class projectile:
    def __init__(self, name, x, y, color, size, direction, shape, speed, player):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.direction = direction
        self.shape = shape
        self.speed = speed
        self.player = player
    def update(self):
        for i in range(2):
            self.x += math.cos(self.direction) * self.speed / 2
            self.y += math.sin(self.direction) * self.speed / 2
            if self.player == p1:
                playerRect = pygame.Rect(p2.x, p2.y, PLAYERSIZE, PLAYERSIZE)
            else:
                playerRect = pygame.Rect(p1.x, p1.y, PLAYERSIZE, PLAYERSIZE)
            if self.shape == "square":
                myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                if myRect.colliderect(playerRect):
                    self.hitPlayer()
            elif self.shape == "circle":
                if math.dist((playerRect.x + (PLAYERSIZE / 2), playerRect.y + (PLAYERSIZE / 2)), (self.x, self.y)) < self.size + PLAYERSIZE:
                    self.hitPlayer()
            for wall in walls:
                wRect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
                if self.shape == "square":
                    myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                    if myRect.colliderect(wRect):
                        self.hitWall()
                elif self.shape == "circle":
                    if wRect.collidepoint((self.x, self.y)):
                        self.hitWall()
        self.specialUpdate()
    def hitPlayer(self):
        pass
    def hitWall(self):
        pass
    def specialUpdate(self):
        pass
    def draw(self):
        if self.shape == "square":
            pygame.draw.rect(win, self.color, (self.x - camX, self.y - camY, self.size, self.size))
        elif self.shape == "circle":
            pygame.draw.circle(win, self.color, (self.x - camX, self.y - camY), self.size)
    def delete(self):
        if self in projectiles:
            projectiles.remove(self)
class ember(projectile):
    def __init__(self, x, y, player, direction):
        super().__init__("ember", x, y, (255, 100, 0), 5, direction, "circle", 13, player)
    def hitPlayer(self):
        global screenShake
        if self.player == p1:
            p2.damage(8)
        else:
            p1.damage(8)
        
        for i in range(8):
            r = random.randrange(200, 255)
            g = random.randrange(50, 150)
            b = 0
            alpha = random.randrange(80, 255)
            size = random.uniform(4, 10)
            speed = random.uniform(1, 4)
            particles.append(particle( self.x, self.y, random.uniform(-speed, speed), random.uniform(-speed, speed), "circle", [r, g, b, alpha], size, random.randint(20, 50), -0.15, fade=4, drag=random.uniform(0.85, 0.95)))
        for i in range(3):
            particles.append(particle(self.x, self.y, random.uniform(-1, 1), random.uniform(-1, 1), "circle", [255, 180, 80, 100], random.uniform(12, 20), 20, -0.2, fade=3))
        screenShake += 3
        self.delete()
    def hitWall(self):
        for i in range(8):
            r = random.randrange(200, 255)
            g = random.randrange(50, 150)
            b = 0
            alpha = random.randrange(80, 255)
            size = random.uniform(4, 10)
            speed = random.uniform(1, 4)
            particles.append(particle( self.x, self.y, random.uniform(-speed, speed), random.uniform(-speed, speed), "circle", [r, g, b, alpha], size, random.randint(20, 50), -0.15, fade=4, drag=random.uniform(0.85, 0.95)))
        for i in range(3):
            particles.append(particle(self.x, self.y, random.uniform(-1, 1), random.uniform(-1, 1), "circle", [255, 180, 80, 100], random.uniform(12, 20), 20, -0.2, fade=3))
        self.delete()
    def specialUpdate(self):
        particles.append(particle(self.x, self.y, 0, 0, "circle", [255, 120, 40, 100], 6, 10, -0.3, fade=10))
class teleportProjectile(projectile):
    def __init__(self, x, y, player, direction):
        super().__init__("teleporter", x, y, (0, 255, 0), 3, direction, "circle", 13, player)
        self.xSpeed = math.cos(self.direction) * self.speed
        self.ySpeed = math.sin(self.direction) * self.speed
    def hitWall(self):
        for i in range(10):
            particles.append(particle(self.player.x, self.player.y, random.uniform(-1, 1), random.uniform(-1, 1), "square", [0, 255, 0, 128], 6, 60, 0, fade=5))
        self.player.x = self.x
        self.player.y = self.y
        self.player.xVel = 0
        self.player.yVel = 0
        self.player.oldX = self.x - self.xSpeed
        self.player.oldY = self.y - self.ySpeed
        self.delete()
    def hitPlayer(self):
        oldX = self.player.x
        oldY = self.player.y
        self.player.x = self.x
        self.player.y = self.y
        self.player.xVel = 0
        self.player.yVel = 0
        self.player.oldX = self.x
        self.player.oldY = self.y
        if self.player == p1:
            p2.x = oldX
            p2.y = oldY
            p2.xVel = 0
            p2.yVel = 0
            p2.oldX = p2.x
            p2.oldY = p2.y
        else:
            p1.x = oldX
            p1.y = oldY
            p1.xVel = 0
            p1.yVel = 0
            p1.oldX = p1.x
            p1.oldY = p1.y
        self.delete()
    def update(self):
        for i in range(2):
            self.y += self.ySpeed / 2
            self.x += self.xSpeed / 2
            if self.player == p1:
                playerRect = pygame.Rect(p2.x, p2.y, PLAYERSIZE, PLAYERSIZE)
            else:
                playerRect = pygame.Rect(p1.x, p1.y, PLAYERSIZE, PLAYERSIZE)
            if self.shape == "square":
                myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                if myRect.colliderect(playerRect):
                    self.hitPlayer()
                    break
            elif self.shape == "circle":
                if math.dist((playerRect.x + (PLAYERSIZE / 2), playerRect.y + (PLAYERSIZE / 2)), (self.x, self.y)) < self.size + PLAYERSIZE:
                    self.hitPlayer()
                    break
            for wall in walls:
                wRect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
                if self.shape == "square":
                    myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                    if myRect.colliderect(wRect):
                        self.hitWall()
                        break
                elif self.shape == "circle":
                    if wRect.collidepoint((self.x, self.y)):
                        self.hitWall()
                        break
        self.specialUpdate()
    def specialUpdate(self):
        for i in range(3):
            particles.append(particle(self.x + random.randrange(-3,3), self.y + random.randrange(-3,3), random.uniform(-1,1), random.uniform(-1,1), "square", [0, random.randrange(196,255), 0, 255], 
                                    6, 10, -0.6, drag=0.9, fade=25.5))
class fist(projectile):
    def __init__(self, x, y, direction, player):
        super().__init__("fist", x, y, player.color, 8, direction, "square", 6, player)
        self.time = 0
    def specialUpdate(self):
        self.x += self.player.x - self.player.oldX
        self.y += self.player.y - self.player.oldY
        self.time += 1
        if self.time == 8:
            self.direction -= math.pi
        elif self.time == 16:
            self.delete()
    def hitPlayer(self):
        global screenShake
        if self.player == p1:
            p2.damage(10)
        else:
            p1.damage(10)
        for i in range(2):
            particles.append(particle(self.x, self.y, random.uniform(-3, 3), random.uniform(-3, 3), "circle", [self.color[0],self.color[1],self.color[2],255], 4, random.uniform(5, 30), -0.1, acceleration=(0,0.3), fade=6))
        screenShake += 2
        self.delete()
class stickyBomb(projectile):
    def __init__(self, x, y, direction, player):
        super().__init__("sticky bomb", x, y, (255, 0, 0), 4, direction, "circle", 24, player)
        self.xSpeed = math.cos(direction) * self.speed
        self.ySpeed = math.sin(direction) * self.speed
        self.connectedToPlayer = False
        self.active = False
    def hitWall(self):
        self.x -= self.xSpeed/3
        self.y -= self.ySpeed/3
        self.speed = 0
        self.xSpeed = 0
        self.ySpeed = 0
        self.active = True
    def hitPlayer(self):
        if not self.active:
            self.speed = 0
            self.xSpeed = 0
            self.ySpeed = 0
            self.connectedToPlayer = True
            if self.player == p1:
                self.xDist = (p2.x - self.x) / 2
                self.yDist = (p2.y - self.y) / 2
            else:
                self.xDist = (p1.x - self.x) / 2
                self.yDist = (p1.y - self.y) / 2
            self.active = True
    def specialUpdate(self):
        if not self.active:
            self.ySpeed += 0.4
        if self.connectedToPlayer:
            if self.player == p1:
                self.x = p2.x + self.xDist
                self.y = p2.y + self.yDist
            else:
                self.x = p1.x + self.xDist
                self.y = p1.y + self.yDist
    def explode(self):
        global screenShake
        for i in range(15):
            particles.append(particle(self.x, self.y, random.uniform(-2,2),random.uniform(-2,2),"circle",[random.uniform(128,255),random.uniform(64, 128), 0, 255], random.uniform(3,6), random.randrange(30,60), fade = 2, drag=0.98))
        for i in range(12):
            particles.append(particle(self.x, self.y, random.uniform(-2,2),random.uniform(-2,2),"circle",[128, 128, 128, random.randrange(64, 255)], random.uniform(10,12), random.randrange(80,120), fade = 2, drag=0.95))
        if self.player == p1:
            if math.dist((p2.x, p2.y), (self.x, self.y)) < 50:
                p2.damage(30)
        else:
            if math.dist((p1.x, p1.y), (self.x, self.y)) < 50:
                p1.damage(30)
        if math.dist((p1.x, p1.y), (self.x, self.y)) < 100:
            angleToPlayer = math.atan2(self.y - p1.y, self.x - p1.x)
            p1.oldX += math.cos(angleToPlayer) * min((100 - math.dist((p1.x, p1.y), (self.x, self.y))) / 2, 20)
            p1.oldY += math.sin(angleToPlayer) * min((100 - math.dist((p1.x, p1.y), (self.x, self.y))) / 2, 20)
        if math.dist((p2.x, p2.y), (self.x, self.y)) < 100:
            angleToPlayer = math.atan2(self.y - p2.y, self.x - p2.x)
            p2.oldX += math.cos(angleToPlayer) * min((100 - math.dist((p2.x, p2.y), (self.x, self.y))) / 2, 20)
            p2.oldY += math.sin(angleToPlayer) * min((100 - math.dist((p2.x, p2.y), (self.x, self.y))) / 2, 20)
        screenShake += 10
        self.delete()
    def update(self):
        for i in range(2):
            self.x += self.xSpeed / 2
            self.y += self.ySpeed / 2
            if self.player == p1:
                playerRect = pygame.Rect(p2.x, p2.y, PLAYERSIZE, PLAYERSIZE)
            else:
                playerRect = pygame.Rect(p1.x, p1.y, PLAYERSIZE, PLAYERSIZE)
            if self.shape == "square":
                myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                if myRect.colliderect(playerRect):
                    self.hitPlayer()
            elif self.shape == "circle":
                if math.dist((playerRect.x + (PLAYERSIZE / 2), playerRect.y + (PLAYERSIZE / 2)), (self.x, self.y)) < self.size + PLAYERSIZE:
                    self.hitPlayer()
            for wall in walls:
                wRect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
                if self.shape == "square":
                    myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                    if myRect.colliderect(wRect):
                        self.hitWall()
                elif self.shape == "circle":
                    if wRect.collidepoint((self.x, self.y)):
                        self.hitWall()
        self.specialUpdate()
class trackingSpell(projectile):
    def __init__(self, x, y, direction, player):
        super().__init__("magic missle", x, y, (148,0,211), 4, direction, "circle", 1, player)
    def specialUpdate(self):
        if self.player == p1:
            otherPlayer = p2
        else:
            otherPlayer = p1
        targetAngle = math.atan2(otherPlayer.y - self.y, otherPlayer.x - self.x)
        angle_diff = (targetAngle - self.direction) % (360 * (math.pi / 180))
        if angle_diff > 180 * (math.pi / 180):
            angle_diff -= 360 * (math.pi / 180)
        if abs(angle_diff) > 0.08:
            self.direction += 0.08 * (1 if angle_diff > 0 else -1)
        else:
            self.direction = targetAngle
        self.speed += 0.1
        #self.speed = min(self.speed, 20)
        col = random.uniform(128, 255)
        particles.append(particle(self.x, self.y, random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), "square", [col, random.uniform(64, 128), col, 255], random.uniform(4, 8), random.uniform(20, 50), fade=4, acceleration=(0, 0.1), drag=0.95))
    def hitPlayer(self):
        global screenShake
        if self.player == p1:
            p2.damage(19)
        else:
            p1.damage(19)
        screenShake += 8
        for i in range(12):
            col = random.uniform(128, 255)
            particles.append(particle(self.x, self.y, random.uniform(-3.5, 3.5), random.uniform(-3.5, 3.5), "circle", [col, random.uniform(64, 128), col, 255], random.uniform(4, 8), random.uniform(20, 50), fade=4, acceleration=(0, 0.1), drag=0.95))
        self.delete()
    def hitWall(self):
        for i in range(12):
            col = random.uniform(128, 255)
            particles.append(particle(self.x, self.y, random.uniform(-3.5, 3.5), random.uniform(-3.5, 3.5), "circle", [col, random.uniform(64, 128), col, 255], random.uniform(4, 8), random.uniform(20, 50), fade=4, acceleration=(0, 0.1), drag=0.95))
        self.delete()
class napalm(projectile):
    def __init__(self, x, y, direction, player):
        super().__init__("napalm", x, y, (255, 196, 0), 4, direction, "circle", random.uniform(2,4), player)
        self.xSpeed = math.cos(self.direction) * self.speed
        self.ySpeed = math.sin(self.direction) * self.speed
    def specialUpdate(self):
        col = random.uniform(128, 255)
        smokeCol = random.uniform(128, 255)
        particles.append(particle(self.x, self.y, random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), "circle", [smokeCol,smokeCol,smokeCol, random.uniform(64, 196)], random.uniform(4,6), random.uniform(50,60),0.2,fade=9,acceleration=(0,-0.12)))
        particles.append(particle(self.x, self.y, random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), "circle", [col, col-random.uniform(64, 128), 0, 255], random.uniform(3, 5), random.uniform(20, 60), fade=8, acceleration=(0, 0.2), drag=0.95))
        self.ySpeed += 0.1
    def update(self):
        for i in range(2):
            self.x += self.xSpeed
            self.y += self.ySpeed
            if self.player == p1:
                playerRect = pygame.Rect(p2.x, p2.y, PLAYERSIZE, PLAYERSIZE)
            else:
                playerRect = pygame.Rect(p1.x, p1.y, PLAYERSIZE, PLAYERSIZE)
            if self.shape == "square":
                myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                if myRect.colliderect(playerRect):
                    self.hitPlayer()
            elif self.shape == "circle":
                if math.dist((playerRect.x + (PLAYERSIZE / 2), playerRect.y + (PLAYERSIZE / 2)), (self.x, self.y)) < self.size + PLAYERSIZE:
                    self.hitPlayer()
            for wall in walls:
                wRect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
                if self.shape == "square":
                    myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                    if myRect.colliderect(wRect):
                        self.hitWall()
                elif self.shape == "circle":
                    if wRect.collidepoint((self.x, self.y)):
                        self.hitWall()
        self.specialUpdate()
    def hitPlayer(self):
        global screenShake
        if self.player == p1:
            p2.damage(15)
        else:
            p1.damage(15)
        for i in range(7):
            particles.append(particle(self.x, self.y, random.uniform(-1,1),random.uniform(-1,1),"circle",[random.uniform(128,255),random.uniform(64, 128), 0, 255], random.uniform(5,8), random.randrange(30,60), fade = 4, drag=0.98))
        for i in range(3):
            particles.append(particle(self.x, self.y, random.uniform(-1,1),random.uniform(-1,1),"circle",[128, 128, 128, random.randrange(64, 255)], random.uniform(10,12), random.randrange(80,120), fade = 2, drag=0.95))
        screenShake += 8
        self.delete()
    def hitWall(self):
        for i in range(7):
            particles.append(particle(self.x, self.y, random.uniform(-1,1),random.uniform(-1,1),"circle",[random.uniform(128,255),random.uniform(64, 128), 0, 255], random.uniform(5,8), random.randrange(30,60), fade = 4, drag=0.98))
        for i in range(3):
            particles.append(particle(self.x, self.y, random.uniform(-1,1),random.uniform(-1,1),"circle",[128, 128, 128, random.randrange(64, 255)], random.uniform(10,12), random.randrange(80,120), fade = 2, drag=0.95))
        self.delete()
        
class molotovCocktail(projectile):
    def __init__(self, x, y, direction, player):
        super().__init__("molotov cocktail", x, y, (150, 75, 0), 8, direction, "square", 12, player)
        self.xSpeed = math.cos(self.direction) * self.speed
        self.ySpeed = math.sin(self.direction) * self.speed
        self.ySpeed -= 2
    def specialUpdate(self):
        particles.append(particle(self.x, self.y, random.uniform(-1,1),random.uniform(-1,1),"circle",[255,random.uniform(196, 255), 0, 255], random.uniform(3,5), random.randrange(5,10), drag=0.98, acceleration=(0,-0.1), fade=25))
        self.ySpeed += 0.28
    def update(self):
        for i in range(2):
            self.x += self.xSpeed / 2
            self.y += self.ySpeed / 2
            if self.player == p1:
                playerRect = pygame.Rect(p2.x, p2.y, PLAYERSIZE, PLAYERSIZE)
            else:
                playerRect = pygame.Rect(p1.x, p1.y, PLAYERSIZE, PLAYERSIZE)
            if self.shape == "square":
                myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                if myRect.colliderect(playerRect):
                    self.hitPlayer()
            elif self.shape == "circle":
                if math.dist((playerRect.x + (PLAYERSIZE / 2), playerRect.y + (PLAYERSIZE / 2)), (self.x, self.y)) < self.size + PLAYERSIZE:
                    self.hitPlayer()
            for wall in walls:
                wRect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
                if self.shape == "square":
                    myRect = pygame.Rect(self.x, self.y, self.size, self.size)
                    if myRect.colliderect(wRect):
                        self.hitWall()
                elif self.shape == "circle":
                    if wRect.collidepoint((self.x, self.y)):
                        self.hitWall()
        self.specialUpdate()
    def hitWall(self):
        self.x -= self.xSpeed
        self.y -= self.ySpeed
        for i in range(13):
            projectiles.append(napalm(self.x+(self.size/2), self.y+(self.size/2), random.uniform(0,360)*(math.pi/180), self.player))
        self.delete()
    def hitPlayer(self):
        global screenShake
        if self.player == p1:
            p2.damage(30)
        else:
            p1.damage(30)
        for i in range(6):
            for i in range(7):
                particles.append(particle(self.x, self.y, random.uniform(-1,1),random.uniform(-1,1),"circle",[random.uniform(128,255),random.uniform(64, 128), 0, 255], random.uniform(5,8), random.randrange(30,60), fade = 4, drag=0.98))
            for i in range(3):
                particles.append(particle(self.x, self.y, random.uniform(-1,1),random.uniform(-1,1),"circle",[128, 128, 128, random.randrange(64, 255)], random.uniform(10,12), random.randrange(80,120), fade = 2, drag=0.95))
        screenShake = 16
        self.delete()
class diode(projectile):
    def __init__(self, x, y, direction, player):
        super().__init__("diode", x, y, (196, 196, 196), 4, direction, "circle", 0, player)
        self.timer = 300
        self.active = False
    def specialUpdate(self):
        for i in range(2):
            particles.append(particle(self.x, self.y, 0, 0, "circle", [255,0,0,random.randrange(128,255)], random.uniform(1.8, 3), 5, 0, fade=64))
        if self.active:
            self.timer -= 1
            if self.timer <= 1:
                for i in range(4):
                    smokeCol = random.uniform(128, 255)
                    particles.append(particle(self.x, self.y, random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), "circle", [smokeCol,smokeCol,smokeCol, random.uniform(64, 196)], random.uniform(4,6), random.uniform(50,60),0.2,fade=9,acceleration=(0,-0.12)))
                for i in range(3):
                    particles.append(particle(self.x, self.y, random.uniform(-1, 1),random.uniform(-1, 1), "circle", [255,255,0,255], random.randrange(1,3), random.uniform(10,30), acceleration=(0,0.2)))
                self.delete()
class missle(projectile):
    def __init__(self, x, y, direction, player):
        super().__init__("missle", x, y, (200, 0, 0), 6, direction, "square", 3, player)
    def specialUpdate(self):
        if self.player == p1:
            otherPlayer = p2
        else:
            otherPlayer = p1
        self.targetAngle = math.atan2(otherPlayer.y - self.y, otherPlayer.x - self.x)
        angle_diff = (self.targetAngle - self.direction) % (360 * (math.pi / 180))
        if angle_diff > 180 * (math.pi / 180):
            angle_diff -= 360 * (math.pi / 180)
        if abs(angle_diff) > 0.1:
            self.direction += 0.1 * (1 if angle_diff > 0 else -1)
        else:
            self.direction = self.targetAngle
        self.direction += random.uniform(-self.speed, self.speed) / 20
        self.speed += random.uniform(0.1, 0.05)
        col = random.uniform(196, 255)
        smokeCol = random.uniform(128, 255)
        particles.append(particle(self.x, self.y, random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), "circle", [smokeCol,smokeCol,smokeCol, random.uniform(64, 196)], random.uniform(4,6), random.uniform(50,60),0.2,fade=9,acceleration=(0,-0.12)))
        particles.append(particle(self.x, self.y, random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), "circle", [col, col-random.uniform(0, 96), 0, 255], random.uniform(3, 5), random.uniform(10, 20), fade=8, drag=0.95))
    def hitPlayer(self):
        global screenShake
        if self.player == p1:
            p2.damage(8)
        else:
            p1.damage(8)
        for i in range(15):
            particles.append(particle(self.x, self.y, random.uniform(-2,2),random.uniform(-2,2),"circle",[random.uniform(128,255),random.uniform(64, 128), 0, 255], random.uniform(3,6), random.randrange(30,60), fade = 2, drag=0.98))
        for i in range(12):
            particles.append(particle(self.x, self.y, random.uniform(-2,2),random.uniform(-2,2),"circle",[128, 128, 128, random.randrange(64, 255)], random.uniform(10,12), random.randrange(80,120), fade = 2, drag=0.95))
        screenShake += 8
        self.delete()
    def hitWall(self):
        global screenShake
        for i in range(15):
            particles.append(particle(self.x, self.y, random.uniform(-2,2),random.uniform(-2,2),"circle",[random.uniform(128,255),random.uniform(64, 128), 0, 255], random.uniform(3,6), random.randrange(30,60), fade = 2, drag=0.98))
        for i in range(12):
            particles.append(particle(self.x, self.y, random.uniform(-2,2),random.uniform(-2,2),"circle",[128, 128, 128, random.randrange(64, 255)], random.uniform(10,12), random.randrange(80,120), fade = 2, drag=0.95))
        screenShake += 4
        self.delete()
class ability:
    def __init__(self, name, color1, color2, index, delay):
        self.name = name
        self.color1 = color1
        self.color2 = color2
        self.index = index
        self.player = None
        self.delay = delay
        self.timer = 0
    def update(self):
        if self.timer > 1:
            self.timer -= 1
    def use(self):
        if self.timer <= 1:
            self.timer = self.delay
            self.activate()
    def activate(self):
        pass
    def draw(self): 
        if self.player == p1:
            pygame.draw.rect(win,(70, 70, 70), (20 + (self.index * 50), height - 70, 50, 50), 4)
            pygame.draw.circle(win, self.color2, (20 + (self.index * 50) + 25, height - 70 + 25), 20)
            pygame.draw.circle(win, self.color1, (20 + (self.index * 50) + 25, height - 70 + 25), 15)
            if self.timer > 1:
                zi = self.timer / self.delay
                pygame.draw.rect(win,(200, 200, 200), (20 + (self.index * 50), height - 70, 50, zi * 50))
        else:
            pygame.draw.rect(win,(70, 70, 70), ((width - 70) - (self.index * 50), height - 70, 50, 50), 4)
            pygame.draw.circle(win, self.color2, ((width - 70) - (self.index * 50) + 25, height - 70 + 25), 20)
            pygame.draw.circle(win, self.color1, ((width - 70) - (self.index * 50) + 25, height - 70 + 25), 15)
            if self.timer > 1:
                zi = self.timer / self.delay
                pygame.draw.rect(win,(200, 200, 200), ((width - 70) - (self.index * 50), height - 70, 50, zi * 50))

class dash(ability):
    def __init__(self, index):
        super().__init__("dash", (100, 100, 255), (0, 0, 255), index, 200)
        self.effectTimer = 0
    def activate(self):
        direction = [0, 0]
        if self.player == p1:
            controls = p1Controls
        else:
            controls = p2Controls
        if controls["left"]:
            direction[0] -= 1
        if controls["right"]:
            direction[0] += 1
        if controls["jump"]:
            direction[1] -= 1
        if controls["slam"]:
            direction[1] += 1
        if abs(direction[1]) > 0:
            self.player.oldX = self.player.x - (direction[0] * 25) / 1.44
        else:
            self.player.oldX = self.player.x - (direction[0] * 25)
        if abs(direction[0]) > 0:
            self.player.oldY = self.player.y - (direction[1] * 10) / 1.44
        else:
            self.player.oldY = self.player.y - (direction[1] * 10)
        self.effectTimer = 25
    def update(self):
        if self.timer > 1:
            self.timer -= 1
        if self.effectTimer > 1:
            self.effectTimer -= 1
            particles.append(particle(self.player.x, self.player.y, 0, 0, "square", [0, 0, 0, 0], PLAYERSIZE, 10, 0, [128, 128, 255, 128], fade=10))
class fireball(ability):
    def __init__(self, index):
        super().__init__("fireball", (255, 255, 60), (255, 100, 0), index, 1000)
    def activate(self):
        direction = [0, 0]
        if self.player == p1:
            controls = p1Controls
        else:
            controls = p2Controls
        if controls["left"]:
            direction[0] -= 1
        if controls["right"]:
            direction[0] += 1
        if controls["jump"]:
            direction[1] -= 1
        if controls["slam"]:
            direction[1] += 1
        projectiles.append(ember(self.player.x, self.player.y, self.player, math.atan2(direction[1], direction[0])))
        for i in range(4):
            projectiles.append(ember(self.player.x, self.player.y, self.player, math.atan2(direction[1], direction[0]) + random.uniform(-0.1, 0.1)))
class parry(ability):
    def __init__(self, index):
        super().__init__("parry", (128, 128, 128), (200, 200, 255), index, 600)
        self.parryTimer = 0
    def activate(self):
        if self.parryTimer <= 1:
            self.parryTimer = 20
    def update(self):
        global freezeFrame
        if self.timer > 1:
            self.timer -= 1
        if self.parryTimer > 1:
            self.parryTimer -= 1
            pygame.draw.circle(win, (50, 50, 200), (self.player.x + (PLAYERSIZE / 2) - camX, self.player.y + (PLAYERSIZE / 2) - camY), PLAYERSIZE*3 + math.log(self.parryTimer*5), 2)
            for pro in projectiles:
                if math.dist((pro.x, pro.y), (self.player.x, self.player.y)) < PLAYERSIZE * 3 and pro.player != self.player:
                    if hasattr(pro, "explode"):
                        if pro.connectedToPlayer:
                            pro.connectedToPlayer = False
                            pro.active = False
                            pro.xSpeed = pro.xDist * 2
                            pro.ySpeed = pro.yDist * 2
                    pro.player = self.player
                    pro.direction -= math.pi
                    if hasattr(pro, "xSpeed"):
                        pro.xSpeed *= -1
                        pro.ySpeed *= -1
                    particles.append(particle(pro.x, pro.y, 0, 0, "circle", [255, 255, 255, 128], 1, 40, 0.6, fade=5))
                    freezeFrame = 10
            if self.player == p1:
                self.otherPlayer = p2
            else:
                self.otherPlayer = p1
            for i in self.otherPlayer.abilitys:
                if isinstance(i, groundPound) and i.active > 0:
                    if math.dist((self.player.x, self.player.y), (self.otherPlayer.x, self.otherPlayer.y)) < PLAYERSIZE * 3:
                        i.active = 0
                        self.otherPlayer.oldY = self.otherPlayer.y + 10
class projectileTeleport(ability):
    def __init__(self, index):
        super().__init__("teleport projectile", (0, 60, 0), (0, 128, 0), index, 1100)
    def activate(self):
        direction = [0, 0]
        if self.player == p1:
            controls = p1Controls
        else:
            controls = p2Controls
        if controls["left"]:
            direction[0] -= 1
        if controls["right"]:
            direction[0] += 1
        if controls["jump"]:
            direction[1] -= 1
        if controls["slam"]:
            direction[1] += 1
        projectiles.append(teleportProjectile(self.player.x, self.player.y, self.player, math.atan2(direction[1], direction[0])))
class punch(ability):
    def __init__(self, index):
        super().__init__("punch", (192, 0, 0), (255, 0, 0), index, 80)
    def activate(self):
        if self.player == p1:
            otherPlayer = p2
        else:
            otherPlayer = p1
        dir = math.atan2(otherPlayer.y - self.player.y, otherPlayer.x - self.player.x)
        self.player.oldX -= math.cos(dir) * 6
        self.player.oldY -= math.sin(dir) * 5
        projectiles.append(fist(self.player.x, self.player.y, math.atan2(otherPlayer.y - self.player.y, otherPlayer.x - self.player.x), self.player))
    def update(self):
        if self.timer > 1:
            self.timer -= 1
        self.color1 = self.player.color
        self.color2 = (self.player.color[0]/2, self.player.color[1]/2, self.player.color[2]/2)
class smoke(ability):
    def __init__(self, index):
        super().__init__("smoke", (128, 128, 128), (100, 100, 100), index, 800)
    def activate(self):
        for i in range(50):
            particles.append(particle(self.player.x + random.randrange(-150, 150), self.player.y + random.randrange(-100, 100), random.uniform(-3,3), random.uniform(-1,1), "circle", [128, 128, 128, 255], random.randrange(40, 100), random.randrange(800, 1200), -0.05, fade=random.uniform(0.03, 0.01), drag=0.95))
class stickyBombAttack(ability):
    def __init__(self, index):
        super().__init__("sicky bomb", (0, 0, 0), (200, 0, 0), index, 1100)
        self.active = False
        self.storedBombs = []
    def activate(self):
        direction = [0, 0]
        if self.player == p1:
            controls = p1Controls
        else:
            controls = p2Controls
        if controls["left"]:
            direction[0] -= 1
        if controls["right"]:
            direction[0] += 1
        if controls["jump"]:
            direction[1] -= 1
        if controls["slam"]:
            direction[1] += 1
        if self.active == True:
            for i in self.storedBombs:
                i.explode()
            self.storedBombs = []
            self.active = False
        else:
            for i in range(3):
                newBomb = stickyBomb(self.player.x, self.player.y, math.atan2(direction[1], direction[0]) + random.uniform(-0.1, 0.1), self.player)
                self.storedBombs.append(newBomb)
                projectiles.append(newBomb)
            self.active = True
    def use(self):
        if self.timer <= 1:
            if self.active:
                self.timer = self.delay
            else:
                self.timer = 80
            self.activate()
    def draw(self):
        if self.player == p1:
            pygame.draw.rect(win,(70, 70, 70), (20 + (self.index * 50), height - 70, 50, 50), 4)
            pygame.draw.circle(win, self.color2, (20 + (self.index * 50) + 25, height - 70 + 25), 20)
            pygame.draw.circle(win, self.color1, (20 + (self.index * 50) + 25, height - 70 + 25), 15)
            if self.timer > 1:
                if self.active:
                    zi = self.timer / 80
                    pygame.draw.rect(win,(200, 200, 100), (20 + (self.index * 50), height - 70, 50, zi * 50))
                else:
                    zi = self.timer / self.delay
                    pygame.draw.rect(win,(200, 200, 200), (20 + (self.index * 50), height - 70, 50, zi * 50))
        else:
            pygame.draw.rect(win,(70, 70, 70), ((width - 70) - (self.index * 50), height - 70, 50, 50), 4)
            pygame.draw.circle(win, self.color2, ((width - 70) - (self.index * 50) + 25, height - 70 + 25), 20)
            pygame.draw.circle(win, self.color1, ((width - 70) - (self.index * 50) + 25, height - 70 + 25), 15)
            if self.timer > 1:
                if self.active:
                    zi = self.timer / 80
                    pygame.draw.rect(win,(200, 200, 100), ((width - 70) - (self.index * 50), height - 70, 50, zi * 50))
                else:
                    zi = self.timer / self.delay
                    pygame.draw.rect(win,(200, 200, 200), ((width - 70) - (self.index * 50), height - 70, 50, zi * 50))
class magicMissle(ability):
    def __init__(self, index):
        super().__init__("magic missle", (128, 0, 140), (180, 0, 180), index, 1200)
    def activate(self):
        if self.player == p1:
            angle = math.atan2(p2.y - self.player.y, p2.x - self.player.x)
        else:
            angle = math.atan2(p1.y - self.player.y, p1.x - self.player.x)
        projectiles.append(trackingSpell(self.player.x, self.player.y, angle, self.player))
class heatWave(ability):
    def __init__(self, index):
        super().__init__("heat wave", (200, 0, 0), (255, 96, 0), index, 1000)
    def activate(self):
        v = (math.pi / 180)
        projectiles.append(ember(self.player.x, self.player.y, self.player, 90 * v))
        projectiles.append(ember(self.player.x, self.player.y, self.player, -90 * v))
        projectiles.append(ember(self.player.x, self.player.y, self.player, 0 * v))
        projectiles.append(ember(self.player.x, self.player.y, self.player, 180 * v))
        projectiles.append(ember(self.player.x, self.player.y, self.player, 45 * v))
        projectiles.append(ember(self.player.x, self.player.y, self.player, -45 * v))
        projectiles.append(ember(self.player.x, self.player.y, self.player, 135 * v))
        projectiles.append(ember(self.player.x, self.player.y, self.player, -135 * v))
        particles.append(particle(self.player.x+(PLAYERSIZE/2), self.player.y+(PLAYERSIZE/2), 0, 0, "circle", [255, 96, 0, 255], 40, 80, 0.6, fade=3))
class molotov(ability):
    def __init__(self, index):
        super().__init__("molotov", (150, 75, 0), (100, 120, 180), index, 1900)
    def activate(self):
        direction = [0, 0]
        if self.player == p1:
            controls = p1Controls
        else:
            controls = p2Controls
        if controls["left"]:
            direction[0] -= 1
        if controls["right"]:
            direction[0] += 1
        if controls["jump"]:
            direction[1] -= 1
        if controls["slam"]:
            direction[1] += 1
        projectiles.append(molotovCocktail(self.player.x, self.player.y, math.atan2(direction[1], direction[0]), self.player))
class zap(ability):
    def __init__(self, index):
        super().__init__("zap", (64, 64, 255), (255, 255, 0), index, 2600)
        self.zapTimer = False
        self.active = False
    def activate(self):
        if self.active:
            self.zapTimer = 600
            self.active = False
            self.myDiode.active = True
        else:
            self.myDiode = diode(self.player.x, self.player.y, 0, self.player)
            projectiles.append(self.myDiode)
            self.active = True
    def use(self):
        if self.timer <= 1:
            if self.active:
                self.timer = self.delay
            else:
                self.timer = 300
            self.activate()
    def draw(self):
        if self.player == p1:
            pygame.draw.rect(win,(70, 70, 70), (20 + (self.index * 50), height - 70, 50, 50), 4)
            pygame.draw.circle(win, self.color2, (20 + (self.index * 50) + 25, height - 70 + 25), 20)
            pygame.draw.circle(win, self.color1, (20 + (self.index * 50) + 25, height - 70 + 25), 15)
            if self.timer > 1:
                if self.active:
                    zi = self.timer / 300
                    pygame.draw.rect(win,(200, 200, 100), (20 + (self.index * 50), height - 70, 50, zi * 50))
                else:
                    zi = self.timer / self.delay
                    pygame.draw.rect(win,(200, 200, 200), (20 + (self.index * 50), height - 70, 50, zi * 50))
        else:
            pygame.draw.rect(win,(70, 70, 70), ((width - 70) - (self.index * 50), height - 70, 50, 50), 4)
            pygame.draw.circle(win, self.color2, ((width - 70) - (self.index * 50) + 25, height - 70 + 25), 20)
            pygame.draw.circle(win, self.color1, ((width - 70) - (self.index * 50) + 25, height - 70 + 25), 15)
            if self.timer > 1:
                if self.active:
                    zi = self.timer / 300
                    pygame.draw.rect(win,(200, 200, 100), ((width - 70) - (self.index * 50), height - 70, 50, zi * 50))
                else:
                    zi = self.timer / self.delay
                    pygame.draw.rect(win,(200, 200, 200), ((width - 70) - (self.index * 50), height - 70, 50, zi * 50))
    def update(self):
        global screenShake
        if self.zapTimer > 1:
            x = self.player.x + (PLAYERSIZE/2)
            y = self.player.y + (PLAYERSIZE/2)
            a = math.atan2(self.myDiode.y - y, self.myDiode.x - x)
            while math.dist((self.myDiode.x, self.myDiode.y), (x, y)) > 10:
                a += random.uniform(-0.3, 0.3)
                pygame.draw.line(win,(0, 255, 255), (x-camX, y-camY), (x + (math.cos(a) * 10)-camX, y + (math.sin(a) * 10)-camY), random.randrange(1,4))
                x += math.cos(a) * 10
                y += math.sin(a) * 10
                if self.player == p1:
                    if math.dist((p2.x, p2.y), (x, y)) < 10:
                        p2.damage(0.3)
                        pygame.draw.line(win,(0, 255, 255), (x-camX, y-camY), (p2.x-camX, p2.y-camY), random.randrange(1,4))
                else:
                    if math.dist((p1.x, p1.y), (x, y)) < 10:
                        p1.damage(0.3)
                        pygame.draw.line(win,(0, 255, 255), (x-camX, y-camY), (p1.x-camX, p1.y-camY), random.randrange(1,4))
                a = math.atan2(self.myDiode.y - y, self.myDiode.x - x)
                screenShake = 5
            pygame.draw.line(win,(00, 255, 255), (x-camX, y-camY), (self.myDiode.x-camX, self.myDiode.y-camY), random.randrange(1,4))
            self.zapTimer -= 1
        if self.timer > 1:
            self.timer -= 1
class rockets(ability):
    def __init__(self, index):
        super().__init__("rockets", (200,200,0), (200,0,0), index, 800)
        self.abilityTimer = 0
    def activate(self):
        self.abilityTimer = 300
    def update(self):
        if self.timer > 1:
            self.timer -= 1
        if self.abilityTimer > 1:
            if self.abilityTimer % 100 == 0:
                for i in range(2):
                    projectiles.append(missle(self.player.x, self.player.y, random.uniform(0, 360)*(math.pi/180), self.player))
            self.abilityTimer -= 1
class groundPound(ability):
    def __init__(self, index):
        super().__init__("ground pound", (255, 128, 196), (255, 0, 255), index, 600)
        self.active = 0
        self.otherPlayer = None
    def update(self):
        global screenShake
        if self.timer > 1:
            self.timer -= 1
        if self.active > 0:
            self.active -= 1
            if math.dist((self.player.x, self.player.y), (self.otherPlayer.x, self.otherPlayer.y)) < PLAYERSIZE:
                self.otherPlayer.damage(20)
                self.player.oldY = self.player.y + 20
                self.otherPlayer.oldY = self.otherPlayer.y + 10
                self.otherPlayer.oldX += random.uniform(-20, 20)
                screenShake += 30
                self.active = 0
                self.timer = 10
        
    def activate(self):
        if self.player == p1:
            self.otherPlayer = p2
        else:
            self.otherPlayer = p1
        
        self.player.oldY = self.player.y - 20
        if self.otherPlayer.y > self.player.y + 15:
            self.active = 30


abilitys = [dash,fireball,parry,punch,smoke,stickyBombAttack,magicMissle,heatWave,molotov,zap,rockets]
attackAbilitys = [fireball,punch,stickyBombAttack,magicMissle,heatWave,molotov,zap,rockets]
default = player(width/2*1.5, height/2*1.5, (255, 0, 0), 100, 1, 0.8, 0.7, 8, 0.8, 1, [random.choice(abilitys)(0),random.choice(abilitys)(1),random.choice(abilitys)(2)])
default2 = player(width/2*1.5, height/2*1.5, (0, 0, 255), 100, 1, 0.8, 0.7, 8, 0.8, 1, [random.choice(abilitys)(0),random.choice(abilitys)(1),random.choice(abilitys)(2)])

def restart():
    global p1, p2
    p1 = player(width/2*1.5, height/2*1.5, (255, 0, 0), 100, 1, 0.8, 0.7, 8, 0.8, 1, [random.choice(attackAbilitys)(0),random.choice(abilitys)(1),random.choice(abilitys)(2)])
    p2 = player(width/2*1.5, height/2*1.5, (0, 0, 255), 100, 1, 0.8, 0.7, 8, 0.8, 1, [random.choice(attackAbilitys)(0),random.choice(abilitys)(1),random.choice(abilitys)(2)])

custom = player(width/2*1.5, height/2*1.5, (255, 0, 0), 100, 1, 0.8, 0.7, 8, 0.8, 1, [parry(0),parry(1),parry(2)])
custom2 = player(width/2*1.5, height/2*1.5, (0, 255, 0), 100, 1, 0.8, 0.7, 8, 0.8, 1, [parry(0),parry(1),magicMissle(2)])

p1 = default
p2 = default2

screenShake = 0
freezeFrame = 0
clock = pygame.time.Clock()
run = True
while run:
    if freezeFrame < 1:
        win.fill((0, 0, 60, 255))
        particleSurface.fill((0, 0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        p1Controls = {"left" : keys[pygame.K_a], "right" : keys[pygame.K_d], "jump" : keys[pygame.K_w], "slam" : keys[pygame.K_s],
                    "a1" : keys[pygame.K_1], "a2" : keys[pygame.K_2], "a3" : keys[pygame.K_3]}
        if p1.dead == False:
            p1.update(p1Controls)

        p2Controls = {"left" : keys[pygame.K_LEFT], "right" : keys[pygame.K_RIGHT], "jump" : keys[pygame.K_UP], "slam" : keys[pygame.K_DOWN],
                    "a3" : keys[pygame.K_COMMA], "a1" : keys[pygame.K_SLASH], "a2" : keys[pygame.K_PERIOD]}
        if p2.dead == False:
            p2.update(p2Controls)
        if (p1.dead or p2.dead) and keys[pygame.K_r]:
            restart()
        p1.draw()
        p2.draw()
        for p in particles:
            p.update()
            p.draw()
        for wall in walls:
            pygame.draw.rect(win, (100, 100 ,100), (wall[0] - camX, wall[1] - camY, wall[2], wall[3]))
        for item in projectiles:
            item.update()
            item.draw()
        p1.drawUI()
        p2.drawUI()
        win.blit(particleSurface, (0, 0))
        camX += random.uniform(-screenShake, screenShake)
        camY += random.uniform(-screenShake, screenShake)
        screenShake *= 0.9
        camX += ((((p1.x + p2.x) / 2) - (width/2)) - camX) / 15
        camY += ((((p1.y + p2.y) / 2) - (height/2)) - camY) / 15

        screen_shader.render_direct(pygame.Rect(0, 0, width, height))
        pygame.display.flip()
    else:
        freezeFrame -= 1
    clock.tick(60)
pygame.quit()