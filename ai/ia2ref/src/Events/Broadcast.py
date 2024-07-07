##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Broadcast.py
##

"""
@file SocketController.py
"""

from collections import deque
from typing import Optional
from copy import copy

from ..Communications.Communication import CommunicationRecv, CommunicationSend
from ..Communications.Broadcasts.InitSpawn import CDRecvInitSpawn
from ..Communications.CommunicationType import CommunicationType
from ..Utils.OSUtils import check_pid, get_pid

MAX_ENEMY_BROADCASTS = 20
KEY = "NOGITHUBHISTORY!"


class BroadcastVerification:
    def __init__(self, data: dict[int, int], key: int) -> None:
        """
        Initialize a Broadcast object.

        Args:
            data (dict[int, int]): The data dictionary.
            key (int): The key to tell which team is which.

        Returns:
            None
        """
        self.dict = data
        self.is_frozen = False
        self.key = key

    def is_valid(self, key: int, drone_id: int, msg_id: int) -> bool:
        """
        Side effect (auto msg_id increment) if valid
        """

        if self.is_frozen:
            return False
        if key != self.key:
            return False # same IA, different team

        val = self.dict.get(drone_id)
        if val is None:
            if check_pid(drone_id):
                self.dict[drone_id] = msg_id
                return True
            return False
        if msg_id < val + 1:
            return False  # repetition
        self.dict[drone_id] += 1
        return True

    def set_freeze(self, freezeValue: bool) -> None:
        self.is_frozen = freezeValue


class Broadcast:
    """
    @class SocketController
    @brief Socket class for Zappy AI
    @details
    This class is used as a wrapper to send and receive requests
    """

    def __init__(self, key: int, should_store_enemy_msgs=False, is_forked=True, activate: bool = False) -> None:
        self.broadcasts: deque[CommunicationRecv] = deque()
        self.store_enemy_msgs = should_store_enemy_msgs
        self.verification: Optional[BroadcastVerification] = BroadcastVerification(
            {}, key) if not is_forked or activate else None
        self.msg_index = 0
        self.key = key
        self.id = get_pid()
        if should_store_enemy_msgs:
            self.enemybroadcasts: deque[str] = deque(
                maxlen=MAX_ENEMY_BROADCASTS)

    def consume(self, rawContent: str) -> None:
        try:
            recv = CommunicationRecv(rawContent)
            unpackData = recv.unpack()
            if not unpackData:
                raise Exception()
            (key, drone_id, msg_index, com_type) = recv.get_msg_headers()
            # print(get_pid(), "received", drone_id, msg_index, com_type)
        except:
            if self.__shoulStoreEnemyMsgs():
                self.enemybroadcasts.append(rawContent)
            return

        # gradually update the counter
        if not self.__is_activated():
            if com_type == CommunicationType.BORN_SET:
                self.broadcasts.append(recv)
            return  # Is activated in NewSpawn SubBehavior.
        if not self.verification.is_valid(key, drone_id, msg_index):  # type: ignore
            return
        self.broadcasts.append(recv)

    def create_broadcast(self, send: CommunicationSend) -> str:
        """
        Returns the value packed with the drone id and the message id
        """
        self.msg_index += 1
        send.set_header(self.key, self.id, self.msg_index)
        return send.pack()

    def pop_broadcasts(self) -> list[CommunicationRecv]:
        broadcasts = list(self.broadcasts)
        self.broadcasts.clear()
        return broadcasts

    def activate(self, recv_broadcast: CDRecvInitSpawn) -> None:
        if recv_broadcast.unpack():
            self.verification = BroadcastVerification(recv_broadcast.team_dic, self.key)

    def get_activation(self) -> Optional[dict[int, int]]:
        """
        When a new player spawns, get the master dict
        """
        if self.verification is None:
            return None
        dic = copy(self.verification.dict)  # need only shallow copy
        dic[self.id] = self.msg_index  # set mine since it's not here
        return dic

    def __is_activated(self):
        return self.verification is not None

    def __shoulStoreEnemyMsgs(self) -> bool:
        return self.store_enemy_msgs and self.__is_activated()
