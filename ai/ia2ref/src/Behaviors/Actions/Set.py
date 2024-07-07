##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Set.py
##

"""
@file Set.py
"""

from __future__ import annotations

from ..Action import IAction
from ..Action import ActionResultType, IAction

from ... import Player
from ...Map import ResourceType, resourcetype_to_str
from ...Constants import FOOD_MULTIPLIER

from ..Commands import Com_Set

class Set(IAction):
    def __init__(self, resource: ResourceType):
        super().__init__(-1, "Set")
        self.wanted_resource = resource

    def update(self, player: Player.Player):
        command = Com_Set(resourcetype_to_str(self.wanted_resource))
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP
        # if player.my_drone.drone_inventory[self.wanted_resource] <= 0:
            # raise ValueError(f"Resource should not be set... {self.wanted_resource}, (tile :) {player.map.get_resource(player.map.player_pos.x, player.map.player_pos.y)}")
            # return ActionResultType.CHANGE_TO

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not result:
            return ActionResultType.CHANGE_TO
        if result:
            if self.wanted_resource == ResourceType.FOOD:
                player.set_life(-FOOD_MULTIPLIER)
            else:
                player.my_drone.drone_inventory[self.wanted_resource] -= 1
        return ActionResultType.DONE
