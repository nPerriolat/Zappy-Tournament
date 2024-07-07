##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## cell
##

from config import *


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE_X
        self.y = row * CELL_SIZE_Y
        self.neighbors = []
        self.visited = False
        self.value = 0

    def add_neighbors(self, grid) -> None:
        rows = len(grid)
        cols = len(grid[0])
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < cols - 1:
            self.neighbors.append(grid[self.row][self.col + 1])

    def calculate_distance(self, player_pos) -> float:
        return (((self.row - player_pos.row) ** 2) +
                ((self.col - player_pos.col) ** 2)) ** 0.5

    def __str__(self) -> str:
        return f'({self.row},{self.col})'


def convert_to_list(LVL, VIEW) -> None:
    global ROWS, COLS, CELL_SIZE_X, CELL_SIZE_Y, CREATION_VIEW
    ROWS = LVL + 1
    COLS = (LVL * 2) + 1
    CELL_SIZE_X = WIDTH // COLS
    CELL_SIZE_Y = HEIGHT // ROWS

    elements = VIEW.strip('[]').split(',')

    values = []
    for element in elements:
        items = element.split(' ')
        combined_value = int(''.join(str(mapping[item]) for item in items if item in mapping))
        values.append(combined_value)

    CREATION_VIEW = [[0] * COLS for _ in range(ROWS)]
    tmp = 0
    for i in range(ROWS):
        for j in range((ROWS - 1) - i, (COLS - (ROWS - 1) + i)):
            if tmp < len(values):
                CREATION_VIEW[i][j] = values[tmp]
                tmp += 1

    CREATION_VIEW.reverse()


def create_grid(LVL, VIEW) -> list:
    convert_to_list(LVL, VIEW)
    grid = []
    for row in range(ROWS):
        grid.append([])
        for col in range(COLS):
            cell = Cell(row, col)
            cell.value = CREATION_VIEW[row][col]
            grid[-1].append(cell)
    return grid


def sort_nearest_cell(list_cell, player) -> list:
    return sorted(list_cell, key=lambda cell: cell.calculate_distance(player))


def check_point_cell(grid, LVL) -> list:
    list_cell = []
    for row in grid:
        for cell in row:
            list_cell.append(cell)

    player = Cell(LVL, LVL)
    return sort_nearest_cell(list_cell, player)
