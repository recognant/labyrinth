import pygame
import sys
from actor import *
from world import *
from level import *
from const import *

SCREEN = None          

pygame.init()
SCREEN = pygame.display.set_mode( (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT) )#, pygame.FULLSCREEN )
pygame.display.set_caption('Labyrinth')

world = World()
world.create(Level("level1.txt"))

CLOCK = pygame.time.Clock()

actor_move_left = 0
actor_move_right = 0
actor_move_up = 0
actor_move_down = 0

camera_move_left = 0
camera_move_right = 0
camera_move_up = 0
camera_move_down = 0

world.start()

running = 1
while running:
    tick = CLOCK.tick(Constants.FPS)
    dt = 1.0 / tick
    
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                camera_move_left = -500
            if event.key == pygame.K_RIGHT:
                camera_move_right = 500
            if event.key == pygame.K_UP:
                camera_move_up = -500
            if event.key == pygame.K_DOWN:
                camera_move_down = 500
            if event.key == pygame.K_a:
                actor_move_left = 200
            if event.key == pygame.K_d:
                actor_move_right = -200
            if event.key == pygame.K_w:
                actor_move_up = 200
            if event.key == pygame.K_s:
                actor_move_down = -200

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                camera_move_left = 0
            if event.key == pygame.K_RIGHT:
                camera_move_right = 0
            if event.key == pygame.K_UP:
                camera_move_up = 0
            if event.key == pygame.K_DOWN:
                camera_move_down = 0
            if event.key == pygame.K_a:
                actor_move_left = 0
            if event.key == pygame.K_d:
                actor_move_right = 0
            if event.key == pygame.K_w:
                actor_move_up = 0
            if event.key == pygame.K_s:
                actor_move_down = 0

        if event.type == pygame.MOUSEBUTTONUP:
            mX, mY = pygame.mouse.get_pos()
            world.click(mX, mY)


    camera_move_x = int((camera_move_left + camera_move_right) * dt)
    camera_move_y = int((camera_move_up + camera_move_down) * dt)

    actor_move_x = int((actor_move_left + actor_move_right) * dt)
    actor_move_y = int((actor_move_up + actor_move_down) * dt)

##    if actor_move_x != 0 or actor_move_y != 0:
##        world.moveActor((actor_move_x, actor_move_y))

    if camera_move_x != 0 or camera_move_y != 0:
        world.getCamera().move((camera_move_x, camera_move_y))
    #world.getCamera().pan(world.player.screenPos())
    
    SCREEN.fill(Color.BLACK)

    world.update(dt)
    world.render(SCREEN)
    
    pygame.display.flip()

pygame.quit()
sys.exit()



