import pygame
import cProfile
import math
import random

pygame.init()

width, height = 1200, 600
lowWidth = round(1200 / 2)
lowHeight = round(600 / 2)

surf = pygame.Surface((lowWidth, lowHeight))
screen = pygame.PixelArray(surf)
win = pygame.display.set_mode((width, height))


class vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"vec2({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x + other.x, self.y + other.y)
        return vec2(self.x + other, self.y + other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x - other.x, self.y - other.y)
        return vec2(self.x - other, self.y - other)

    def __rsub__(self, other):
        return vec2(other - self.x, other - self.y)

    def __mul__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x * other.x, self.y * other.y)
        return vec2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x / other.x, self.y / other.y)
        return vec2(self.x / other, self.y / other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.sqrt(self.dot(self))

    def normalized(self):
        length = self.length()
        if length == 0:
            return vec2(0, 0)
        return self / length


class vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        return vec3(self.x + other, self.y + other, self.z + other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        return vec3(self.x - other, self.y - other, self.z - other)

    def __rsub__(self, other):
        return vec3(other - self.x, other - self.y, other - self.z)

    def __mul__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        return vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        return vec3(self.x / other, self.y / other, self.z / other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self):
        return math.sqrt(self.dot(self))

    def normalized(self):
        length = self.length()
        if length == 0:
            return vec3(0, 0, 0)
        return self / length

def sampleHemisphere(nx, ny, nz):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-1, 1)

    l = x*x + y*y + z*z
    if l == 0:
        return nx, ny, nz

    inv = 1.0 / math.sqrt(l)
    x *= inv; y *= inv; z *= inv

    if x*nx + y*ny + z*nz < 0:
        x = -x; y = -y; z = -z

    return x, y, z


class ray:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
    def positionAt(self, t):
        return self.pos + self.dir * t
    def hitSphere(self, spherePos, radius):
        thisHitInfo = [False, 0, 0, 0]#didHit, distance, hitPos, normal
        originOffset = self.pos - spherePos

        a = 1
        b = 2 * originOffset.dot(self.dir)
        c = originOffset.dot(originOffset) - (radius * radius)

        discriminant = b * b - 4 * a * c
        if discriminant >= 0:
            dist = (-b - math.sqrt(discriminant)) / (2 * a)

            if dist >= 0:
                thisHitInfo[1] = dist
                thisHitInfo[0] = True
                thisHitInfo[2] = self.pos + self.dir * dist
                thisHitInfo[3] = (thisHitInfo[2] - spherePos).normalized()
        return thisHitInfo

class traceMaterial:
    def __init__(self, color, glow=0):
        self.color = color
        self.glow = glow
class sphere:
    def __init__(self, pos, radius, material):
        self.pos = pos
        self.radius = radius
        self.material = material

class camera:
    def __init__(self, x, y, z, FOV, yaw):
        self.x = x
        self.y = y
        self.z = z
        self.FOV = FOV
        self.yaw = yaw
        self.rays = []
        self.deadRays = []#0 -cast ray, 1 -dead ray, 2 -full strength light

        self.setupRays()
    def setupRays(self):
        self.rays = []
        for dy in range(lowHeight):
            for dx in range(lowWidth):
                pos = vec3(self.x, self.y, self.z - 3)
                dir = vec3(dx - (lowWidth/2), dy - (lowHeight/2), self.FOV*lowHeight).normalized()
                self.rays.append(ray(pos, dir))
                self.deadRays.append(False)
    def render(self):
        index = 0
        for r in self.rays:
            if self.deadRays[index]:
                index += 1
                continue
            i = ray(r.pos, r.dir)
            x = index % lowWidth
            y = math.floor(index / lowWidth)
            
            col = [1, 1, 1]
            brightness = 0
            for bounce in range(8):
                hit = []
                for s in spheres:
                    hitSphere = i.hitSphere(s.pos, s.radius)
                    if hitSphere[0]:
                        hit.append((s, hitSphere))
                if len(hit) > 0:
                    smallest = 9999999999999999999999999999999999999999999999999
                    current = None
                    for h in hit:
                        if h[1][1] < smallest:
                            smallest = h[1][1]
                            current = h
                    strength = abs(i.dir.dot(current[1][3]))
                    col[0] *= current[0].material.color[0]
                    col[1] *= current[0].material.color[1]
                    col[2] *= current[0].material.color[2]
                    glow = current[0].material.glow * strength
                    if glow > 0:
                        brightness += glow
                        break

                    i.pos = i.pos + i.dir * current[1][1]
                    hemisphere = sampleHemisphere(current[1][3].x,current[1][3].y,current[1][3].z)
                    i.dir = vec3(hemisphere[0], hemisphere[1], hemisphere[2])
                else:
                    if bounce == 0:
                        self.deadRays[index] = True
                    break
            if brightness > 0:
                newCol = (min(col[0] * brightness * 255,255) / raysPerPixel, min(col[1] * brightness * 255,255) / raysPerPixel, min(col[2] * brightness * 255,255) / raysPerPixel)
                """weight = 1 / (rIndex+1)
                if screen[x, y] != 0:
                    oldScreenCol = surf.unmap_rgb(screen[x, y])
                    average = ((oldScreenCol[0] * (1 - weight)) + (newCol[0] * weight), 
                                (oldScreenCol[1] * (1 - weight)) + (newCol[1] * weight), 
                                (oldScreenCol[2] * (1 - weight)) + (newCol[2] * weight))
                else:
                    oldScreenCol = (0, 0, 0)
                    average = newCol
                screen[x, y] = average"""
                screen[x, y] += surf.map_rgb(newCol)
            index += 1
        print("rendered!")
raysPerPixel = 10

spheres = [sphere(vec3(-2, 0, 5), 1, traceMaterial((0, 0, 1))), sphere(vec3(0, 0, 5), 1, traceMaterial((0, 1, 0))), sphere(vec3(0, 10, 5), 10, traceMaterial((0.8, 0.5, 0.2))), sphere(vec3(2, 0, 5), 1, traceMaterial((1, 0, 0))), sphere(vec3(0, -8, 20), 3, traceMaterial((1, 1, 1), 2))]
cam = camera(0, 0, 0, 1, 0)
run = True
frame = 0
rIndex = 0
while run:
    #surf.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in range(raysPerPixel):
        #cProfile.run("cam.render()")
        cam.render()
    rIndex += 1
    pygame.transform.scale(surf, win.get_size(), win)
    pygame.display.update()
    frame += 1
pygame.quit()