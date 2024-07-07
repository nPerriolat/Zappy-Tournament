from socket import socket
import time

from ai.src.player.player import Player
from ai.src.utils.info_look import look_resources, only_forward_resources
from ai.src.gameplay.enum_gameplay import Directions as compass


class Collector(Player):

    def __init__(self, serv_info: list[int] | None = None, cli_socket: socket | None = None, debug_mode: bool = False):
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
        self.need_eat = 0
        self.the_place_to_be: tuple[int, int] = (0, 0)
        self.focus: list[str] = ['thystame', 'phiras', 'mendiane', 'deraumere', 'sibur', 'linemate', 'food']
        self.nbr_focus: list[int] = [0]
        self.depot: tuple[int, int] = (0, 0)
        self.hard_focus: bool = False
        self.id = 0
        self.start: bool = False
        self.get_id('Quot publicani ibi sunt?', collector=True)
        self.start_path: list = []
        self.deposit_path: list = []
        self.start_pos: list = [0, 0]
        self.empty: bool = True
        self.lvl_one: bool = False

    def get_deposit_path(self) -> list:
        """

        :return:
        """
        if self.id % 2 == 0 and self.id != 0:
            path = ['Left']
        else:
            path = ['Right']
        path += ['Forward'] * ((self.id // 2) + self.id % 2)
        if self.debug_mode:
            print(f'path to depot is: {path}')
        return path

    def go_to_start(self) -> None:
        """

        :return:
        """
        if self.id == 0:
            self.queue.append('Forward')
            self.start_path = ['Forward']
            self.start = True
            return
        if self.id % 2 == 0:
            self.path.start = (0, 0)
            self.path.end = (1, int(self.id / 2))
        else:
            self.path.start = (0, 0)
            self.path.end = (1, self.path.limit[0] - 1 - self.id // 2)

        self.start_path = [item for sublist in self.path.get_path()
                           for item in (sublist if isinstance(sublist, list) else [sublist])]
        if self.id != 0:
            self.deposit_path = self.get_deposit_path()
        if self.debug_mode:
            print(f'start: {self.path.start}')
            print(f'end: {self.path.end}')
            print(f'queue without path: {self.queue}')
            print(f'facing: {self.path.facing}')
        self.start_pos[0], self.start_pos[1] = self.path.end
        self.pos[0], self.pos[1] = self.path.end
        for index, move in enumerate(self.start_path):
            self.queue.append(move)
            self.life -= self.ACTION
        self.message.buf_messages(message='sum extra domum')
        self.queue.append('Broadcast')
        self.life -= self.ACTION
        if self.debug_mode:
            print(f'queue with path: {self.queue}')
            print(f'start path: {self.start_path}')
            print(f'2nd start: {self.path.start}')
            print(f'2nd end: {self.path.end}')
            print(f'deposit path: {self.deposit_path}')
        self.start = True
        self.turn_to_the_north()

    def raids_resources(self, tiles) -> None:
        """
        Perform raids on resources based on the given tiles and focus.

        :param tiles: list - List of tiles to search for resources.
        :return: None
        """
        for tile in tiles:
            for resource in tile:
                if resource in self.focus:
                    self.queue.append(("Take", resource))
                    self.life -= self.ACTION
            self.deactivate_pusher()
            if (self.pos == self.start_pos and self.id != 0 and not self.empty and not
               (self.id == 1 and not self.lvl_one)):
                break
            self.queue.append('Forward')
            self.life -= self.ACTION
            self.pos[0] = (self.pos[0] + 1) % (self.limit[0] - 1)
            if self.debug_mode:
                print(f'lim: {self.limit[0]}')
                print(f'pos: {self.pos}')
                print(f'start: {self.start_pos}')
            if (self.pos == self.start_pos and self.id == 0) or (self.id == 1 and not self.lvl_one):
                break
            if self.pos[0] == self.start_pos[0] + 1:
                self.empty = False

    def moving_straight(self, ) -> None:
        """
        Move the player straight while focusing on specific resources.

        :return: None
        """
        tiles = look_resources(self.environment, self.focus)
        self.looked = False
        self.environment = ""
        tiles = only_forward_resources(tiles)
        self.raids_resources(tiles)
        if self.pos == self.start_pos:
            self.deposits_resources()
            self.turn_to_the_north()

    def reset_focus(self) -> None:
        """
        Reset the focus of the player to default values.

        :return: None
        """
        self.focus = ['linemate', 'deraumere', 'sibur', 'mendiane', 'phiras', 'thystame', 'food']
        self.hard_focus = False
        self.nbr_focus = []

    def deposits_resources(self) -> None:
        """
        Deposits the resources from the player's inventory.
        This method adds the resources to the queue for depositing and remove it from the inventory.

        :return: None
        """
        self.empty = True
        forward_count = 0
        before_depot = len(self.deposit_path) - 2
        for index, move in enumerate(self.deposit_path):
            if index == before_depot and self.id > 2:
                self.message.buf_messages('situm intrare')
                self.queue.append('Broadcast')
                self.life -= self.ACTION
            self.queue.append(move)
            self.life -= self.ACTION
        self.deposit_ressources()
        if self.id % 2 == 0 and self.id != 0:
            self.queue.append('Right')
            self.life -= self.ACTION
        elif self.id % 2 == 1:
            self.queue.append('Left')
            self.life -= self.ACTION
        for move in self.start_path:
            if move == 'Left':
                self.path.facing = (self.path.facing - 1) % 4
            if move == 'Right':
                self.path.facing = (self.path.facing + 1) % 4
            self.queue.append(move)
            if move == 'Forward':
                forward_count += 1
                if forward_count == 2 and self.id > 2:
                    self.message.buf_messages(message='sum extra domum', bis=True)
                    self.queue.insert(2, 'Broadcast bis')
                    self.life -= self.ACTION
        self.life -= self.ACTION
        self.turn_to_the_north()

    def make_action(self) -> None:
        """
        Perform the next action based on the current state of the player.
        This method checks if there are pending actions,
        looks around if needed, and applies the next action in the queue.

        :return: None
        """
        if 0 < len(self.queue) and len(self.actions) < 1:
            self.apply_action()
        if len(self.actions) > 0:
            return
        if not self.looked and 'Look' not in self.queue and self.start is not False:
            self.queue.append('Look')
            self.life -= self.ACTION
        if self.looked:
            if len(self.queue) == 0:
                self.moving_straight()
            self.looked = False

    def broadcast_traitement(self, message: tuple | str | dict) -> None:
        """
        Process the broadcast message and take appropriate actions.

        :param message: tuple | str | dict - The message received for broadcast processing.
        :return: None
        """
        if message['msg'] == 'quid habes ut nobis offerat':
            self.message.buf_messages('opes in meo inventario sunt : ',
                                      infos=[(key, str(value)) for key, value in self.inventory.items()])
            self.queue.append('Broadcast')
        if message['msg'] == 'focus in his opibus : ':
            self.focus = message['infos']
            self.nbr_focus = message['nbr']
        if message['msg'] == 'collectio rerum : ':
            self.depot = message['coord']
        if message['msg'] == 'Potes dominum facti':
            self.queue.append('Forward')
            self.queue.append('Forward')
            self.deposits_resources()
        if message['msg'] == 'est dominus aquilonis':
            if self.path.facing is None:
                self.path.get_north(message['direction'])
                self.turn_to_the_north()
            if self.got_id > 2 and self.start is False:
                self.go_to_start()
        if message['msg'] == 'Ego sum publicani ibi' and self.got_id < 3:
            self.id += 1
        if message['msg'] == 'Quot publicani ibi sunt?':
            self.message.buf_messages('Ego sum publicani ibi', my_id=[self.id])
            self.queue.insert(0, 'Broadcast')
        if message['msg'] == 'nobilis incantatio':
            self.lvl_one = True
        self.global_message(message)

    def deactivate_pusher(self):
        """

        :return:
        """
        if ((0 < self.id < 3 and self.pos[0] == (self.start_pos[0] - 2) % (self.limit[0] - 1)) or
                (self.id == 0 and self.pos[0] == (self.start_pos[0] - 3) % (self.limit[0] - 1))):
            self.message.buf_messages('situm intrare')
            self.queue.append('Broadcast')
            self.life -= self.ACTION
        if ((0 < self.id < 3 and self.pos[0] == (self.start_pos[0]) % (self.limit[0] - 1)) or
                (self.id == 0 and self.pos[0] == (self.start_pos[0] + 1) % (self.limit[0] - 1))):
            self.message.buf_messages(message='sum extra domum', bis=True)
            self.queue.insert(2, 'Broadcast bis')
            self.life -= self.ACTION

    def deposit_ressources(self):
        """

        :return:
        """
        for resource in self.inventory:
            if resource != 'food':
                for _ in range(self.inventory[resource]):
                    self.queue.append(('Set', resource.__str__()))
                    self.inventory[resource] -= 1
                    self.life -= self.ACTION
