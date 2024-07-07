##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# MoveToMe.py
##

"""
@file MoveToMe.py
"""

from __future__ import annotations
from ... import Player

import json

from ..Communication import CommunicationSend, DecoratorCommunicationRecv, CommunicationRecv
from ..CommunicationType import CommunicationType
from ...Map import Position

from ...Locomotion import LocomotionAction


class CDRecvMoveToCoords(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False
        self.coords = Position(-1, -1)

    def unpack(self, player: Player.Player) -> bool:
        try:
            list_coords, pids = json.loads(self.content.raw_content)
            if pids == "*" or str(player.my_drone.pid) in pids:
                self.concerned = True
                # the coordinates are offset from the base, shared between all drones that incante together
                base_coords = player.my_drone.base_coords
                self.coords = Position(
                    base_coords.x + list_coords[0], base_coords.y + list_coords[1])
            return True
        except:
            return False

    def should_follow(self) -> bool:
        return self.concerned


class CDRecvMasterCancelMove(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            if self.content.raw_content == "*":
                self.concerned = True
                return True

            pids = self.content.raw_content.split(',')
            if str(player.my_drone.pid) in pids:
                self.concerned = True
            return True
        except:
            return False

    def should_follow(self) -> bool:
        return self.concerned


class CDRecvMoveToMe(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            pids = self.content.raw_content.split(',')
            if str(player.my_drone.pid) in pids:
                self.concerned = True
            return True
        except:
            return False

    def should_follow(self) -> bool:
        return self.concerned


class CDRecvMoveBase(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False
        self.actions: list[LocomotionAction] = []

    def unpack(self, player: Player.Player) -> bool:
        try:
            if self.content.drone_id == player.my_drone.jefe_pid:
                self.concerned = True
                actions = self.content.raw_content.split(',')
                self.actions = [LocomotionAction(
                    int(action)) for action in actions]
            return True
        except:
            return False

##########################################


class CDSendMoveToMe(CommunicationSend):
    """
    @class CommunicationSend
    @brief Parent SEND Class, self.data will be modified via child classes and use Broadcast to pack it.
    @details
    Extract overhead so the decorator can further parse the requests
    """

    def __init__(self, concerned: list[int] | bool) -> None:
        super().__init__(CommunicationType.MOVE_TO_ME)
        if isinstance(concerned, bool):
            self.data = "*"
        else:
            self.data = ','.join(list(map(str, concerned)))


class CDSendMasterCancelMove(CommunicationSend):
    def __init__(self, concerned: list[int] | bool) -> None:
        super().__init__(CommunicationType.MA_CANCEL_TO_MOVE)
        if isinstance(concerned, bool):
            self.data = "*"
        else:
            self.data = ','.join(list(map(str, concerned)))


class CDSendMoveToCoords(CommunicationSend):
    def __init__(self, concerned: list[int] | bool, offset_pos: Position) -> None:
        super().__init__(CommunicationType.MOVE_TO_COORDS)
        payload = []
        if isinstance(concerned, bool):
            payload[0] = "*"
        else:
            payload[0] = ','.join(list(map(str, concerned)))
        payload[1] = [offset_pos.x, offset_pos.y]
        self.data = json.dumps(payload)


class CDSendMoveBase(CommunicationSend):
    def __init__(self, list_actions: list[LocomotionAction]) -> None:
        super().__init__(CommunicationType.UPDATE_BASE_COORDS)
        l = [action.value for action in list_actions]
        self.data = ','.join(map(str, l))
