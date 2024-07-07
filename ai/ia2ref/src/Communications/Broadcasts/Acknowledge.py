##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## Acknowledge.py
##

"""
@file Acknowledge.py
"""

from __future__ import annotations
from ... import Player

import json

from ..Communication import CommunicationRecv, DecoratorCommunicationRecv, CommunicationSend
from ..CommunicationType import CommunicationType

class CDRecvAcknowledge(DecoratorCommunicationRecv):

    def __init__(self, content: CommunicationRecv, id: int):
        """
        Id is the id of the message when transmitted, avoiding clash with other handlers
        """
        super().__init__(content)
        self.id = id
        self.acknowledged = False

    def unpack(self) -> bool:
        try:
            id, ack = json.loads(self.content.raw_content)
            if id == self.id and ack == True:
                self.acknowledged = True
            return True
        except:
            return False

    #####################

    def did_acknowledge(self) -> bool:
        return self.acknowledged

class CDSendAcknowledge(CommunicationSend):
    def __init__(self, id: int, response: bool):
        super().__init__(CommunicationType.ACKNOWLEDGE)
        self.data = json.dumps([id, response])
