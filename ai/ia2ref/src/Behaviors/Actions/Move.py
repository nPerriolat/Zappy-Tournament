##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Move.py
##

"""
@file Move.py
"""

from __future__ import annotations

import multiprocessing

from collections import deque

from ...Behaviors.Action import IAction
from ...Map import Position
from ...Behaviors.Action import ActionResultType, IAction
from ... import Player
from ...Algorithms.PathFinding import calculate_shortest_path
from ...Locomotion import LocomotionDirection, LocomotionAction
from ..Commands import Com_Forward, Com_Left, Com_Right

def locomotion_to_command(locomotion: LocomotionAction):
    match locomotion:
        case LocomotionAction.FORWARD:
            return Com_Forward()
        case LocomotionAction.TURN_LEFT:
            return Com_Left()
        case LocomotionAction.TURN_RIGHT:
            return Com_Right()

class Move(IAction):
    """
    Be very aware with this action in behaviors, ejects is corrupting the precalculated path
    This is action must be changed if ejected...
    Automatically modulo the position to the map size
    """
    def __init__(self, from_pos: Position, to_pos: Position, direction: LocomotionDirection, max_x: int, max_y: int, path: list[LocomotionAction] | None = None):
        super().__init__(-1, "Move")
        if path is None:
            self.goto_position = Position(to_pos.x % max_x, to_pos.y % max_y)
            path = calculate_shortest_path(direction, from_pos, to_pos, max_x, max_y)
            self.path = deque(path)
        else:
            self.path = deque(path)
        self.previous_action = None

    def update(self, player: Player.Player) -> ActionResultType:
        if self.__is_done(player):
            return ActionResultType.DONE
        self.previons_action = self.path.popleft()
        command = locomotion_to_command(self.previons_action)
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not result:
            return ActionResultType.CHANGE_TO
        if self.previons_action is not None:
            player.map.move_player(self.previons_action)
        if self.__is_done(player):
            return ActionResultType.DONE
        return ActionResultType.CONTINUE

    def __is_done(self, player: Player.Player):
        # TODO: temp, maybe don't care for exemple on base reset.
        return len(self.path) == 0
        # if de:
        #     if player.map.player_pos.x != self.goto_position.x or player.map.player_pos.y != self.goto_position.y:
        #         print(multiprocessing.current_process().name, "WTF IS DONE")
        # return de
