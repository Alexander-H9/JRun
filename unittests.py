import unittest
from unittest.mock import MagicMock
import pygame
from model import Player, Coin, Laiserwall


# Mocking pygame functions
pygame.image.load = MagicMock(return_value=pygame.Surface((64, 64)))

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(100, 200, 50, 50)

    def test_player_initialization(self):
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 200)
        self.assertEqual(self.player.width, 50)
        self.assertEqual(self.player.height, 50)
        self.assertEqual(self.player.runCount, 0)
        self.assertFalse(self.player.jeting)


class TestCoin(unittest.TestCase):

    def setUp(self):
        self.coin = Coin(100, 200, 30, 30)

    def test_coin_initialization(self):
        self.assertEqual(self.coin.x, 100)
        self.assertEqual(self.coin.y, 200)
        self.assertEqual(self.coin.width, 30)
        self.assertEqual(self.coin.height, 30)
        self.assertEqual(self.coin.coinCount, 0)

    def test_coin_draw(self):
        win = pygame.Surface((800, 600))
        self.coin.draw(win)
        # Add assertions to check if the coin is drawn correctly

    def test_coin_collide(self):
        rect = (120, 220, 50, 50)
        result = self.coin.collide(rect)
        self.assertTrue(result)


class TestLaiserwall(unittest.TestCase):

    def setUp(self):
        self.wall = Laiserwall(100, 200, 50, 100)

    def test_wall_initialization(self):
        self.assertEqual(self.wall.x, 100)
        self.assertEqual(self.wall.y, 200)
        self.assertEqual(self.wall.width, 50)
        self.assertEqual(self.wall.height, 100)
        self.assertEqual(self.wall.count, 0)

    def test_wall_collide(self):
        rect = (120, 220, 50, 50)
        result = self.wall.collide(rect)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()