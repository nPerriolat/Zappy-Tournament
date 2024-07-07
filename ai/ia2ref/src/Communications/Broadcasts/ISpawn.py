##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## ISpawn.py
##

"""
@file ISpawn.py
"""

from __future__ import annotations
from ... import Player

from ..Communication import CommunicationRecv, DecoratorCommunicationRecv, CommunicationSend
from ..CommunicationType import CommunicationType

class CDRecvISpawn(DecoratorCommunicationRecv):

    def __init__(self, content: CommunicationRecv):
        super().__init__(content)
        self.concerned = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            jefe_pid = int(self.content.raw_content)
            if player.role == Player.PlayerRole.MASTER \
                and player.my_drone.pid == jefe_pid:
                self.concerned = True
            return True
        except:
            return False

class CDSendISpawn(CommunicationSend):
    def __init__(self, master_pid: int = -1):
        super().__init__(CommunicationType.BORN_NEW)
        self.data = f"{master_pid}"
