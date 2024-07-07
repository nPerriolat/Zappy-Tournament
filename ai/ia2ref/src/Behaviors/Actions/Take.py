##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Take.py
##

"""
@file Take.py
"""

from __future__ import annotations

from ...Behaviors.Action import IAction
from ...Behaviors.Action import ActionResultType, IAction

from ... import Player
from ...Map import ResourceType, resourcetype_to_str
from ...Constants import FOOD_MULTIPLIER

from ..Commands import Com_Take

class Take(IAction):
    def __init__(self, resource: ResourceType, dont_check: bool = False):
        super().__init__(-1, "Take")
        self.wanted_resource = resource
        self.dont_check = dont_check

    def update(self, player: Player.Player):
        """
        Assumes you know it's here based on y
        """
        command = Com_Take(resourcetype_to_str(self.wanted_resource))
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not self.dont_check and not player.map.take_resource(self.wanted_resource):
            raise ValueError(f"Resource should not be taken... {self.wanted_resource}, (tile :) {player.map.get_resource(player.map.player_pos.x, player.map.player_pos.y)}")
        if not result:
            return ActionResultType.CHANGE_TO
        if result:
            if self.wanted_resource == ResourceType.FOOD:
                player.set_life(FOOD_MULTIPLIER)
            else:
                player.my_drone.drone_inventory[self.wanted_resource] += 1
        return ActionResultType.DONE
