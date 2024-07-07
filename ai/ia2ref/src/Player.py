##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Player.py
##

"""
@file Player.py
"""

from enum import Enum
from typing import Optional
from multiprocessing import Process
from random import randint
from copy import deepcopy

from .SocketController import SocketController
from .Map import Map, Position, ResourceType, Direction
from .BehaviorList import calculate_behavior
from .BehaviorScheduler import BehaviorScheduler
from .Utils.OSUtils import get_pid
from .Constants import INITIAL_FOOD


class PlayerRole(Enum):
    NONE = -1
    MASTER = 0
    SLAVE = 1
    TROLL = 2


class Drone:
    """
    @brief Drone class, shows information, these info are shared across other drones
    """

    def __init__(self, id: int, role: PlayerRole, jefe_pid: int = -1, base_coords: Position = Position(-1, -1)) -> None:
        self.id = id
        self.pid = get_pid()
        self.jefe_pid = jefe_pid
        self.role = role

        self.knows_base = False
        # base coords are the first time they all incant together, subjective coordinates
        self.base_coords = base_coords
        self.jefe_dir = Direction.SAME_TILE

        self.coords = base_coords
        self.level = 1
        self.drone_inventory = {
            ResourceType.FOOD: INITIAL_FOOD,
            ResourceType.LINEMATE: 0,
            ResourceType.DERAUMERE: 0,
            ResourceType.SIBUR: 0,
            ResourceType.MENDIANE: 0,
            ResourceType.PHIRAS: 0,
            ResourceType.THYSTAME: 0
        }
        self.unwanted_incant = False

    def __str__(self) -> str:
        return f"Drone {self.id} : {self.coords} - {self.drone_inventory} - JEFE {self.jefe_pid}"


class Player:
    """
    @brief Player class
    """

    def __init__(self, port: int, host: str, team_name: str, is_forked: bool = False, jefe_pid: int = -1, broadcast_key: int = -1, preload_broadcast: bool = False):
        self.team_name = team_name
        self.key = broadcast_key
        self.should_preload_broadcast = preload_broadcast
        self.controller = SocketController(
            port, host, is_forked, key=broadcast_key, preload_broadcast=preload_broadcast)
        connect_res = self.controller.connect(self.team_name)
        if connect_res is None:
            raise Exception("Connection failed")
        id, max_coords, self.max_connects = self.__parse_connection_res(
            *connect_res)
        self.other_drones: dict[int, Drone] = {}
        self.role = self.__calculate_role(is_forked)
        self.map = Map(*max_coords, self.role == PlayerRole.TROLL)
        self.my_drone = Drone(id, self.role, jefe_pid)
        behavior = calculate_behavior(self)
        self.behavior_scheduler = BehaviorScheduler(behavior, behavior)
        self.com_was_none = False

    def think(self) -> bool:
        """
        @brief Think method
        Return false if the player is disconnected, else true
        """
        cur_len_commands = self.controller.get_command_queue_size()
        # certain action waiting for a broadcast message must wait, no actions in cache
        if self.behavior_scheduler.have_to_wait() and not self.controller.has_results_in_cache():
            self.controller.wait_unblock_actions(self.my_drone)
        elif not self.com_was_none and (cur_len_commands >= 10 or self.behavior_scheduler.wants_to_wait()):
            """
            The client has too many commands in the queue, waits until a new command is issued
            Notice : a broadcast may stop the waiting, the command resonses will be empty
            """

            # Wait until a response comes out, before applying broadcasts
            while not self.controller.wait_unblock_actions(self.my_drone):
                pass
        else:
            self.controller.recv_commands(self.my_drone)

        prev_responses = self.controller.get_command_responses()
        if self.controller.is_disconnected():
            return False
        command = self.behavior_scheduler.update(self,
                                                 prev_responses, self.controller.get_pushed_directions())
        if command is not None:
            self.controller.execute_action(command)
            self.set_life(-command.time)
            self.com_was_none = False
        else:
            self.com_was_none = True
        return True

    def fork(self, preload_broadcast: bool = False) -> Optional[int]:
        """
        @brief Fork method
        """
        def handle_new_player(port: int, host: str, team_name: str, jefe_pid: int, key: int, preload_broadcast: bool):
            p = Player(port, host, team_name, True,
                       jefe_pid, key, preload_broadcast)
            try:
                while p.think():
                    pass
                return 0
            except RuntimeError as e:
                if p.my_drone.level >= 7:  # server disconnected automatically
                    return 0
                print("Subprocess:", e)
                return 84

        proc = Process(target=handle_new_player, args=(self.controller.socket.port,
                                                       self.controller.socket.host,
                                                       self.team_name,
                                                       self.my_drone.pid,
                                                       self.key,
                                                       preload_broadcast))
        proc.daemon = True
        proc.start()
        return proc.pid

    def get_life(self) -> int:
        """
        @brief Get the player life
        """
        return self.my_drone.drone_inventory[ResourceType.FOOD]

    def set_life(self, life: int, accumulate: bool = True) -> None:
        """
        @brief Set the player life
        """
        if accumulate:
            self.my_drone.drone_inventory[ResourceType.FOOD] += life
        else:
            self.my_drone.drone_inventory[ResourceType.FOOD] = life

    def get_inventory(self):
        """
        Faster way to access it
        """
        return self.my_drone.drone_inventory

    def set_new_base(self, pos_diff: Optional[Position] = None) -> Position:
        """
        base_coords are modified
        """
        if not self.my_drone.knows_base:
            raise Exception("Drone doesn't know the base")
        if pos_diff is None:
            x_max = self.map.max_x // 2
            y_max = self.map.max_y // 2
            x_diff = randint(-x_max, x_max) + 1
            y_diff = randint(-y_max, y_max) + 1
            pos_diff = Position(x_diff, y_diff)

        x = (self.my_drone.base_coords.x + pos_diff.x) % self.map.max_x
        y = (self.my_drone.base_coords.y + pos_diff.y) % self.map.max_y
        new_pos = Position(x, y)
        self.map.update_db_base(new_pos, self.my_drone.base_coords)
        self.my_drone.base_coords = new_pos
        return pos_diff

    def set_first_base(self, pos: Position) -> Position:
        """
        base_coords are modified
        """
        new_pos = deepcopy(pos)
        self.map.update_db_base(new_pos, self.my_drone.base_coords)
        self.my_drone.base_coords = new_pos
        return pos

    def set_first_base_dir(self, direction: Direction):
        self.my_drone.jefe_dir = direction

    # Private

    def __calculate_role(self, is_forked: bool) -> PlayerRole:
        if not is_forked:
            return PlayerRole.MASTER
        # TODO: implement troll role and other based on mutatation probability
        return PlayerRole.SLAVE

    def __parse_connection_res(self, id: str, raw_coords: str, nb_connects: str) -> tuple[int, tuple[int, int], int]:
        """
        @brief Parse the connection response
        @param id: Client id
        @param raw_coords: Raw coordinates
        @return: Parsed connection response
        """
        coords = raw_coords.split(' ')
        x, y = coords
        return int(id), (int(x), int(y)), int(nb_connects)
