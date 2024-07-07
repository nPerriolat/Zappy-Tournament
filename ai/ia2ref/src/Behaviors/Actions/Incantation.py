##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Incantation.py
##

"""
@file Incantation.py
"""

from __future__ import annotations

from ..Action import IAction
from ..Action import ActionResultType, IAction

from ... import Player
from ...Map import ResourceType, resourcetype_to_str

from ..Commands import Com_Incant, IncantationStatus

class Incantation(IAction):
    def __init__(self):
        super().__init__(-1, "Incantation")

    def update(self, player: Player.Player):
        """
        Assumes you know it's here based on y
        """
        command = Com_Incant()
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.already_doing = True
        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        res = IncantationStatus(result)

        if res == IncantationStatus.BAD:
            print("incantation failed")
            return ActionResultType.CHANGE_TO
        if res == IncantationStatus.FINISH:
            player.my_drone.level += 1
            return ActionResultType.DONE
        return ActionResultType.CONTINUE
