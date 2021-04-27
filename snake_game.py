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

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4