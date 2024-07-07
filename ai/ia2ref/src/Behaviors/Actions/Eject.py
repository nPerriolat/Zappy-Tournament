##
# EPITECH PROJECT, 2023
# zappy [Dev Container: zappy_docker @ unix:///run/user/1002/docker.sock]
# File description:
# Eject.py
##

"""
@file Eject.py
"""

from __future__ import annotations

from ..Action import IAction
from ..Action import ActionResultType, IAction

from ... import Player

from ..Commands import Com_Eject


class Eject(IAction):
    def __init__(self):
        super().__init__(-1, "Eject")

    def update(self, player: Player.Player):
        command = Com_Eject()
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not result:
            return ActionResultType.CHANGE_TO
        return ActionResultType.DONE
