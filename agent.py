import torch
import random
import numpy as np
from collections import deque
from snake_game_ai import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LR = 0.001

class Agent:
    def __init__(self):
        self.n_episodes = 0     # number of games
        self.epsilon = 0        # randomness
        self.gamma = 0          # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        # TODO: mode, trainer

    def get_state(self, snake_game):
        pass

    def remember(self, state, action, reward, next_state, is_game_over):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, is_game_over):
        pass

    def get_action(self, state):
        pass

def train():
    scores = []
    mean_scores = []
    total_score = 0
    record_score = 0
    agent = Agent()
    snake_game = SnakeGameAI()

    while True:
        # get current state
        curr_state = agent.get_state(snake_game)
        # get move
        move = agent.get_action(curr_state)
        # perform move and get new state
        reward, is_game_over, score = snake_game.take_step(move)
        new_state = agent.get_state(snake_game)

        # train short memory
        agent.train_short_memory(state=curr_state,
                                action=move,
                                reward=reward,
                                next_state=new_state,
                                is_game_over=is_game_over)
        # remember
        agent.remember(state=curr_state,
                    action=move,
                    reward=reward,
                    next_state=new_state,
                    is_game_over=is_game_over)
        
        if is_game_over:
            # train long memory, plot result
            snake_game.reset()
            agent.n_episodes += 1
            agent.train_long_memory()

            if score > record_score:
                record_score = score
                # agent.model.save()
            
            print(f'Game: {agent.n_episodes}')
            print(f'Score: {score}')
            print(f'Record score: {record_score}')

            # TODO: plotting

if __name__ == '__main__':
    train()