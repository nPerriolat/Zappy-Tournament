##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Broadcast.py
##

"""
@file Broadcast.py
"""

from __future__ import annotations

from ..Action import IAction
from ..Action import ActionResultType, IAction

from ... import Player

from ..Commands import Com_Broadcast
from ...Communications.Communication import CommunicationSend

class Broadcast(IAction):
    def __init__(self, send: CommunicationSend):
        super().__init__(-1, "Broadcast")
        self.send = send

    def update(self, player: Player.Player):
        """
        Assumes you know it's here based on y
        """
        payload = player.controller.broadcastHandler.create_broadcast(self.send)
        command = Com_Broadcast(payload)
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not result:
            return ActionResultType.CHANGE_TO
        return ActionResultType.DONE

