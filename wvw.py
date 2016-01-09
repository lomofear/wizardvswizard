import pygame
import math

# initialize game engine
pygame.init()
# set screen width/height and caption
size = [800, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Wizard VS Wizard')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()
 
# Loop until the user clicks close button

done = False

MB_LEFT = 1

FPS = 30
VEL = 3.0 / float(FPS)
x = 0
y = 0
dx, dy = 1,1
x2,y2 = -50, -50

while done == False:
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
            print "You pressed the left mouse button at (%d, %d)" % event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == MB_LEFT:
            print "You released the left mouse button at (%d, %d)" % event.pos        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_UP:    dy -= 1
        #    if event.key == pygame.K_DOWN:  dy += 1
        #    if event.key == pygame.K_LEFT:  dx -= 1
        #    if event.key == pygame.K_RIGHT: dx += 1
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:    dy -= VEL
    if keys[pygame.K_DOWN]:  dy += VEL
    if keys[pygame.K_LEFT]:  dx -= VEL
    if keys[pygame.K_RIGHT]: dx += VEL
    # write game logic here
    x += dx
    y += dy
    if x > size[0] and dx > 0: dx = -dx
    if y > size[1] and dy > 0:
        dy = -dy
    if x < 0 and dx < 0: dx = -dx
    if y < 0 and dy < 0: dy = -dy
    dx /= 1.01
    dy /= 1.01
    dy += 0.06

    dx2, dy2 = x-x2, y-y2
    dist = math.hypot(dx2,dy2)
    if dist < 50:
        dx2n, dy2n =  dx2 / dist, dy2 / dist
        dist1 = max([1,dist])
        fx, fy = dx2n / dist1, dy2n / dist1
        fx *= 3.0
        fy *= 3.0
        dx += fx
        dy += fy

                        
    # clear the screen before drawing
    screen.fill((0, 0, 0)) 
    # write draw code here
    pygame.draw.circle(screen, (0,255,0), (int(x),int(y)) , 9)
    pygame.draw.circle(screen, (200,200,200), (int(x),int(y)) , 7)

    # display whats drawn. this might change.
    pygame.display.update()
    # run at 30 fps
    clock.tick(FPS)
 
# close the window and quit
pygame.quit()
