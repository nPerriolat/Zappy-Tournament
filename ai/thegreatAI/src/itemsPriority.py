##
## EPITECH PROJECT, 2024
## ZAPPY [WSL: Ubuntu]
## File description:
## itemsPriority
##


import random
from config import *
from cell import *
from ia import IA


def calculate_priority(list_cell: list[Cell], player: IA) -> Cell:
    cell = Cell(player.LVL, player.LVL * 2)
    tmp_list: list[Cell] = []
    have = 0

    if player.inventory.food < 50:
        for cell in list_cell:
            if (cell.row == player.LVL and cell.col == player.LVL):
                continue
            if '3' in str(cell.value):
                tmp_list.append(cell)
                have = 1

        if have == 0:
            for cell in list_cell:
                if (cell.row == player.LVL and cell.col == player.LVL):
                    continue
                tmp = str(cell.value)
                tmp = tmp.replace('1', '0')
                if int(tmp) >= 2:
                    tmp_list.append(cell)

    else:
        for cell in list_cell:
            if (cell.row == player.LVL and cell.col == player.LVL):
                continue
            if cell.value >= 2:
                tmp_list.append(cell)

    tmp_list = sort_nearest_cell(tmp_list, Cell(player.LVL, player.LVL))
    if not tmp_list:
        cell.row = random.randrange(0, player.LVL + 1)
        cell.col = random.randrange(0, player.LVL + 1)
        tmp_list.append(cell)

    return tmp_list[0]
