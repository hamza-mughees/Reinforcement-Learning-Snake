from collections import namedtuple

colours = {
    'black': (0,0,0),
    'white': (255,255,255),
    'red': (200,0,0),
    'green_big': (0,200,0),
    'green_small': (0,250,0)
}

settings = {
    'block_size': 20,
    'speed': 20,
}

Point = namedtuple('Point', ['x', 'y'])