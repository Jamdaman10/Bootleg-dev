import pygame
import random
import math
pygame.init()

width, height = 1200, 600
win = pygame.display.set_mode((width, height))

gravity = 0.51
bounce = 0.8
drag = 0.999
friction = 3

def signed_angle_difference(a, b):
    return (b - a + math.pi) % (2 * math.pi) - math.pi

class point:
    def __init__(self, x, y, color, mass, visable=False, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.visable = visable
        self.size = size
        self.xVel = 0
        self.yVel = 0
        self.oldX = x
        self.oldY = y
    def frame(self):
        self.xVel = (self.x - self.oldX) * drag
        self.yVel = (self.y - self.oldY) * drag

        self.oldX = self.x
        self.oldY = self.y

        self.x += self.xVel
        self.y += self.yVel
        self.y += gravity * self.mass

    def constrain(self):
        self.xVel = (self.x - self.oldX) * drag
        self.yVel = (self.y - self.oldY) * drag

        if (self.x > width):
            self.x = width
            self.oldX = self.x + self.xVel * bounce
            self.oldY += self.yVel / friction
        elif (self.x < 0):
            self.x = 0
            self.oldX = self.x + self.xVel * bounce
            self.oldY += self.yVel / friction

        if (self.y > height):
            self.y = height
            self.oldY = self.y + self.yVel * bounce
            self.oldX += self.xVel / friction
        elif (self.y < 0):
            self.y = 0
            self.oldY = self.y + self.yVel * bounce
            self.oldX += self.xVel / friction
    def draw(self):
        if(self.visable):
            pygame.draw.circle(win,self.color, (self.x, self.y), self.size)
class distanceConstraint:
    def __init__(self, P1, P2, length, color=(255,255,255), visable=False):
        self.P1 = P1
        self.P2 = P2
        self.length = length
        self.color = color
        self.visable = visable

    def frame(self):
        dx = self.P2.x - self.P1.x
        dy = self.P2.y - self.P1.y
        distance = math.sqrt(dx*dx + dy*dy) + 0.0000001
        differance = self.length - distance

        percent = differance / distance / 2

        offsetX = percent * dx
        offsetY = percent * dy
        #calculate mass
        total_mass = self.P1.mass + self.P2.mass
        ratio1 = self.P2.mass / total_mass
        ratio2 = self.P1.mass / total_mass

        self.P1.x -= offsetX * ratio1
        self.P1.y -= offsetY * ratio1
        self.P2.x += offsetX * ratio2
        self.P2.y += offsetY * ratio2

    def draw(self):
        if (self.visable):
            pygame.draw.line(win,self.color, (self.P1.x, self.P1.y), (self.P2.x, self.P2.y),2)

class player:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.head = point(x, y - (10 * size), self.color, 1, True, 6)
        self.neck = point(x, y - (8 * size), self.color, 1, True, 3)
        self.crotch = point(x, y - (-6 * size), self.color, 1, True, 3)

        self.leftElbow = point(x - (5 * self.size), y - (8 * size), self.color, 0.5, True, 3)
        self.rightElbow = point(x + (5 * self.size), y - (8 * size), self.color, 0.5, True, 3)
        self.leftHand = point(x - (10 * self.size), y - (8 * size), (255,0,0), 0.5, True, 3)
        self.rightHand = point(x + (10 * self.size), y - (8 * size), (255,0,0), 0.5, True, 3)

        self.leftKnee = point(x - (5 * size), y - (-11 * size), self.color, 1, True, 3)
        self.rightKnee = point(x + (5 * size), y - (-11 * size), self.color, 1, True, 3)
        self.leftFoot = point(x - (10 * size), y - (-16 * size), self.color, 1.5, True, 3)
        self.rightFoot = point(x + (10 * size), y - (-16 * size), self.color, 1.5, True, 3)

        self.neckJoint = distanceConstraint(self.head, self.neck, 5 * self.size, self.color, True)
        self.spine = distanceConstraint(self.neck, self.crotch, 5 * self.size, self.color, True)

        self.leftBicep = distanceConstraint(self.neck, self.leftElbow, 5 * self.size, self.color, True)
        self.rightBicep = distanceConstraint(self.neck, self.rightElbow, 5 * self.size, self.color, True)
        self.leftForarm = distanceConstraint(self.leftElbow, self.leftHand, 5 * self.size, self.color, True)
        self.rightForarm = distanceConstraint(self.rightElbow, self.rightHand, 5 * self.size, self.color, True)

        self.leftThigh = distanceConstraint(self.crotch, self.leftKnee, 5 * self.size, self.color, True)
        self.rightThigh = distanceConstraint(self.crotch, self.rightKnee, 5 * self.size, self.color, True)
        self.leftShin = distanceConstraint(self.leftKnee, self.leftFoot, 5 * self.size, self.color, True)
        self.rightShin = distanceConstraint(self.rightKnee, self.rightFoot, 5 * self.size, self.color, True)

        self.points = []
        self.distanceConstraints = []
        self.points.append(self.head)
        self.points.append(self.neck)
        self.points.append(self.crotch)
        self.points.append(self.leftElbow)
        self.points.append(self.rightElbow)
        self.points.append(self.leftHand)
        self.points.append(self.rightHand)
        self.points.append(self.leftKnee)
        self.points.append(self.rightKnee)
        self.points.append(self.leftFoot)
        self.points.append(self.rightFoot)

        self.distanceConstraints.append(self.neckJoint)
        self.distanceConstraints.append(self.spine)
        self.distanceConstraints.append(self.leftBicep)
        self.distanceConstraints.append(self.rightBicep)
        self.distanceConstraints.append(self.leftForarm)
        self.distanceConstraints.append(self.rightForarm)
        self.distanceConstraints.append(self.leftThigh)
        self.distanceConstraints.append(self.rightThigh)
        self.distanceConstraints.append(self.leftShin)
        self.distanceConstraints.append(self.rightShin)
        self.walkCycle = 0
    def update(self, controls):
        if abs(((self.leftFoot.y + self.rightFoot.y)/2) - self.head.y) < 20*self.size:
            self.head.y -= 2
        if abs(self.crotch.y - ((self.leftFoot.y + self.rightFoot.y)/2)) < 10*self.size:
            self.crotch.y -= 2
        if abs(self.leftKnee.x - self.rightKnee.x) < 4*self.size:
            self.leftKnee.x -= 0.2
            self.rightKnee.x += 0.2
        
        keys = pygame.key.get_pressed()
        if keys[controls["right"]]:
            self.walkCycle += 1
        elif keys[controls["left"]]:
            self.walkCycle -= 1
        else:
            self.walkCycle = 0
        if (keys[controls["right"]] or keys[controls["left"]]):
            if math.sin(self.walkCycle/5) > 0:
                angle = math.sin(self.walkCycle/5) * (math.pi)
                self.leftFoot.x += abs(math.cos(self.walkCycle / 5)) * math.copysign(1,self.walkCycle)
                self.leftFoot.y -= abs(math.sin(self.walkCycle / 5)) * math.copysign(1,self.walkCycle) / 2
            else:
                angle = math.sin(self.walkCycle/5) * (math.pi)
                self.rightFoot.x += abs(math.cos(self.walkCycle / 5)) * math.copysign(1,self.walkCycle)
                self.rightFoot.y += abs(math.sin(self.walkCycle / 5)) * math.copysign(1,self.walkCycle) / 2

    def draw(self):
        for i in self.points:
            i.draw()
        for i in self.distanceConstraints:
            i.draw()
    def updateParts(self):
        for item in self.points:
            item.frame()
        for i in range(5):
            for item in self.distanceConstraints:
                item.frame()
            for item in self.points:
                item.constrain()
points = []
distanceConstraints = []

p = player(width/2, height/2, 3, (255, 0, 128))
p2 = player(width/2, height/2, 3, (128, 0, 255))

points.append(point(0, 0, (0, 0, 0), 0.1, False, 3))
points.append(point(0, 0, (0, 0, 0), 0.1, False, 3))
points.append(point(0, 0, (0, 0, 0), 0.1, False, 3))
points.append(point(0, 0, (0, 0, 0), 0.1, False, 3))

distanceConstraints.append(distanceConstraint(p.crotch, points[-1], 20, visable=True))
distanceConstraints.append(distanceConstraint(points[-1], points[-2], 20, visable=True))
distanceConstraints.append(distanceConstraint(points[-2], points[-3], 20, visable=True))
distanceConstraints.append(distanceConstraint(points[-3], points[-4], 20, visable=True))
distanceConstraints.append(distanceConstraint(points[-4], points[-0], 20, visable=True))
distanceConstraints.append(distanceConstraint(points[-0], p2.crotch, 20, visable=True))

closest = None
clock = pygame.time.Clock()
run = True
while run:
    win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    mouseDown = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    if mouseDown[0]:
        if closest == None:
            smallest = 999999999
            for i in p.points:
                distance = math.sqrt((mousePos[0] - i.x)**2 + (mousePos[1] - i.y)**2)
                if distance < smallest and distance < 30:
                    smallest = distance
                    closest = i
        if closest != None:
            closest.x = mousePos[0]
            closest.y = mousePos[1]
    else:
        closest = None
    
    for item in points:
        item.frame()
    for i in range(5):
        for item in distanceConstraints:
            item.frame()
        for item in points:
            item.constrain()
    p.update({"left" : pygame.K_a, "right" : pygame.K_d})
    p.updateParts()

    p2.update({"left" : pygame.K_LEFT, "right" : pygame.K_RIGHT})
    p2.updateParts()
    for i in points:
        i.draw()
    for i in distanceConstraints:
        i.draw()
    p.draw()
    p2.draw()
    pygame.display.update()
    clock.tick(60)
pygame.quit()