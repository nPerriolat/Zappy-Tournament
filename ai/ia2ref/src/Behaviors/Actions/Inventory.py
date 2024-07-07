##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Inventory.py
##

"""
@file Inventory.py
"""

from __future__ import annotations

import multiprocessing

from ..Action import IAction
from ..Action import ActionResultType, IAction

from ... import Player
from ...Map import ResourceType, resourcetype_from_str
from ...Constants import FOOD_MULTIPLIER

from ..Commands import Com_Inventory

class Inventory(IAction):
    def __init__(self, only_food: bool = False):
        """
        only_food will only check the food, taking less time
        """
        super().__init__(-1, "Inventory")
        self.only_food = only_food

    def update(self, player: Player.Player):
        """
        Assumes you know it's here based on y
        """
        command = Com_Inventory(not self.only_food)
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: list[str] | bool | int | str) -> ActionResultType:
        if not result:
            return ActionResultType.CHANGE_TO
        try:
            if self.only_food: # kind of hacky, but avoids loading resources we don't care
                player.my_drone.drone_inventory[ResourceType.FOOD] = int(result[1:].lstrip()[4:].lstrip().split(',', 1)[0]) # type: ignore
                player.my_drone.drone_inventory[ResourceType.FOOD] *= FOOD_MULTIPLIER
                return ActionResultType.DONE
            for res in result: # type: ignore
                resource, n = res.strip().split(' ')
                player.my_drone.drone_inventory[resourcetype_from_str(resource)] = int(n)
            player.my_drone.drone_inventory[ResourceType.FOOD] *= FOOD_MULTIPLIER
            return ActionResultType.DONE
        except Exception as e:
            print(multiprocessing.current_process().name, "Error inventory:", e, f"{result}")
            return ActionResultType.CHANGE_TO
