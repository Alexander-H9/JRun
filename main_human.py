# https://www.youtube.com/watch?v=PjgLeP0G5Yw
import pygame
from pygame.locals import *
import random

from model import Player, Laiserwall, Obstacle2, Coin
from view import redrawWindow, endScreen, get_bg_width

def main_loop():

    pygame.init()

    clock = pygame.time.Clock()

    runner = Player(200, 755, 64, 64)

    run = True
    speed = 30
    objects = []
    bg_speed = 3.4
    bg_width = get_bg_width()
    bgX = 0
    bgX2 = get_bg_width()

    # fix timer update speed in the loop
    pygame.time.set_timer(USEREVENT + 2, random.randrange(1000//(0.15*bg_speed), 2000//(0.15*bg_speed))) # das USEREVENT 2 wird alle 2 bis 4 sekunden ausgelößt
    pygame.time.set_timer(USEREVENT + 1, 3000)

    while run:

        for objectt in objects:
            
            # catch a coin
            if type(objectt) == Coin and objectt.collide(runner.hitbox) == True:
                runner.score += 1
                objects.pop(objects.index(objectt))
            
            # collide with a abstacle
            elif objectt.collide(runner.hitbox):
                print("Collide!")
                run = endScreen(runner)


            objectt.x -= bg_speed
            if objectt.x < -objectt.width * -1:
                objects.pop(objects.index(objectt))
                runner.score += 1

        bgX -= bg_speed
        bgX2 -= bg_speed

        if bgX < bg_width * -1:
            bgX = bg_width

        if bgX2 < bg_width * -1:
            bgX2 = bg_width

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                if runner.y > 134:
                    runner.jeting = True

            if not keys[pygame.K_SPACE]:
                if runner.y < 755:
                    runner.jeting = False

            # fügt zufällig object(1) oder object(2) hinzu
            if event.type == USEREVENT + 2:
                r = random.randrange(0, 2)
                if r == 0:
                    objects.append(Laiserwall(810, 760, 64, 64))    # x,y,width,hight
                elif r == 1:
                    objects.append(Obstacle2(810, 135, 48, 320))

                bg_speed += 0.1
                speed += 0.1

            if event.type == USEREVENT + 1:
                objects.append(Coin(810, random.randrange(135, 760), 44, 44))

        clock.tick(speed)
        redrawWindow([runner], objects, bgX, bgX2)

    return runner.score


if __name__ == "__main__":
    main_loop()