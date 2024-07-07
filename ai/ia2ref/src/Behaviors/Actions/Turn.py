##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Turn.py
##

"""
@file Turn.py
"""

from __future__ import annotations

from collections import deque

from ...Behaviors.Action import IAction
from ...Behaviors.Action import ActionResultType, IAction

from ... import Player
from ...Locomotion import LocomotionAction, LocomotionDirection
from ..Commands import Com_Left, Com_Right

def loc_action_to_command(locomotion: LocomotionAction):
    if locomotion == LocomotionAction.TURN_LEFT:
        return Com_Left()
    return Com_Right()

class Turn(IAction):
    def __init__(self, direction: LocomotionDirection | LocomotionAction, drone_direction : LocomotionDirection):
        super().__init__(-1, "Turn")
        if isinstance(direction, LocomotionAction):
            self.locomotions : deque[LocomotionAction] = deque([direction]) # [loc_action_to_command(direction)])
        else:
            self.locomotions : deque[LocomotionAction] = deque(self.__calculate_commands(direction, drone_direction))
        self.previons_action: LocomotionAction = LocomotionAction.FORWARD

    def update(self, player: Player.Player):
        if len(self.locomotions) == 0:
            return ActionResultType.DONE
        self.previons_action = self.locomotions.popleft()
        self.cur_command = loc_action_to_command(self.previons_action)
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not result:
            return ActionResultType.CONTINUE
        player.map.move_player(self.previons_action)
        if len(self.locomotions) == 0:
            return ActionResultType.DONE
        return ActionResultType.CONTINUE

    ## PRIVATE ##

    def __calculate_commands(self, direction: LocomotionDirection, drone_direction: LocomotionDirection) -> list[LocomotionAction]:
        if direction == drone_direction:
            return []
        match drone_direction:
            case LocomotionDirection.UP:
                match direction:
                    case LocomotionDirection.RIGHT:
                        return [LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.DOWN:
                        return [LocomotionAction.TURN_RIGHT, LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.LEFT:
                        return [LocomotionAction.TURN_LEFT]
            case LocomotionDirection.RIGHT:
                match direction:
                    case LocomotionDirection.DOWN:
                        return [LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.LEFT:
                        return [LocomotionAction.TURN_RIGHT, LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.UP:
                        return [LocomotionAction.TURN_LEFT]
            case LocomotionDirection.DOWN:
                match direction:
                    case LocomotionDirection.LEFT:
                        return [LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.UP:
                        return [LocomotionAction.TURN_RIGHT, LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.RIGHT:
                        return [LocomotionAction.TURN_LEFT]
            case LocomotionDirection.LEFT:
                match direction:
                    case LocomotionDirection.UP:
                        return [LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.RIGHT:
                        return [LocomotionAction.TURN_RIGHT, LocomotionAction.TURN_RIGHT]
                    case LocomotionDirection.DOWN:
                        return [LocomotionAction.TURN_LEFT]
        return []
