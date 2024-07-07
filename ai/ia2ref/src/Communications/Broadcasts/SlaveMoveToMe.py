##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## MoveToMe.py
##

"""
@file MoveToMe.py
"""

from __future__ import annotations
from ... import Player

from ..Communication import CommunicationSend, DecoratorCommunicationRecv, CommunicationRecv
from ..CommunicationType import CommunicationType

class CDRecvOKToMove(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            if player.my_drone.pid == int(self.content.raw_content):
                self.concerned = True
            return True
        except:
            return False

class CDRecvSlaveCancelMove(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False
        self.ejected = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            str_pids, ejected = self.content.raw_content.split(',')

            if player.my_drone.pid == int(str_pids):
                self.concerned = True
                self.ejected = ejected == "1"
            return True
        except:
            return False

class CDRecvDoneMove(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            if player.my_drone.pid == int(self.content.raw_content):
                self.concerned = True
            return True
        except:
            return False

#################################""

class CDSendOKToMove(CommunicationSend):
    """
    @class CommunicationSend
    @brief Parent SEND Class, self.data will be modified via child classes and use Broadcast to pack it.
    @details
    Extract overhead so the decorator can further parse the requests
    """
    def __init__(self, master_pid: int) -> None:
        super().__init__(CommunicationType.OK_TO_MOVE)
        self.data = str(master_pid)

class CDSendSlaveCancelMove(CommunicationSend):
    def __init__(self, master_pid: int, ejected: bool) -> None:
        super().__init__(CommunicationType.CL_CANCEL_TO_MOVE)
        self.data = f"{master_pid},{int(ejected)}"

class CDSendDoneMove(CommunicationSend):
    def __init__(self, master_pid: int) -> None:
        super().__init__(CommunicationType.DONE_MOVE)
        self.data = str(master_pid)
