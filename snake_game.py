import pygame
import random
from enum import Enum
from collections import namedtuple

colours = {
    'black': (0,0,0),
    'white': (255,255,255),
    'red': (200,0,0),
    'green_big': (0,250,0),
    'green_small': (0,200,0)
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
        self._update()
    
    def _update(self):
        self.display.fill(colours['black'])

        block_border_size = 2

        for p in self.snake:
            pygame.draw.rect(self.display, 
                            colours['green_big'],
                            pygame.Rect(p.x, p.y, 
                                    settings['block_size'], 
                                    settings['block_size']))
            pygame.draw.rect(self.display, 
                            colours['green_small'],
                            pygame.Rect(p.x + block_border_size, 
                                        p.y + block_border_size, 
                                        settings['block_size'] - 2*block_border_size, 
                                        settings['block_size'] - 2*block_border_size))
        
        pygame.draw.rect(self.display,
                        colours['red'],
                        pygame.Rect(self.food.x, self.food.y,
                                    settings['block_size'], 
                                    settings['block_size']))
        
        text = font.render(f'Score: {str(self.score)}', True, colours['white'])
        self.display.blit(text, [0,0])
        pygame.display.flip()
    
    def _place_food(self):
        x_max_scaled = (self.width - settings['block_size']) // settings['block_size']
        y_max_scaled = (self.height - settings['block_size']) // settings['block_size']
        x = random.randint(0, x_max_scaled) * settings['block_size']
        y = random.randint(0, y_max_scaled) * settings['block_size']
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

if __name__ == '__main__':
    game = SnakeGame()