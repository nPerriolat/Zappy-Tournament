##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Fork.py
##

"""
@file Fork.py
"""

from __future__ import annotations

from ...Behaviors.Action import IAction
from ...Behaviors.Action import ActionResultType, IAction

from ... import Player

from ..Commands import Com_Fork

class Fork(IAction):
    def __init__(self):
        super().__init__(-1, "Fork")

    def update(self, player: Player.Player):
        """
        Assumes you know it's here based on y
        """
        command = Com_Fork()
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not result:
            return ActionResultType.CHANGE_TO
        drone_pid = player.fork()
        if drone_pid is None or drone_pid == -1:
            return ActionResultType.CHANGE_TO
        # TODO: not necessarily slave, but master.role | slave
        player.other_drones[drone_pid] = Player.Drone(drone_pid, Player.PlayerRole.SLAVE, player.my_drone.pid)
        return ActionResultType.DONE
