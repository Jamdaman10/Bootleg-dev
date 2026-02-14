import pygame
import random
import math

pygame.init()
width, height = 1200, 600
win = pygame.display.set_mode((width, height))
gravity = 0.51
bounce = 0.8
drag = 0.999
friction = 0.8

class point:
    def __init__(self, x, y, color, mass, visable=False):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.visable = visable
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
            self.yVel *= friction
        elif (self.x < 0):
            self.x = 0
            self.oldX = self.x + self.xVel * bounce
            self.yVel *= friction

        if (self.y > height):
            self.y = height
            self.oldY = self.y + self.yVel * bounce
            self.xVel *= friction
        elif (self.y < 0):
            self.y = 0
            self.oldY = self.y + self.yVel * bounce
            self.xVel *= friction
    def draw(self):
        if(self.visable):
            pygame.draw.circle(win,self.color, (self.x, self.y),3)

class pin(point):
    def __init__(self, x, y, color, visable=False):
        super().__init__(x, y, color, 9999999999999999, visable)
        self.x = x
        self.color = color
        self.visable = visable
    def frame(self):
        pass
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

class shape:
    def __init__(self, positions, mass, visable=True, color=(255,255,255)):
        self.positions = positions
        self.mass = mass
        self.visable = visable
        self.color = color
        self.myPoints = []
        self.myDistanceConstraints = []
        for i in range(len(self.positions)):
            self.myPoints.append(point(self.positions[i][0], self.positions[i][1], self.color, self.mass, False))
            if i != 0:
                dist = math.sqrt((self.myPoints[i].x - self.myPoints[i-1].x)**2 + (self.myPoints[i].y - self.myPoints[i-1].y)**2)
                self.myDistanceConstraints.append(distanceConstraint(self.myPoints[i], self.myPoints[i - 1], dist, self.color, self.visable))
        
        dist = math.sqrt((self.myPoints[i].x - self.myPoints[0].x)**2 + (self.myPoints[i].y - self.myPoints[0].y)**2)
        self.myDistanceConstraints.append(distanceConstraint(self.myPoints[i], self.myPoints[0], dist, self.color, self.visable))
        for thisPoint in self.myPoints:
            for connectedPoint in self.myPoints:
                if (thisPoint == connectedPoint):
                    pass
                else:
                    dist = math.sqrt((thisPoint.x - connectedPoint.x)**2 + (thisPoint.y - connectedPoint.y)**2)
                    self.myDistanceConstraints.append(distanceConstraint(thisPoint, connectedPoint, dist, self.color, False))
        
        for i in self.myPoints:
            points.append(i)
        for i in self.myDistanceConstraints:
            distanceConstraints.append(i)
    def draw(self):
        if self.visable:
            pygame.draw.polygon(win,self.color,self.positions)

class creature:
    def __init__(self, name, x, y, size, color):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.time = 0
        self.color = color

    def force(self, bodyPart, ammountX, ammountY):
        bodyPart.oldX -= ammountX
        bodyPart.oldY -= ammountY
    def frame(self):
        self.time += 1

class tenticle(creature):
    def __init__(self, x, y, size, color, target, length=20, weight=1, strength=1):
        super().__init__("tenticle", x, y, size, color)
        self.name = "tenticle"
        self.x = x
        self.y = y
        self.weight = weight
        self.length = length
        self.size = size
        self.color = color
        self.target = target
        self.strength = strength
        self.pointSections = []
        self.distanceSections = []

        self.head = point(self.x, self.y, color, self.weight, True)
        self.pointSections.append(self.head)
        for i in range(self.length):
            self.pointSections.append(point(self.x, self.y + i, self.color, self.weight, False))
            self.distanceSections.append(distanceConstraint(self.pointSections[i], self.pointSections[i-1], self.size, self.color, True))
        
        self.distanceSections.append(distanceConstraint(self.pointSections[i], self.pointSections[i+1], self.size, self.color, True))
        for i in self.pointSections:
            points.append(i)
        for i in self.distanceSections:
            distanceConstraints.append(i)
    
    def frame(self):
        if self.target == "mouse":
            angleToTarget = math.atan2(mousePos[1] - self.head.y, mousePos[0] - self.head.x)
        else:
            angleToTarget = math.atan2(self.target.y - self.head.y, self.target.x - self.head.x)
        self.force(self.head, math.cos(angleToTarget)*self.strength, math.sin(angleToTarget)*self.strength)

class fly:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.time = random.randrange(0, 30)

        self.head = point(self.x, self.y, color, 1, True)
        self.leftElbow = point(self.x - (10 * self.size), self.y, color, 1, True)
        self.rightElbow = point(self.x + (10 * self.size), self.y, color, 1, True)
        self.leftHand = point(self.x - (20 * self.size), self.y, color, 1, True)
        self.rightHand = point(self.x + (20 * self.size), self.y, color, 1, True)
        
        self.headToLeftElbow = distanceConstraint(self.head, self.leftElbow, (10 * self.size), color, True)
        self.headToRightElbow = distanceConstraint(self.head, self.rightElbow, (10 * self.size), color, True)
        self.leftElbowToHand = distanceConstraint(self.leftElbow, self.leftHand, (10 * self.size), color, True)
        self.rightElbowToHand = distanceConstraint(self.rightElbow, self.rightHand, (10 * self.size), color, True)
        points.append(self.head)
        points.append(self.leftElbow)
        points.append(self.rightElbow)
        points.append(self.leftHand)
        points.append(self.rightHand)
        distanceConstraints.append(self.headToLeftElbow)
        distanceConstraints.append(self.headToRightElbow)
        distanceConstraints.append(self.leftElbowToHand)
        distanceConstraints.append(self.rightElbowToHand)
    def force(self, bodyPart, ammountX, ammountY):
        bodyPart.oldX -= ammountX
        bodyPart.oldY -= ammountY

    def flapWings(self, frame, strength, xChange):
        if frame < 10:
            self.force(self.leftHand, -1 * strength, -1 * strength)
            self.force(self.rightHand, 1 * strength, -1 * strength)
        elif frame > 10 and frame < 12:
            self.force(self.head, xChange,-50 - ((self.head.y - self.head.oldY) * 2) * strength)

        else:
            if (self.size >= 1.4):
                self.force(self.leftHand, -1 * strength, 0)
                self.force(self.rightHand, 1 * strength, 0)
            else:
                pass

    def frame(self):
        self.time += 1
        if self.time >= 30:
            self.time = 0
        yMouseTarget = ((self.head.y - mousePos[1]) / 100) + 1
        xMouseTarget = (mousePos[0] - self.head.x) / 25
        normXChange = 0
        normFlapStrength = 1
        self.flapWings(self.time, yMouseTarget, xMouseTarget)
        
points = []
distanceConstraints = []
shapes = []
creatures = []

drawingColor = (255, 255, 255)
selectedItem = 1
drawingMass = 1
drawingSize = 1
curserClicked = False

selectedPointA = None
selectedPointB = None

closest = None
run = True
paused = False
while run:
    win.fill((0,0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if paused:
                    paused = False
                else:
                    paused = True
            if event.key == pygame.K_1:
                selectedItem = 1
                drawingLine = False
            elif event.key == pygame.K_2:
                selectedItem = 2
                drawingLine = False
            elif event.key == pygame.K_3:
                selectedItem = 3
                drawingLine = False

    mousePos = pygame.mouse.get_pos()
    mouseDown = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    
    for item in points:
        item.draw()
    for item in distanceConstraints:
        item.draw()
    for item in shapes:
        item.draw()
    if paused == False:
        if mouseDown[0]:
            if closest == None:
                smallest = 999999999
                for i in points:
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
        for item in creatures:
            item.frame()
        for i in range(5):
            for item in distanceConstraints:
                item.frame()
            for item in points:
                item.constrain()
        if keys[pygame.K_d]:
            points[0].x += 2
        if keys[pygame.K_a]:
            points[0].x -= 2
        if keys[pygame.K_w]:
            points[0].y -= 3
        if keys[pygame.K_s]:
            points[0].y += 0
    else:
        pygame.draw.rect(win,(30,30,50),(0, 0, width, 80))
        pygame.draw.circle(win,drawingColor,(40, 40), 3)
        if selectedItem == 1:
            pygame.draw.rect(win,(255, 255, 0),(10, 10, 60, 60), 3)
            pygame.draw.circle(win,drawingColor,mousePos, 3)
        pygame.draw.circle(win,drawingColor,(100, 60), 3)
        pygame.draw.circle(win,drawingColor,(140, 20), 3)
        pygame.draw.line(win,drawingColor,(100, 60),(140, 20),2)
        if selectedItem == 2:
            pygame.draw.rect(win,(255, 255, 0),(90, 10, 60, 60), 3)
        pygame.draw.circle(win,drawingColor,(200, 40), 3)
        pygame.draw.circle(win,drawingColor,(210, 35), 3)
        pygame.draw.circle(win,drawingColor,(190, 35), 3)
        pygame.draw.circle(win,drawingColor,(220, 25), 3)
        pygame.draw.circle(win,drawingColor,(180, 25), 3)

        pygame.draw.line(win,drawingColor,(200, 40),(210, 35),2)
        pygame.draw.line(win,drawingColor,(200, 40),(190, 35),2)
        pygame.draw.line(win,drawingColor,(220, 25),(210, 35),2)
        pygame.draw.line(win,drawingColor,(180, 25),(190, 35),2)
        if selectedItem == 3:
            pygame.draw.rect(win,(255, 255, 0),(170, 10, 60, 60), 3)
        
        if mouseDown[0]:
            if selectedItem == 1 and not curserClicked: #Point logic
                points.append(point(mousePos[0],mousePos[1],drawingColor,drawingMass,True))
                curserClicked = True
            
            elif selectedItem == 2 and not curserClicked: #Distance Constraints logic
                smallest = 999999999
                closest = None
                for i in points:
                    distance = math.sqrt((mousePos[0] - i.x)**2 + (mousePos[1] - i.y)**2)
                    if distance < smallest and distance < 5:
                        smallest = distance
                        closest = i

                if closest:
                    if selectedPointA is None:
                        selectedPointA = closest
                    elif selectedPointB is None and closest != selectedPointA:
                        selectedPointB = closest
                
                if selectedPointA and selectedPointB:
                    dist = math.sqrt((selectedPointA.x - selectedPointB.x)**2 + (selectedPointA.y - selectedPointB.y)**2)
                    new_constraint = distanceConstraint(selectedPointA, selectedPointB, dist, drawingColor, True)
                    distanceConstraints.append(new_constraint)
                    selectedPointA = None
                    selectedPointB = None
                curserClicked = True
            
            elif selectedItem == 3 and not curserClicked: #Fly logic
                creatures.append(fly(mousePos[0], mousePos[1], drawingSize, drawingColor))
                curserClicked = True
        else:
            curserClicked = False

        if selectedPointA:
            pygame.draw.circle(win, (0, 255, 0), (int(selectedPointA.x), int(selectedPointA.y)), 6, 2)
        if selectedPointB:
            pygame.draw.circle(win, (0, 255, 0), (int(selectedPointB.x), int(selectedPointB.y)), 6, 2)
    pygame.display.update()
    pygame.time.Clock().tick(60)
pygame.quit()