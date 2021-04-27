import pygame
import random
from enum import Enum
from collections import namedtuple

colours = {
    'black': (0,0,0),
    'white': (255,255,255),
    'red': (200,0,0),
    'green': (0,200,0)
}

settings = {
    'block_size': 20,
    'speed': 20,
}

Point = namedtuple('Point', ['x', 'y'])

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        self.display = pygame.display.set_mode(
                        (self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head,
                      Point(self.head.x - settings['block_size'], self.head.y),
                      Point(self.head.x - 2*settings['block_size'], self.head.y)]
        
        self.food = None
        self.score = 0

        self._place_food()
    
    def _place_food(self):
        pass

if __name__ == '__main__':
    game = SnakeGame()