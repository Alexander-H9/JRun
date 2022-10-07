import pygame
from pygame.locals import *
import os
from model import Coin

W, H = 800, 1000
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('JRun')

bg = pygame.image.load(os.path.join('images', 'bg1.jpg')).convert()
#bg2 = pygame.image.load(os.path.join('images', 'bg2.jpg')).convert()
# bgX = 0
# bgX2 = bg.get_width()


def get_bg_width():
    return bg.get_width()


def endScreen(runner):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                return False

        largeFont = pygame.font.SysFont('comicsans', 80)
        endScore = largeFont.render('Score: ' + str(runner.score), 1, (255,255,255))
        win.blit(endScore, (W/2 - endScore.get_width()/2, 200))
        pygame.display.update()



def redrawWindow(runners, objects, bgX, bgX2):

    win.blit(bg, (bgX, 0))  # draws our first bg image
    win.blit(bg, (bgX2, 0))  # draws the second bg image
    # draws the random objects
    for x in objects:
        x.draw(win)
    
    # draw the runners
    for ru in runners:
        ru.draw(win)
        # line between player and obstacle
        pygame.draw.line(win, (255,0,0), (ru.x+50, ru.y), ru.obstacle_distance(objects), width=2)

        for obj in objects:
            if type(obj) == Coin:
                if obj.x > ru.x:
                    pygame.draw.line(win, (0,255,0), (ru.x+50, ru.y), (obj.x, obj.y), width=2)
                    break


    # draw score 
    if runners:
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render("Score: " + str(runners[0].score), 1, (255,255,255))
        win.blit(text, (650, 10))

    # updates the screen
    pygame.display.update()  