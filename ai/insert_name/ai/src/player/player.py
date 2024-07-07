import socket
import select
import random
from abc import abstractmethod
from datetime import datetime

from ai.src.utils.messages import extract_inventory
from ai.src.zappy_ai import Bot
from ai.src.gameplay.enum_gameplay import Directions as dir
from ai.src.mvt.path import Path
from ai.src.gameplay.enum_gameplay import Resources as res
from ai.src.utils.info_look import look_resources
from ai.src.gameplay.enum_gameplay import RoleInGame


class Player(Bot):
    def __init__(self, serv_info: list[int], cli_socket: socket, debug_mode: bool = False):
        """
        This class is the player class.
        
        :param serv_info: list[int] - Information about the server.
        :param cli_socket: socket - The client socket for communication.
        :param debug_mode: bool - The debug mode.
        """
        super().__init__(serv_info, cli_socket, debug_mode)
        self.limit: list[int] = self.dimensions
        self.pos: list[int] = [0, 0]
        self.inv = {}
        self.parent = None
        self.level: int = 1
        self.actions = []
        self.queue = []
        self.LIMIT_QUEUE: int = 9
        self.LEVEL_MAX: int = 8
        self.FORK_ACTION: int = 42
        self.INCUBATION_TIME: int = 600
        self.based_ressources = {'food': 10,
                                'linemate': 0,
                                'deraumere': 0,
                                'sibur': 0,
                                'mendiane': 0,
                                'phiras': 0,
                                'thystame': 0
                                }
        self.need_ressources = {'linemate': 8,
                                'deraumere': 8,
                                'sibur': 10,
                                'mendiane': 5,
                                'phiras': 6,
                                'thystame': 1
                                }
        self.inventory: dict[str: int] = self.based_ressources
        self.looked: bool = False
        self.environment: str = ""
        self.path = Path(self.limit, (0, 0), (0, 0))
        self.death: any = False
        self.got_id: int = 0
        self.eject_security = True
        self.new_born = True

        #TODO: seed is it necessary?
        random.seed(datetime.now().timestamp())
        self.id = random

        self.life = 126 * self.inventory['food']
    
        #TODO: improve the direction system
        self.dir = dir.NORTH

    def create_egg(self) -> None:
        """
        This method creates an egg.

        :return: None
        """
        self.life -= self.FORK_ACTION
        self.send_action("Fork\n")

    def turn_around_without_watching(self) -> None:
        """
        This method makes the player turn around without watching.

        :return: None
        """
        self.right()
        self.right()
        self.actions.append('Right\n')
        self.actions.append('Right\n')

    def move_without_watching(self, dire: dir, right: dir, left: dir, turn_around: dir) -> None:
        """
        This method makes the player move without watching.

        :param dire: dir - The direction to move.
        :param right: dir - The right direction.
        :param left: dir - The left direction.
        :param turn_around: dir - The turn around direction.
        :return: None
        """
        self.actions.pop()
        if dire == right:
            self.right()
            self.actions.append('Right\n')
        elif dire == left:
            self.left()
            self.actions.append('Left\n')
        elif dire == turn_around:
            self.turn_around_without_watching()
        self.forward()
        self.actions.append('Forward\n')

    def move(self, mvt: list | tuple, dire: dir) -> None:
        """
        This method makes the player move.

        :param mvt: list - The movement to be done.
        :param dire: dir - The direction to move.
        :return: None
        """
        if not mvt:
            return
        if self.pos[0] == mvt[0]:
            if self.pos[1] < mvt[1]:
                self.move_without_watching(dire, dir.NORTH, dir.SOUTH, dir.WEST)
            else:
                self.move_without_watching(dire, dir.SOUTH, dir.NORTH, dir.EAST)
        else:
            if self.pos[0] < mvt[0]:
                self.move_without_watching(dire, dir.EAST, dir.WEST, dir.SOUTH)
            else:
                self.move_without_watching(dire, dir.WEST, dir.EAST, dir.NORTH)

    def turn_to_the_north(self) -> None:
        """
        Turn the player to face the North direction.

        This method checks the current facing direction of the player and adjusts it to face North if needed.

        :return: None
        """
        # TODO - move it in Path class if possible
        if self.debug_mode:
            print('going to the north')
        if self.path.facing == dir.NORTH.value:
            return
        if self.path.facing == dir.EAST.value:
            self.queue.append('Left')
            self.life -= self.ACTION
            self.path.facing = dir.NORTH.value
        if self.path.facing == dir.WEST.value:
            self.queue.append('Right')
            self.life -= self.ACTION
            self.path.facing = dir.NORTH.value
        if self.path.facing == dir.SOUTH.value:
            self.queue.append('Right')
            self.queue.append('Right')
            self.life -= self.ACTION * 2
            self.path.facing = dir.NORTH.value

    def move_to(self, pos: tuple[int, int]) -> None:
        """
        This method makes the player move to a position.

        :param pos: tuple[int, int] - The position to move to.
        :return: None
        """
        path = Path(self.limit, self.pos, pos, self.dir).opti_path()
        for mvt in path:
            self.queue.append(mvt)

    def get_id(self, message: str, collector: bool = False) -> None:
        self.message.buf_messages(message)
        self.queue.append('Broadcast')
        self.life -= self.ACTION
        self.queue.append(('Take', 'player'))
        self.life -= self.ACTION
        self.queue.append(('Take', 'player'))
        self.life -= self.ACTION
        self.queue.append(('Take', 'player'))
        self.life -= self.ACTION
        if collector is True:
            self.message.buf_messages('situm intrare', bis=True)
            self.queue.append('Broadcast bis')
            self.life -= self.ACTION

    def get_timing(self, message: str, delay: int) -> None:
        for _ in range(delay):
            self.queue.append(('Take', 'player'))
            self.life -= self.ACTION
        self.message.buf_messages(message)
        self.queue.append('Broadcast')
        self.life -= self.ACTION

    def apply_action(self) -> None:
        """
        This method applies the action to the player.

        :return: None
        """
        self.actions.append(self.queue[0])
        self.queue.pop(0)
        if self.debug_mode:
            print(f'apply action actions: {self.actions}')
            print(f'waiting queue: {self.queue}')
        action = self.actions[-1]
        if action[0] == 'Take':
            self.take_obj(action[1])
        elif action == 'Incantation':
            # print('uuuuuuuuuuuuuuuuuuuuuuuuuui')
            self.incantation()
        elif action[0] == 'Set':
            self.set_obj(action[1])
        elif action == 'Look':
            self.look_around()
        elif action == 'Fork':
            self.create_egg()
        elif action == 'Slots':
            self.nbr_of_slot()
        elif action == 'Broadcast':
            self.broadcast()
        elif action == 'Broadcast bis':
            self.broadcast_bis()
        elif action == 'Forward':
            self.forward()
        elif action == 'Right':
            self.right()
        elif action == 'Left':
            self.left()
        elif action == 'Inventory':
            self.check_inventory()
        elif action == 'Eject':
            self.eject()
        elif isinstance(action, tuple):
            self.move(action, self.dir)

    def recv_treatment(self, buf) -> None:
        """
        Process the received data from the server.

        This method handles the data received from the server, updates player attributes accordingly, and removes the processed action from the action queue.

        :param buf: The data received from the server.
        :return: None
        """
        if len(self.actions) == 0:
            recv_list = self.message.receive(buf)
        else:
            recv_list = self.message.receive(buf, self.actions)
        for recv_type, msgs in recv_list:
            if recv_type == 'ko' and len(self.actions) > 0 and self.actions[0] == ('Take', 'player'):
                self.got_id += 1
            if recv_type == 'ok':
                if isinstance(msgs, tuple) and msgs[0] == 'Take' and msgs[1] != 'player':
                    self.inventory[msgs[1]] += 1
                    if msgs[1] == 'food':
                        self.life += self.FOOD
                if isinstance(msgs, tuple) and msgs[0] == 'Set':
                    self.inventory[msgs[1]] -= 1
            if recv_type == 'look':
                self.looked = True
                self.environment = msgs
            if recv_type == 'inventory':
                self.inventory = extract_inventory(msgs)
                self.life = self.inventory['food'] * self.FOOD
                # print(f'life: {self.life}')
                if self.debug_mode:
                    print("inventory")
            if recv_type == 'elevation':
                # print('elevation :', msgs)
                continue
            if recv_type == 'broadcast':
                if msgs == 'ko' or msgs[0] == 'ko':
                    # TODO - on vient pas skip des messages avec ce continue ?
                    continue
                for msg in msgs:
                    self.broadcast_traitement(msg)
                continue
            if recv_type == 'eject':
                self.back_on_track(msgs[-1])
                continue
            try:
                self.actions.pop(0)
            except Exception as e:
                print(e)
                print(f"pnj except : rcv_typ {recv_type}, msg {msg}")

    @abstractmethod
    def make_action(self) -> None:
        pass

    def update_inventory(self, new_object: str, action: bool) -> None:
        """
        TODO - doit être appelé quand on vient récup un obt
        """
        if action:
            self.inventory[new_object] += 1
        else:
            self.inventory[new_object] -= 1

    def run(self) -> any:
        """
        This method is the main loop of the ai.

        :return: None
        """
        while self.level < self.LEVEL_MAX:
            if self.death != False:
                return self.death
            infds, outfds, _ = select.select(self.inout, self.inout, [])

            """
            infds: list[socket] - The list of sockets to read from.
            """
            if len(infds) != 0:
                buf = self.recv_action()
                self.recv_treatment(buf)
                if buf == 'death\n':
                    return None

            """
            outfds: list[socket] - The list of sockets to write to.
            """
            if len(outfds) != 0 and len(self.actions) < self.LIMIT_QUEUE:
                self.make_action()

    @abstractmethod
    def broadcast_traitement(self, msg: tuple | str) -> None:
        pass

    def global_message(self, message: tuple | str | dict = None) -> None:
        if message and message['msg'] == 'haec est historia imperii ACCMST' and self.new_born is True:
            self.message.uuid_used = [uuid for uuid in message['infos'] if uuid not in self.message.uuid_used] + self.message.uuid_used
            print(f'new self.uuid: {self.message.uuid_used}')
            self.new_born = False

    def back_on_track(self, msg):
        """

        :param msg:
        :return:
        """
        if self.eject_security is False:
            return
        direction = int(msg)
        if direction == 3:
            self.queue.insert(0, 'Left')
        if direction == 7:
            self.queue.insert(0, 'Right')
        if direction == 5:
            self.queue.insert(0, 'Right')
            self.queue.insert(0, 'Right')
        self.queue.insert(0, 'Forward')
