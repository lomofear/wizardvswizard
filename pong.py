import pygame
 
# initialize game engine
pygame.init()
# set screen width/height and caption
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Wizard VS Wizard')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()
 
# Loop until the user clicks close button
done = False
FPS = 30
VEL = 3.0 / float(FPS)
x = 0
y = 0
dx, dy = 1,1
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                done = True
        #if event.type == pygame.KEYDOWN:
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
    
    # clear the screen before drawing
    screen.fill((0, 0, 0)) 
    # write draw code here
    pygame.draw.circle(screen, (255,255,255), (int(x),int(y)) , 5)

    # display whats drawn. this might change.
    pygame.display.update()
    # run at 30 fps
    clock.tick(FPS)
 
# close the window and quit
pygame.quit()
