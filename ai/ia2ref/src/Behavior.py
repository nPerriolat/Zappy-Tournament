##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Behavior.py
##

"""
@file Behavior.py
"""

from __future__ import annotations

from typing import Optional

from .Behaviors.Action import IAction, Command, ActionResultType
from . import Player
from .Locomotion import LocomotionDirection, get_reversed_direction, Direction
from .Communications.Communication import CommunicationRecv

class ABehavior:
    def __init__(self):
        self.should_wait = False
        self.finished = False
        self.must_wait = False

        self.was_suspended = False # gets modified by scheduler, don't modify here

    def update(self, player: Player.Player) -> Optional[Command]: # type: ignore
        pass

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        pass

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        return (ActionResultType.CONTINUE, None)

    def finish_suspended(self, player: Player.Player):
        """ Only called when the suspended action is DONE """
        self.finished = False
        pass

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        return False

    def handle_eject(self, player: Player.Player, direction: Direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        player.map.move_player_direction(player.map.player_dir, direction)

    def is_finished(self) -> bool:
        return self.finished

    def wants_to_wait(self) -> bool:
        return self.should_wait

    def have_to_wait(self) -> bool:
        return self.must_wait
