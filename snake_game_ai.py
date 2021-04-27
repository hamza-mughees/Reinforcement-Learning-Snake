import pygame
import random
import numpy as np
from enum import Enum
from config import *

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGameAI:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        self.display = pygame.display.set_mode(
                        (self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.reset()
    
    # initial game state
    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head,
                      Point(self.head.x - settings['block_size'], self.head.y),
                      Point(self.head.x - 2*settings['block_size'], self.head.y)]
        
        self.food = None
        self.score = 0

        self._place_food()
        self.frame_iter = 0
    
    # render display updates
    def _update(self):
        self.display.fill(colours['black'])

        block_border_size = 3

        for pt in self.snake:
            # display and colour snake outer body
            pygame.draw.rect(self.display, 
                            colours['green_big'],
                            pygame.Rect(pt.x, pt.y, 
                                    settings['block_size'], 
                                    settings['block_size']))
            # display and colour snake inner body
            pygame.draw.rect(self.display, 
                            colours['green_small'],
                            pygame.Rect(pt.x + block_border_size, 
                                        pt.y + block_border_size, 
                                        settings['block_size'] - 2*block_border_size, 
                                        settings['block_size'] - 2*block_border_size))
        
        # display and colour food
        pygame.draw.rect(self.display,
                        colours['red'],
                        pygame.Rect(self.food.x, self.food.y,
                                    settings['block_size'], 
                                    settings['block_size']))
        
        # display scoring text
        text = font.render(f'Score: {str(self.score)}', True, colours['white'])
        self.display.blit(text, [0,0])
        pygame.display.flip()
    
    # random food positioning
    def _place_food(self):
        x_max_scaled = (self.width - settings['block_size']) // settings['block_size']
        y_max_scaled = (self.height - settings['block_size']) // settings['block_size']
        x = random.randint(0, x_max_scaled) * settings['block_size']
        y = random.randint(0, y_max_scaled) * settings['block_size']
        self.food = Point(x, y)
        # if food is on snake, replace it
        if self.food in self.snake:
            self._place_food()
    
    def take_step(self, action):
        self.frame_iter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # update head (take the move to self.direction)
        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0

        if self.is_collision() or self.frame_iter > 100*len(self.snake):
            # return -10 reward, game over, and score
            reward = -10
            return reward, True, self.score
        
        # if snake eats food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        self.clock.tick(settings['speed'])
        self._update()

        # return reward, game not over, and score
        return reward, False, self.score
    
    def _move(self, action):
        # [straight, right, left]
        l, idx = self._get_direction_list_idx()

        if np.array_equal(action, [1,0,0]):
            # no change in direction
            self.direction = l[idx]
        elif np.array_equal(action, [0,1,0]):
            # turn right
            idx = (idx + 1) % 4     # cycle back from up to right
            self.direction = l[idx]
        else:       # action = [0,0,1]
            # turn left
            idx = (idx - 1) % 4     # cycle back from right to up
            self.direction = l[idx]

        x, y = self._get_head()

        if self.direction == Direction.RIGHT:
            x += settings['block_size']
        if self.direction == Direction.LEFT:
            x -= settings['block_size']
        if self.direction == Direction.UP:
            y -= settings['block_size']
        if self.direction == Direction.DOWN:
            y += settings['block_size']
        
        self.head = Point(x, y)
    
    def _get_direction_list_idx(self):
        l = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        return l, l.index(self.direction)

    def _get_head(self):
        return self.head.x, self.head.y

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # check snake hits its own body
        if pt in self.snake[1:]:
            return True

        w, h = self.width, self.height
        bs = settings['block_size']

        # check snake hits a wall
        if pt.x + bs > w or pt.x < 0 or pt.y + bs > h or pt.y < 0:
            return True
        
        return False