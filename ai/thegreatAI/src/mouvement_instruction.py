##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## instruction
##


import asyncio
from config import *
from ia import response_filter, evolved


def get_orientation(current, target) -> str:
    x = target.col - current.col
    y = target.row - current.row

    if x == 0 and y == -1:
        return 'N'
    elif x == 1 and y == 0:
        return 'E'
    elif x == 0 and y == 1:
        return 'S'
    elif x == -1 and y == 0:
        return 'W'

def calculate_rotations(current_orientation, target_orientation) -> str:
    directions = ['N', 'E', 'S', 'W']
    current_index = directions.index(current_orientation)
    target_index = directions.index(target_orientation)
    difference = (target_index - current_index) % 4

    if difference == 1:
        return 'Right'
    elif difference == 3:
        return 'Left'
    elif difference == 2:
        return 'Back'
    else:
        return 'none'

async def perform_instructions(instructions, server_conn, ia, start) -> None:
    for instruction in instructions:
        server_conn.send_command(f'{instruction}\n')
        response = (await server_conn.get_data()).strip()
        response = await response_filter(ia, server_conn, response, ['None'])

        tmp = await evolved(ia, server_conn, start)
        while (tmp == 'ok'):
            tmp = await evolved(ia, server_conn, start)

async def instruction(path, ia, server_conn, start) -> None:
    path.reverse()
    instructions = []
    current_orientation = ia.look_direction

    for i in range(len(path) - 1):
        current_cell = path[i]
        next_cell = path[i + 1]

        target_orientation = get_orientation(current_cell, next_cell)
        if target_orientation:
            direction = calculate_rotations(current_orientation, target_orientation)
            if direction == 'Right':
                instructions.append('Right')
            elif direction == 'Left':
                instructions.append('Left')
            elif direction == 'Back':
                instructions.append('Right')
                instructions.append('Right')
            current_orientation = target_orientation
            instructions.append('Forward')
            current_cell.look_direction = current_orientation

    await perform_instructions(instructions, server_conn, ia, start)
    ia.look_direction = current_orientation
