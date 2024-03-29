import pygame
import os
import math
import copy
from game_classes import GameObject, Obstacle


class Player(GameObject):

    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(5, 8)]  # früher 8 bis 16
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 5)]  # früher 1 bis 8
    score = 0

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.runCount = 0
        self.jeting = False
        self.jet_lock = False
        self.speed = 10
        self.jetpack_volume = 100.0

        # payer specific ui-elements
        self.jet_bar_bg = Bar(20, 960, 123, 23, (255,255,255))
        self.jet_bar_volume = Bar(21, 961, 121, 21, (50,130,246))


    def draw(self, win):

        # player trys jetting
        if self.jeting:
            # are the jetting conditions true
            if self.y > 134 and self.jetpack_volume > 0 and self.jet_lock == False:
                self.y -= self.speed
                self.jetpack_volume -= 1

                # disable the jatpack if the tank is empty
                if self.jetpack_volume <= 0: self.jet_lock = True

                win.blit(self.jump[1], (self.x, self.y))
                
            # lock the jatpack
            else: self.jeting = False
            

        # falling
        if not self.jeting:
            if self.y < 755:
                self.y += self.speed
                win.blit(self.jump[1], (self.x, self.y))

            # walking
            else:
                if self.runCount >= 6: self.runCount = 0
                if self.jetpack_volume < 100: self.jetpack_volume += 1
                self.jet_lock = False
                win.blit(self.run[self.runCount // 2], (self.x, self.y))
                self.runCount += 1

        self.hitbox = (self.x + 11, self.y, self.width - 26, self.height)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

        # payer specific ui-elements
        self.jet_bar_bg.draw(win)
        self.jet_bar_volume.draw(win, self.jetpack_volume)


    def obstacle_distance(self, objects, d=False):
        """
        Return the x and y pos of the closest obstacle (x,y). If there are no obstacles the player pos will be returned.
        If d is true, the player pos, the distance between player and obstacle pos will join the return statement (player.x, player.y dis, obs.x, obs.y).
        """

        # print(f'All objects: \n {objects}')

        for obj in objects:
            if obj.x < self.x or type(obj) == Coin:
                continue
            else:
                objectt = copy.copy(obj)
                if type(objectt) == Obstacle2:  # move the measurment point to the tip of the obstacle
                    objectt.y += 317        

                dist = math.hypot(self.x+50 - objectt.x, self.y - objectt.y)

                # print(f'Distance: {dist}')

                if d == False:
                    return (objectt.x, objectt.y)
                else:
                    return self.x+50, self.y, dist, objectt.x, objectt.y
        
        return self.x+50, self.y
    

    def coin_distance(self, objects):
        for obj in objects:
            if obj.x < self.x or type(obj) == Coin:
                return (obj.x, obj.y)
        return -1, -1



class Coin(Obstacle):

    coins = [pygame.image.load(os.path.join('images', "coin_0" + str(x) + '.png')) for x in range(1, 9)]

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.coinCount = 0
        self.hitbox = (x, y, width, height)


    def draw(self, win):
        if self.coinCount >= 32:
            self.coinCount = 0

        win.blit(self.coins[self.coinCount//4], (self.x, self.y))
        self.coinCount += 1

    def collide(self, rect):
        self.hitbox = (self.x, self.y, self.width, self.height)
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False



class Laiserwall(Obstacle):
    
    img = [pygame.image.load(os.path.join('images', 'wall0.png')), pygame.image.load(os.path.join('images', 'wall1.png')),
           pygame.image.load(os.path.join('images', 'wall2.png')), pygame.image.load(os.path.join('images', 'wall3.png'))]

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
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


    def __repr__(self):
        return f'Laiserwall at ({self.x},{self.y})'



class Obstacle2(Laiserwall):
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


    def __repr__(self):
        return f'Obstacle at ({self.x},{self.y})'
    


class Bar(GameObject):
    """
    Move this class up and create a instance for each runner.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        super().__init__(x, y, width, height)
        self.color = color


    def draw(self, win, jetpack_volume: float = None):
        
        if jetpack_volume == None: pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        else: 
            bar_length = jetpack_volume*0.01 * self.width
            pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, bar_length, self.height))