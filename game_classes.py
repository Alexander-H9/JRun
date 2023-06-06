from abc import ABC, abstractmethod



class GameObject(ABC):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    @abstractmethod
    def draw(self, win):
        pass



class Obstacle(GameObject):

    @abstractmethod
    def collide(self):
        pass