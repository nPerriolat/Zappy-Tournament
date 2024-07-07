##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## config
##

VIEW = None

DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

NOTHING = 0
EMPTY = 1
PLAYER = 2
FOOD = 3
LINEMATE = 4
DERAUMERE = 5
SIBUR = 6
MENDIANE = 7
PHIRAS = 8
THYSTAME = 9

mapping = {
    '': EMPTY,
    'player': PLAYER,
    'food': FOOD,
    'thystame': THYSTAME,
    'linemate': LINEMATE,
    'deraumere': DERAUMERE,
    'sibur': SIBUR,
    'mendiane': MENDIANE,
    'phiras': PHIRAS
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 0, 0
CELL_SIZE_X, CELL_SIZE_Y = 0, 0

CREATION_VIEW = []

evolution_list = [
    'linemate',
    'linemate,deraumere,sibur',
    'linemate,linemate,sibur,phiras,phiras',
    'linemate,deraumere,sibur,sibur,phiras',
    'linemate,deraumere,deraumere,sibur,mendiane,mendiane,mendiane',
    'linemate,deraumere,deraumere,sibur,sibur,sibur,phiras',
    'linemate,linemate,deraumere,deraumere,sibur,sibur,mendiane,mendiane,phiras,phiras,thystame'
]