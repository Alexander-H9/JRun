# https://neat-python.readthedocs.io/en/latest/

import pygame
from pygame.locals import *
import random
import os
import neat

from model import Player, Laiserwall, Obstacle2, Coin
from view import redrawWindow, endScreen, get_bg_width

def main_loop(genomes, config):

    pygame.init()

    nets = []
    ge = []
    runners = []

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        runners.append(Player(200, 755, 64, 64))
        genome.fitness = 0
        ge.append(genome)

    clock = pygame.time.Clock()

    run = True
    speed = 30
    objects = []
    bg_speed = 8.4
    bg_width = get_bg_width()
    bgX = 0
    bgX2 = get_bg_width()

    # fix timer update speed in the loop
    pygame.time.set_timer(USEREVENT + 2, random.randrange(1000//(0.15*bg_speed), 2000//(0.15*bg_speed))) # das USEREVENT 2 wird alle 2 bis 4 sekunden ausgelößt
    pygame.time.set_timer(USEREVENT + 1, 3000)

    while run and len(runners) > 0:

        # object controller
        for objectt in objects:

            # collision detection
            for x,ru in enumerate(runners):
                if objectt.collide(ru.hitbox) and type(objectt) != Coin:
                    ge[x].fitness -= 5
                    runners.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    if len(runners) == 0: break

                # scoring a coin
                elif type(objectt) == Coin and objectt.collide(ru.hitbox) == True:
                    ge[x].fitness += 2
                    runners[0].score += 0.5
                    # objects.pop(objects.index(objectt))

            # scoring after passing a object
            objectt.x -= bg_speed
            if objectt.x < -objectt.width * -1:
                objects.pop(objects.index(objectt))
                if type(objectt) != Coin:
                    runners[0].score += 1
                    for g in ge:
                        g.fitness += 1

        # background shifting
        bgX -= bg_speed
        bgX2 -= bg_speed

        if bgX < bg_width * -1:
            bgX = bg_width

        if bgX2 < bg_width * -1:
            bgX2 = bg_width


        # spawn events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            # fügt zufällig object(1) oder object(2) hinzu
            if event.type == USEREVENT + 2:
                r = random.randrange(0, 2)
                if r == 0:
                    objects.append(Laiserwall(810, 760, 64, 64))    # x,y,width,hight
                elif r == 1:
                    objects.append(Obstacle2(810, 135, 48, 320))

            # spawns a coin
            if event.type == USEREVENT + 1:
                objects.append(Coin(810, random.randrange(135, 760), 44, 44))

                bg_speed += 0.1
                speed += 0.1

        # runner/player actions
        for x, ru in enumerate(runners):
            ge[x].fitness += 0.03

            if len(objects) > 0:
                obs_x, obs_y = ru.obstacle_distance(objects)
                coin_x, coin_y = ru.coin_distance(objects)
                output = nets[x].activate((ru.y, abs(ru.y - obs_y), abs(ru.x - obs_x), abs(ru.y - coin_y), abs(ru.x - coin_x)))

                if output[0] > 0.5:
                    ru.jeting = True
                else:
                    ru.jeting = False


        clock.tick(speed)
        redrawWindow(runners, objects, bgX, bgX2)




def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main_loop ,50)


if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

    # TODO:
    # move down obstacle2 to improve difficulty
    # add jetpack limit
    # add third obstacle
    # add coins for extra score 