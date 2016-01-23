import pygame, os, random
import math, time

DY_GRAVEDAD = 50
SHOOT_VEL = 500

class GameObject(object):
    OBJECT_LIST = []
    # METODOS DE CLASE // CLASSMETHODS
    @classmethod
    def apply_logic_to_all(cls, frametime):
        for gameobject in cls.OBJECT_LIST:
            gameobject.logic(frametime)

    @classmethod
    def draw_all(cls, screen):
        for gameobject in cls.OBJECT_LIST:
            gameobject.draw(screen)
    
    # INSTANCIAS
    def __init__(self, new_time, x = 0, y = 0, dx = 0, dy = 0):
        self.time = new_time
        self.dtime = 0
        self.x = x
        self.y = y 
        self.dx = dx
        self.dy = dy
        self.OBJECT_LIST.append(self)

    def logic(self, new_time):
        # new_time: nuevo timestamp del frame
        self.dtime = new_time - self.time
        self.time = new_time

        self.x += self.dx * self.dtime
        self.y += self.dy * self.dtime
        
    def draw(self, screen):
        pygame.draw.circle(screen, (200,200,200), (int(self.x),int(self.y)) , 3)
        

class GameCircle(GameObject):
    pass

class GameShoot(GameCircle):
    SPRITE = pygame.image.load('resources/shoot.png')
    def __init__(self, *args, **kwargs):
        GameCircle.__init__(self,*args,**kwargs)
        self.life = 3
        
    def draw(self, screen):
        #pygame.draw.circle(screen, (100,200,255), (int(self.x),int(self.y)) , 2)
        screen.blit(self.SPRITE,(int(self.x-4),int(self.y-4)))
    def logic(self, new_time):
        GameCircle.logic(self,new_time)
        self.life -= self.dtime
        if self.life < 0:
            self.OBJECT_LIST.remove(self)
            
        for obj in self.OBJECT_LIST:
            if isinstance(obj, GameAsteroid):
                dx = self.x - obj.x
                dy = self.y - obj.y
                p_dist = math.hypot(dx, dy)
                if p_dist < 18:
                    obj.dx += self.dx / 10
                    obj.dy += self.dy / 10
                    self.dx = -self.dx / 2
                    self.dy = -self.dy / 2
                    self.life /= 2
                

class GamePlayer(GameCircle):
    SPRITE = pygame.image.load('resources/ball2.png')
    def draw(self, screen):
        #pygame.draw.circle(screen, (100,255,100), (int(self.x),int(self.y)) , 8)
        screen.blit(self.SPRITE,(int(self.x-12),int(self.y-12)))

    def logic(self, new_time):
        GameCircle.logic(self,new_time)
        self.dx /= 1.9 ** self.dtime
        self.dy /= 1.9 ** self.dtime
        self.dy += DY_GRAVEDAD * self.dtime
        if self.x > 800: self.x-=800
        if self.x < 0: self.x+=800
        if self.y > 600:
            if self.dy > 0: self.dy = -self.dy
            self.y = 600
        if self.y < 0: 
            if self.dy < 0: self.dy = -self.dy
            self.y = 0

                

        # super(GamePlayer, self).logic(new_time)

class GameAsteroid(GameCircle):
    SPRITE = pygame.image.load('resources/ball1.png')
    def draw(self, screen):
        #pygame.draw.circle(screen, (255,100,100), (int(self.x),int(self.y)) , 16)
        screen.blit(self.SPRITE,(int(self.x-16),int(self.y-16)))

    def logic(self, new_time):
        GameCircle.logic(self,new_time)
        self.dx /= 1.1 ** self.dtime
        self.dy /= 1.1 ** self.dtime
        self.dy += DY_GRAVEDAD * self.dtime
        if self.x > 800: self.x-=800
        if self.x < 0: self.x+=800
        if self.y > 600:
            if self.dy > 0: self.dy = -self.dy
            self.y = 600
        if self.y < 0: 
            if self.dy < 0: self.dy = -self.dy
            self.y = 0

        for obj in self.OBJECT_LIST:
            if obj is self: continue
            if isinstance(obj, GamePlayer) or isinstance(obj, GameAsteroid) :
                dx = self.x - obj.x
                dy = self.y - obj.y
                p_dist = math.hypot(dx, dy)
                if p_dist < 24:
                    f = 24 - p_dist
                    obj.dx -= dx / p_dist * f 
                    obj.dy -= dy / p_dist * f
                    self.dx += dx / p_dist * f
                    self.dy += dy / p_dist * f

        # super(GamePlayer, self).logic(new_time)

# initialize game engine
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (15,30)
 
pygame.init()
# set screen width/height and caption
size = [800, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Wizard VS Wizard')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()
frametime = time.time()
# Loop until the user clicks close button

done = False

MB_LEFT = 1

FPS = 60
VEL = 300.0 / float(FPS)

Player = GamePlayer(frametime, 200, 100, 0 ,0) 

for i in range(8):
    GameAsteroid(frametime, random.randint(0,800), random.randint(0,600), random.randint(-100,100),random.randint(-100,100)) 
last_shoot_time = time.time()
last_shoot_num = 0

while done == False:
    shoot = False
    frametime = time.time()

    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEMOTION:
            x2,y2 = event.pos

                
            print "mouse at (%d, %d)" % event.pos
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MB_LEFT:
            #print "You pressed the left mouse button at (%d, %d)" % event.pos
            shoot = True
        #if event.type == pygame.MOUSEBUTTONUP and event.button == MB_LEFT:
        #    print "You released the left mouse button at (%d, %d)" % event.pos        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_UP:    dy -= 1
        #    if event.key == pygame.K_DOWN:  dy += 1
        #    if event.key == pygame.K_LEFT:  dx -= 1
        #    if event.key == pygame.K_RIGHT: dx += 1
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        shoot = True    

    if keys[pygame.K_UP]:    Player.dy -= VEL
    if keys[pygame.K_DOWN]:  Player.dy += VEL
    if keys[pygame.K_LEFT]:  Player.dx -= VEL
    if keys[pygame.K_RIGHT]: Player.dx += VEL
    # write game logic here
    if shoot and frametime - last_shoot_time > 0.01 :
        p_dist = math.hypot(Player.dx, Player.dy)
        if p_dist > 0:
            angle = math.atan2(Player.dy,Player.dx)
            num_shots = 50
            max_angle = 10.0 / 180 *math.pi
            minshot = -(num_shots-1)/2
            #shoot_list = range(num_shots)
            shoot_list = [  random.randint(0,num_shots) for i in range(2)]
            last_shoot_num += 1
            last_shoot_num %= num_shots

            for n in shoot_list:
                sdx = math.cos(angle + (n+minshot)*max_angle/num_shots)* SHOOT_VEL
                sdy = math.sin(angle + (n+minshot)*max_angle/num_shots)* SHOOT_VEL

                #sdx = Player.dx / p_dist * SHOOT_VEL
                #sdy = Player.dy / p_dist * SHOOT_VEL

                sdx += Player.dx / 2.0 
                sdy += Player.dy / 2.0 
                last_shoot_time = time.time()
                Shoot = GameShoot(frametime, Player.x + sdx / 20.0, Player.y + sdy / 20.0, sdx, sdy) 

    GameObject.apply_logic_to_all(frametime)

    # clear the screen before drawing
    screen.fill((0, 0, 0)) 
    # write draw code here

    GameObject.draw_all(screen)
    
    # display whats drawn. this might change.
    pygame.display.update()
    # run at 30 fps
    clock.tick(FPS)
 
# close the window and quit
pygame.quit()
