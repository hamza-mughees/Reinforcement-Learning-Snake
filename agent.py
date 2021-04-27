import torch
import random
import numpy as np
from collections import deque
from snake_game_ai import SnakeGameAI, Direction, Point
from model import LinearQNN, QTrainer
from plotting import plot
from config import settings

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.n_episodes = 0     # number of games
        self.epsilon = 0        # randomness
        self.gamma = 0.95       # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNN(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

    def get_state(self, snake_game):
        head = snake_game.snake[0]

        # neighboring points to the head of snake
        left_pt = Point(head.x - settings['block_size'], head.y)
        right_pt = Point(head.x + settings['block_size'], head.y)
        up_pt = Point(head.x, head.y - settings['block_size'])
        down_pt = Point(head.x, head.y + settings['block_size'])

        # current direction of snake
        left_dir = snake_game.direction == Direction.LEFT
        right_dir = snake_game.direction == Direction.RIGHT
        up_dir = snake_game.direction == Direction.UP
        down_dir = snake_game.direction == Direction.DOWN

        state = [
            # danger ahead
            (left_dir and snake_game.is_collision(left_pt)) or
            (right_dir and snake_game.is_collision(right_pt)) or
            (up_dir and snake_game.is_collision(up_pt)) or
            (down_dir and snake_game.is_collision(down_pt)),

            # danger on the right
            (left_dir and snake_game.is_collision(up_pt)) or
            (right_dir and snake_game.is_collision(down_pt)) or
            (up_dir and snake_game.is_collision(right_pt)) or
            (down_dir and snake_game.is_collision(left_pt)),

            # danger on the left
            (left_dir and snake_game.is_collision(down_pt)) or
            (right_dir and snake_game.is_collision(up_pt)) or
            (up_dir and snake_game.is_collision(left_pt)) or
            (down_dir and snake_game.is_collision(right_pt)),

            # current direction
            left_dir,
            right_dir,
            up_dir,
            down_dir,

            # relative food location
            snake_game.food.x < snake_game.head.x,      # food left
            snake_game.food.x > snake_game.head.x,      # food right
            snake_game.food.y < snake_game.head.y,      # food up
            snake_game.food.y > snake_game.head.y       # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, is_game_over):
        self.memory.append((state, action, reward, next_state, is_game_over))

    def train_long_memory(self):
        if len(self.memory) < BATCH_SIZE:
            mini_sample = self.memory
        else:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        
        states, actions, rewards, next_states, is_game_over_statues = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, is_game_over_statues)

    def train_short_memory(self, state, action, reward, next_state, is_game_over):
        self.trainer.train_step(state, action, reward, next_state, is_game_over)

    def get_action(self, state):
        # random moves: tradeoff of exploration / exploitation
        self.epsilon = 80 - self.n_episodes

        one_hot_move = [0,0,0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            one_hot_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            one_hot_move[move] = 1
        
        return one_hot_move

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
                agent.model.save()
            
            print(f'Game: {agent.n_episodes}')
            print(f'Score: {score}')
            print(f'Record score: {record_score}')

            scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_episodes
            mean_scores.append(mean_score)
            plot(scores, mean_scores)

if __name__ == '__main__':
    train()