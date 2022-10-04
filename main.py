# https://www.youtube.com/watch?v=PjgLeP0G5Yw
import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 1000
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('JRun')

bg = pygame.image.load(os.path.join('images', 'bg1.jpg')).convert()
#bg2 = pygame.image.load(os.path.join('images', 'bg2.jpg')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()


class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(5, 8)]  # früher 8 bis 16
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 5)]  # früher 1 bis 8
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -8, -4]

    # jumpList = [10, 12, 0, -12, -10, 0, 0]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.jumpCount = 0
        self.runCount = 0
        self.jeting = False
        self.falling = False

    def draw(self, win):
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 36], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount >= 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0

        if self.jeting:
            if self.y > 134:
                self.y -= 8
            win.blit(self.jump[1], (self.x, self.y))

        if not self.jeting:
            if runner.y < 755:
                runner.y += 8
                win.blit(self.jump[1], (self.x, self.y))
            else:
                if self.runCount >= 6:
                    self.runCount = 0
                win.blit(self.run[self.runCount // 2], (self.x, self.y))
                self.runCount += 1

        self.hitbox = (self.x + 11, self.y, self.width - 26, self.height)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

        

class laiserwall(object):
    img = [pygame.image.load(os.path.join('images', 'wall0.PNG')), pygame.image.load(os.path.join('images', 'wall1.PNG')),
           pygame.image.load(os.path.join('images', 'wall2.PNG')), pygame.image.load(os.path.join('images', 'wall3.PNG'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.count >= 8:
            self.count = 0
        # transform.scale scales the size of the image to 64, 64
        win.blit(pygame.transform.scale(self.img[self.count // 2], (64, 64)), (self.x, self.y))
        self.count += 1
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class obstacle2(laiserwall):
    img = pygame.image.load(os.path.join("images", "spike.png"))

    def draw(self, win):
        self.hitbox = (self.x + 0, self.y + 0, self.width, self.height+135)
        win.blit(self.img, (self.x, self.y))
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


def endScreen():

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                return False

        largeFont = pygame.font.SysFont('comicsans', 80)
        endScore = largeFont.render('Score: ' + str(score), 1, (255,255,255))
        win.blit(endScore, (W/2 - endScore.get_width()/2, 200))
        pygame.display.update()


def redrawWindow():

    win.blit(bg, (bgX, 0))  # draws our first bg image
    win.blit(bg, (bgX2, 0))  # draws the second bg image
    runner.draw(win)
    # draws the random objects
    for x in objects:
        x.draw(win)

    font = pygame.font.SysFont('comicsans', 30)
    text = font.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (650, 10))
    pygame.display.update()  # updates the screen



runner = player(200, 755, 64, 64)
pygame.time.set_timer(USEREVENT + 2, random.randrange(1000, 3000)) # das USEREVENT 2 wird alle 2 bis 4 sekunden ausgelößt
run = True
speed = 30
objects = []
bg_speed = 6.4
score = 0

while run:

    for object in objects:
        if object.collide(runner.hitbox):
            runner.falling = True
            print("Collide!")
            run = endScreen()

        object.x -= bg_speed
        if object.x < -object.width * -1:
            objects.pop(objects.index(object))
            score += 1

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
       bgX2 = bg.get_width()

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
                objects.append(laiserwall(810, 760, 64, 64))    # x,y,width,hight
            elif r == 1:
                objects.append(obstacle2(810, 135, 48, 320))
            #speed += 1
            bg_speed += 0.1

    clock.tick(speed)
    redrawWindow()

# return score