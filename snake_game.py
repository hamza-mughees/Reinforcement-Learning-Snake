import pygame
import random
from enum import Enum
from config import *

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
    
    # render display updates
    def _update(self):
        self.display.fill(colours['black'])

        block_border_size = 3

        for p in self.snake:
            # display and colour snake outer body
            pygame.draw.rect(self.display, 
                            colours['green_big'],
                            pygame.Rect(p.x, p.y, 
                                    settings['block_size'], 
                                    settings['block_size']))
            # display and colour snake inner body
            pygame.draw.rect(self.display, 
                            colours['green_small'],
                            pygame.Rect(p.x + block_border_size, 
                                        p.y + block_border_size, 
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
    
    def take_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if key pressed, check directions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # update head (take the move to self.direction)
        self._move()
        self.snake.insert(0, self.head)

        if self._collided():
            # return game over and score
            return True, self.score
        
        # if snake eats food
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        self.clock.tick(settings['speed'])
        self._update()

        # return game not over and score
        return False, self.score
    
    def _move(self):
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

    def _get_head(self):
        return self.head.x, self.head.y

    def _collided(self):
        # check snake hits its own body
        if self.head in self.snake[1:]:
            return True

        x, y = self._get_head()
        w, h = self.width, self.height
        bs = settings['block_size']

        # check snake hits a wall
        if x + bs > w or x < 0 or y + bs > h or y < 0:
            return True

def game_loop():
    snake_game = SnakeGame()

    while True:
        is_game_over, score = snake_game.take_step()

        if is_game_over:
            break
    
    print(f'Final Score: {score}')

if __name__ == '__main__':
    game_loop()