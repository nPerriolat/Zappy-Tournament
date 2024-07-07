##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## bfs
##

import time
import importlib.util
from server import Server
from collections import deque
from cell import Cell

async def go_to_friend(message: str, ia, server_conn: Server) -> None:
    parts = message.split(',')

    if len(parts) < 2:
        return
    lvl_tmp = ia.LVL
    if str(lvl_tmp) not in parts[1]:
        ia.is_following = False
        return
    case_number = parts[0].split(" ")
    if len(case_number) <= 1 or not case_number[1].isdigit():
        return

    direction = get_direction_from_case_number(int(case_number[1]), ia)
    grid_size = 3
    grid = create_initial_grid(grid_size)

    if direction == [1, 1]:
        ia.is_following = False
        ia.is_waiting = False
    print(direction)
    await bfs(grid[1][1], grid[direction[0]][direction[1]], grid, ia, server_conn)


def create_initial_grid(size: int) -> list:
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            cell = Cell(i, j)
            row.append(cell)
        grid.append(row)
    for row in grid:
        for cell in row:
            cell.add_neighbors(grid)
    return grid


def get_direction_from_case_number(case_number: int, ia) -> list:
    directions = {
        0: (1, 1),  # none
        1: (0, 1),  # N
        2: (0, 0),  # NW
        3: (1, 0),  # W
        4: (2, 0),  # SW
        5: (2, 1),  # S
        6: (2, 2),  # SE
        7: (1, 2),  # E
        8: (0, 2)   # NE
    }
    relative_direction = directions.get(case_number, (1, 1))
    adjusted_direction = adjust_direction_based_on_orientation(relative_direction, ia.look_direction)
    return [adjusted_direction[0], adjusted_direction[1]] if adjusted_direction else [1, 1]


def adjust_direction_based_on_orientation(direction: tuple, orientation: str) -> tuple:
    x, y = direction
    if orientation == 'N':
        return (y, x)
    elif orientation == 'E':
        return (y, 2 - x)
    elif orientation == 'S':
        return (2 - y, 2 - x)
    elif orientation == 'W':
        return (2 - y, x)
    return (1, 1)


async def bfs(start: Cell, end: Cell, grid: list, ia, server_conn: Server) -> bool:
    for row in grid:
        for cell in row:
            cell.visited = False

    queue = deque([start])
    start.visited = True
    path = {}

    while queue:
        current = queue.popleft()
        if current == end:
            await reconstruct_path(path, start, end, server_conn, ia)
            return True

        for neighbor in current.neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                queue.append(neighbor)
                path[neighbor] = current
    return False


async def reconstruct_path(path: dict, start: Cell, end: Cell, server_conn: Server, ia) -> None:
    current = end
    list_path = []
    while current != start:
        list_path.append(current)
        current = path[current]
    list_path.append(start)

    mouvement_instruction = 'mouvement_instruction'
    spec = importlib.util.spec_from_file_location(mouvement_instruction, f"src/{mouvement_instruction}.py")
    instruction_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(instruction_module)
    await instruction_module.instruction(list_path, ia, server_conn, start)
