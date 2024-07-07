##
## EPITECH PROJECT, 2023
## zappy [Dev Container: zappy_docker @ unix:///run/user/1002/docker.sock]
## File description:
## Ready.py
##

"""
@file Ready.py
"""

from __future__ import annotations
from ... import Player

from ..Communication import CommunicationRecv, DecoratorCommunicationRecv, CommunicationSend
from ..CommunicationType import CommunicationType

class CDRecvReady(DecoratorCommunicationRecv):

    def __init__(self, content: CommunicationRecv):
        super().__init__(content)
        self.concerned = False
        self.ready = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            str_pid, ready = self.content.raw_content.split(',')
            if player.my_drone.pid == int(str_pid):
                self.concerned = True
                self.ready = ready
            return True
        except:
            return False

class CDSendReady(CommunicationSend):
    def __init__(self, master_pid: int, ready = True):
        super().__init__(CommunicationType.READY)
        self.data = f"{master_pid},{ready}"
