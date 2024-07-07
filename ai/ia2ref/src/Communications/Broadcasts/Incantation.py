##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# IncantationStatus.py
##

"""
@file IncantationStatus.py
"""

from __future__ import annotations
from ... import Player

import json

from ..Communication import CommunicationRecv, DecoratorCommunicationRecv, CommunicationSend
from ..CommunicationType import CommunicationType
from ...Map import ResourceType


class CDRecvAskInventory(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            pids = json.loads(self.content.raw_content)
            if player.my_drone.pid in pids:
                self.concerned = True
            return True
        except:
            return False

class CDRecvInventory(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False
        self.inventory: dict[ResourceType, int] = {}

    def unpack(self, player: Player.Player) -> bool:
        try:
            pid, inventory = json.loads(self.content.raw_content)
            if player.my_drone.pid == pid:
                self.concerned = True
                self.inventory = {ResourceType(int(k)): v for k, v in inventory.items()}
            return True
        except Exception as e:
            print(e)
            return False

class CDRecvDrop(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False
        self.diff_inventory: dict[ResourceType, int] = {}

    def unpack(self, player: Player.Player) -> bool:
        try:
            pid, inventory = json.loads(self.content.raw_content)
            if player.my_drone.pid == pid:
                self.concerned = True
                self.diff_inventory = {ResourceType(int(k)): v for k, v in inventory.items()}
            return True
        except:
            return False

class CDRecvDoneDrop(DecoratorCommunicationRecv):
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

class CDRecvIncantStatus(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False
        self.is_done = False

    def unpack(self, player: Player.Player) -> bool:
        try:
            pids, id = json.loads(self.content.raw_content)
            if player.my_drone.pid in pids:
                self.concerned = True
                self.is_done = id
            return True
        except:
            return False

class CDRecvGatherResources(DecoratorCommunicationRecv):
    def __init__(self, recv: CommunicationRecv) -> None:
        super().__init__(recv)
        self.concerned = False
        self.resource = ResourceType.FOOD
        self.amount = 0

    def unpack(self, player: Player.Player) -> bool:
        try:
            str_pid, str_res, str_amount = self.content.raw_content.split(',')
            if player.my_drone.pid == int(str_pid):
                self.concerned = True
                self.resource = ResourceType(int(str_res))
                self.amount = int(str_amount)
            return True
        except:
            return False

#####################


class CDSendAskInventory(CommunicationSend):
    def __init__(self, concerned: list[int]) -> None:
        super().__init__(CommunicationType.ASK_INVENTORY)
        self.data = json.dumps(concerned)

class CDSendInventory(CommunicationSend):
    def __init__(self, master_pid: int, inventory: dict[ResourceType, int]) -> None:
        super().__init__(CommunicationType.SHARE_INVENTORY)
        self.data = json.dumps(
            [master_pid, {res.value: x for res, x in inventory.items()}])

class CDSendDrop(CommunicationSend):
    def __init__(self, slave_id: int, diff_inventory: dict[ResourceType, int]) -> None:
        super().__init__(CommunicationType.DROP_RESOURCES)
        self.data = json.dumps(
            [slave_id, {res.value: x for res, x in diff_inventory.items()}])

class CDSendDoneDrop(CommunicationSend):
    def __init__(self, master_pid: int) -> None:
        super().__init__(CommunicationType.DONE_DROP)
        self.data = str(master_pid)

class CDSendIncantStatus(CommunicationSend):
    def __init__(self, concerned: list[int], is_done: bool) -> None:
        super().__init__(CommunicationType.INCANT_STATUS)
        self.data = json.dumps([concerned, is_done])

class CDSendGatherResources(CommunicationSend):
    def __init__(self, slave_pid: int, resource: ResourceType, amount: int) -> None:
        super().__init__(CommunicationType.GATHER_RESOURCES)
        self.data = f"{slave_pid},{resource.value},{amount}"
