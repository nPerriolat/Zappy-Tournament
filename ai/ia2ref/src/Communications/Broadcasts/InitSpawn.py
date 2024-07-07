##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## InitSpawn.py
##

"""
@file InitSpawn.py
"""

import json

from ..Communication import CommunicationRecv, DecoratorCommunicationRecv, CommunicationSend
from ..CommunicationType import CommunicationType

from time import time

class CDRecvInitSpawn(DecoratorCommunicationRecv):

    def __init__(self, content: CommunicationRecv):
        super().__init__(content)

    def unpack(self) -> bool:
        try:
            self.ack_id, self.team_dic = json.loads(self.content.raw_content) # the data used "json.dumps"
            return True
        except:
            return False

class CDSendInitSpawn(CommunicationSend):
    def __init__(self, msg_id: int, dic: dict[int, int]):
        super().__init__(CommunicationType.BORN_SET)
        self.data = json.dumps([msg_id, dic]) # the data used "json.loads"
