import pygame,math,random
from perlin_noise import PerlinNoise
noise = PerlinNoise(3,1)

WIDTH, HEIGHT = 1080,720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
W,H = 40,40
MAP = []
FOV = 120
for i in range(W):
    MAP.append([])
    for j in range(H):
        n = abs(noise.noise((i/W,j/H)))
        if n > 0.15:
            MAP[i].append(1)
        else:
            MAP[i].append(0)


i,j = random.randint(1,W-2),random.randint(1,H-2)

for I in range(3):
    for J in range(3):
        MAP[i-1+I][j-1+J] = 2

            
# Border
for i in range(W):
    MAP[i][0] = 1
    MAP[i][H-1] = 1
for j in range(H):
    MAP[0][j] = 1
    MAP[W-1][j] = 1



DTS = 4
TS = 15
def draw():
    for i in range(W):
        for j in range(H):
            if MAP[i][j] == 1:
                pygame.draw.rect(WIN,(255,255,0),(i*DTS,j*DTS,DTS,DTS))
            if MAP[i][j] == 2:
                pygame.draw.rect(WIN,(0,255,0),(i*DTS,j*DTS,DTS,DTS))
def sign(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


class Player:
    def __init__(self,x,y,speed,g,j,w,h):
        self.x = x
        self.y = y
        self.speed = speed
        self.g = g
        self.j = j
        self.w = w
        self.dj = True
        self.jump = False
        self.dir = 1
        self.h = h
        self.ground = False
    def draw(self,screen):
        pygame.draw.rect(screen,(255,0,0),(self.x,self.y,self.w,self.h))
    def update(self):
        # self.draw(WIN)
        self.fall()

    def Collide(self):
        X,Y,W,H = int(self.x//TS),int(self.y//TS),int((self.x+self.w)//TS),int((self.y+self.h)//TS)
        M = int((self.y+self.h/10*9)//TS)
        M2 = int((self.y+self.h/10)//TS)
        topleft = False
        topright = False
        bottomleft = False
        bottomright = False
        left = False
        right = False
        touch = False
        if MAP[X][Y] == 1:
            topleft = True	
            touch = True
        if MAP[W][Y] == 1:
            topright = True
            touch = True
        if MAP[X][H] == 1:
            bottomleft = True
            touch = True
        if MAP[W][H] == 1:
            bottomright = True
            touch = True
        if MAP[X][M] == 1 or MAP[X][M2] == 1:
            left = True
        if MAP[W][M] == 1 or MAP[W][M2] == 1:
            right = True
        
        return [topleft,topright,bottomleft,bottomright,touch,left,right]
    def fall(self):
        self.g += 1
        if self.g >= 0:
            for i in range(self.g):
                self.y += 1*sign(self.g)
                self.ground = False
                if self.Collide()[4]:
                    self.g = 0
                    self.y -= 1
                    self.ground = True
        else:
            for i in range(abs(self.g)):
                self.y -= 1
                self.ground = False
                if self.Collide()[4]:
                    self.g = 0
                    self.y += 1
                    self.ground = True




import time
prev = time.time()
dt = 0
FPS = 60
PL = Player(0,20,5,1,10,TS,TS)
Clock = pygame.time.Clock()
SPACE = False


def single_ray(x,y,angle):
    X,Y = x,y
    i = 0
    while not MAP[int(X//TS)][int(Y//TS)] == 1 and not i == 400:
        # move by angle
        X += math.cos(angle)
        Y += math.sin(angle)
        i += 1

    dist = math.sqrt((X-x)**2+(Y-y)**2)
    dist /= 4
    dist = int(dist)*4
    color = 1
    xx,yy = X//TS,Y//TS
    if yy%2 == 0:
        if xx%2 == 0:
            color = 0
        else:
            color = 1
    else:
        if xx%2 == 0:
            color = 1
        else:
            color = 0

    return [(X,Y),abs(dist),color]
    
def raycast(x,y,dir):
    
    rays = []
    colors = []
    for i in range(FOV):
        if dir == -1:

            rays.append(int(single_ray(x,y,(i-FOV//2-Offset)*math.pi/180)[1]))
            colors.append(single_ray(x,y,(i-FOV//2-Offset)*math.pi/180)[2])
        else:
            rays.append(int(single_ray(x,y,(i-FOV//2+Offset)*math.pi/180+math.pi)[1]))
            colors.append(single_ray(x,y,(i-FOV//2+Offset)*math.pi/180+math.pi)[2])
    return rays,colors

c = HEIGHT//FOV
Offset = 0
fo = 0
C = 2
while True: 


    Dist,Colors = raycast(PL.x+(PL.w/2),PL.y+(PL.h/2),PL.dir)

    # print((PL.dir*90))
    # Dist = []
    # D = (PL.dir*90)
    # for I in range(FOV):
        # single_ray(PL.x,PL.y,I)[1]
        # Dist.append(int(single_ray(PL.x,PL.y,I)[1]))
    # single_ray(PL.x,PL.y,0)[1]

    for i in range(FOV):
        if Colors[i] == 0:
            CLR = [150,100,0]
            clr = [CLR[0]-Dist[i]/C,CLR[1]-Dist[i]/C,0]
            if clr[0] < 0:
                clr[0] = 0
            if clr[1] < 0:
                clr[1] = 0
            if PL.dir == -1:

                pygame.draw.rect(WIN,(clr[0],clr[1],0),(0,i*c,WIDTH,c))
            else:
                pygame.draw.rect(WIN,(clr[0],clr[1],0),(0,HEIGHT-i*c,WIDTH,c))
        else:
            CLR = [100,50,0]
            clr = [CLR[0]-Dist[i]/C,CLR[1]-Dist[i]/C,0]
            if clr[0] < 0:
                clr[0] = 0
            if clr[1] < 0:
                clr[1] = 0
            if PL.dir == -1:
                    pygame.draw.rect(WIN,(clr[0],clr[1],0),(0,i*c,WIDTH,c))
            else:
                pygame.draw.rect(WIN,(clr[0],clr[1],0),(0,HEIGHT-i*c,WIDTH,c))


    pygame.draw.circle(WIN,(255,0,0),(int((PL.x+PL.w/2)/TS*DTS),int((PL.y+PL.h/2)/TS*DTS)),int(4/TS*DTS))


    KEYS = pygame.key.get_pressed()


    if PL.ground:
        PL.dj = 0


    if KEYS[pygame.K_SPACE]:

        if PL.ground or PL.dj < 3:
            if not SPACE:
                PL.jump = True
                PL.g = -12
                PL.dj += 1
        


            SPACE = True
    else:
        SPACE = False

    if KEYS[pygame.K_LEFT]:
        PL.dir = 1
        for i in range(PL.speed):
            PL.x -= 1
            if PL.Collide()[5]:
                PL.x += 1.1
                break

    if KEYS[pygame.K_RIGHT]:
        PL.dir = -1
        for i in range(PL.speed):
            PL.x += 1
            if PL.Collide()[6]:
                PL.x -= 1.1
                break


    if KEYS[pygame.K_UP]:
        fo += 3
    
    if KEYS[pygame.K_DOWN]:
        fo -= 3
    


    Offset = int(fo)

    Clock.tick(FPS)
    PL.update()

    now = time.time()
    dt = now - prev
    prev = now

    draw()

    MB = pygame.mouse.get_pressed()
    if MB[0]:
        PL.x = pygame.mouse.get_pos()[0]
        PL.y = pygame.mouse.get_pos()[1]
        PL.g = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()



    pygame.display.update()
    WIN.fill((30,30,30))