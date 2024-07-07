##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# SocketController.py
##

"""
@file SocketController.py
"""

from __future__ import annotations

from typing import Optional, Callable
from collections import deque
from select import select
from collections import deque
from time import time, sleep

from . import Player
from .Socket.ZappySocket import ZappySocket
from .Events.Broadcast import Broadcast, CommunicationRecv
from .Behaviors.Action import Command
from .Locomotion import Direction, get_direction_from_str


class SocketController:
    """
    @class SocketController
    @brief Socket class for Zappy AI
    @details
    This class is used as a wrapper to send and receive requests
    """

    def __init__(self, port: int, host: str, is_forked: bool, should_store_enemy_msg=False, key: int = -1, preload_broadcast:bool = False):
        self.socket = ZappySocket(port, host)
        self.broadcastHandler = Broadcast(key, should_store_enemy_msg, is_forked, preload_broadcast)
        self.should_stop = False

        # parse the value based on the previous command
        self.callback_prev_command: deque[Callable[[
            str], bool | list[str] | int]] = deque(maxlen=10)
        self.res_prev_command = deque()
        self.pushed_directions = deque()

    def __del__(self) -> None:
        del self.socket

    def is_disconnected(self) -> bool:
        return self.should_stop

    def connect(self, team_name: str) -> Optional[tuple[str, str, str]]:
        """
        Returns unparsed client id and map coordinates
        """
        max_attempt = 100
        cur_attempt = 0
        while True:
            try:
                self.socket.connect()
                self.socket.recv()
                self.socket.send(team_name)
                vals = self.socket.recv()
                if vals is None:
                    return None

                id, coords = vals
                self.socket.send("Connect_nbr")
                vals = self.socket.recv()
                if vals is None:
                    return None

                nb_clients = vals[0]
                self.socket.set_blocking(False)
                return id, coords, nb_clients
            except Exception as e:
                self.socket.reset()
                cur_attempt += 1
                if cur_attempt == max_attempt:
                    return None
                sleep(0.2)

    def execute_action(self, command: Command) -> int:
        """
        @brief Send the current command of the action
        returns whether the action pool accepts the action (10 is the max)
        """
        cur_len = len(self.callback_prev_command)
        if self.callback_prev_command.maxlen == cur_len:
            return cur_len
        self.socket.send(command.payload)
        self.callback_prev_command.append(command.parse_callback)
        return cur_len + 1

    def get_command_queue_size(self) -> int:
        return len(self.callback_prev_command)

    def recv_commands(self, drone: Player.Drone):
        payloads_received = self.socket.recv()
        response_to_command = False
        if payloads_received:
            for p in payloads_received:
                response_to_command |= self.__addEvent(p, drone)
        return response_to_command

    def has_results_in_cache(self) -> bool:
        return len(self.broadcastHandler.broadcasts) != 0 \
            or len(self.res_prev_command) != 0 \
            or len(self.pushed_directions) != 0

    def clear_command_queue(self):
        """
        Clear the callback queue, do it when something unexpected occured
        """
        self.callback_prev_command.clear()

    def get_command_responses(self) -> list:
        return [self.res_prev_command.pop() for _ in range(len(self.res_prev_command))]

    def get_broadcasts(self) -> list[CommunicationRecv]:
        return self.broadcastHandler.pop_broadcasts()

    def get_pushed_directions(self) -> list[Direction]:
        return [self.pushed_directions.pop() for _ in range(len(self.pushed_directions))]

    def wait_unblock_actions(self, drone: Player.Drone, timeout: float | None = None) -> bool:
        """
        Will wait forever until the server responds
        returns if in the responses, a command response was received
        """
        try:
            read, _, _ = select([self.socket.socket], [], [], timeout)
            if read:
                return self.recv_commands(drone)
            return False
        except Exception as e:
            print(e)
            raise RuntimeError("Error while waiting for server response")

    def disconnects(self, _: str, __: Player.Drone) -> bool:
        print("Disconnected........")
        self.socket.close()
        self.should_stop = True
        return False

    # Private

    def _add_broadcasts(self, payload: str, _) -> bool:
        self.broadcastHandler.consume(payload)
        return False

    def _process_prev_commands(self, payload: str) -> bool:
        if not self.callback_prev_command:
            return False

        callback = self.callback_prev_command.popleft()
        self.res_prev_command.append(callback(payload))
        return True

    def _process_player_interaction(self, payload: str, _) -> bool:
        self.pushed_directions.append(get_direction_from_str(payload))
        return False

    def _process_cur_elevation(self, payload: str, drone: Player.Drone) -> bool:
        if self.callback_prev_command and self.callback_prev_command[0].__name__ == "parse_incantation":
            callback = self.callback_prev_command.popleft()
            self.res_prev_command.append(callback(payload))
            return True
        drone.level = int(payload[CUR_LEVEL_PAYLOAD_OFFSET:])
        drone.unwanted_incant = False
        return True

    def _process_elevation(self, _: str, drone: Player.Drone) -> bool:
        if not self.callback_prev_command or self.callback_prev_command[0].__name__ != "parse_incantation":
            drone.unwanted_incant = True
        return False

    def __addEvent(self, payload: str, drone: Player.Drone) -> bool:
        """
        returns whenever the event was a response to a command
        """
        for [header, (lenght, func)] in EVENT_HEADERS.items():
            if not payload.startswith(header):
                continue
            return func(self, payload[lenght:], drone)
        return self._process_prev_commands(payload)


################################################################################


EVENT_HEADERS = {
    "message ": (len("message "), SocketController._add_broadcasts),
    "dead": (len("dead"), SocketController.disconnects),
    "eject: ": (len("eject: "), SocketController._process_player_interaction),
    # Elevation underway
    "Ele": (len("Ele"), SocketController._process_elevation),
    "Cur": (len("Cur"), SocketController._process_cur_elevation)  # Current level: k
}

CUR_LEVEL_PAYLOAD_OFFSET = len("rent level: ") # since 'Cur' was already spliited, only use this offset