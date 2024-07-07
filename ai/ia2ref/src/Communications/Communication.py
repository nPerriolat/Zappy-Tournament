##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## Communication.py
##

"""
@file Communication.py
"""
from __future__ import annotations

import base64
from typing import Optional

from .CommunicationType import CommunicationType
from ..Locomotion import LocomotionDirection, get_direction_from_str
from .. import Player

class CommunicationRecv:
    """
    @class CommunicationRecv
    @brief Parent RECV Class, later to be decorated via specific classes
    @details
    Extract overhead so the decorator can further parse the requests
    """
    def __init__(self, raw_content: str) -> None:
            dir, self.raw_msg = raw_content.split(", ")
            self.dir = get_direction_from_str(dir)
            self.parsed = False

    def unpack(self) -> bool:
        """
        Data is like : [int,base64]
        The return values is stored in the class
        """
        try:
            if self.raw_msg[0] != '%' or self.raw_msg[-1] != '%':
                return False

            stripped_string = self.raw_msg.strip(r'%%')
            parts = stripped_string.split('&', 4)

            self.key = int(parts[0])
            self.drone_id = int(parts[1])
            self.msg_id = int(parts[2])
            self.type = CommunicationType(int(parts[3]))
            base64_string = parts[4]

            self.raw_content = base64.b64decode(base64_string).decode('ascii')
            self.parsed = True
            return True
        except:
            return False # corruption

    def get_msg_headers(self) -> tuple[int, int, int, CommunicationType]:
        return self.key, self.drone_id, self.msg_id, self.type

    def get_data(self) -> tuple[int, int, int, CommunicationType, str]:
        """ Assumes you've already parsed """
        return self.key, self.drone_id, self.msg_id, self.type, self.raw_content

class DecoratorCommunicationRecv:
    def __init__(self, content: CommunicationRecv) -> None:
        self.content = content

    def unpack(self, player: Player.Player) -> bool: # type: ignore
        pass

#################################""

class CommunicationSend:
    """
    @class CommunicationSend
    @brief Parent SEND Class, self.data will be modified via child classes and use Broadcast to pack it.
    @details
    Extract overhead so the decorator can further parse the requests
    """
    def __init__(self, type: CommunicationType) -> None:
        self.key = -1
        self.drone_id: int = -1
        self.msg_id: int = -1
        self.type: CommunicationType = type
        self.data: str = ""

    def set_header(self, key: int, my_drone_id: int, new_msg_id: int) -> None:
        self.key = key
        self.drone_id = my_drone_id
        self.msg_id = new_msg_id

    def pack(self) -> str:
        encoded = base64.b64encode(self.data.encode('ascii')).decode('ascii')
        return f"%{self.key}&{self.drone_id}&{self.msg_id}&{self.type.value}&{encoded}%"
