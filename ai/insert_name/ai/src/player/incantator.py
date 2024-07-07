from socket import socket

from ai.src.player.player import Player
from ai.src.utils.messages import extract_inventory

class Incantator(Player):
    """
    Incantator class
    """

    def __init__(self, serv_info: list[int] | None = None, cli_socket: socket | None = None, debug_mode: bool = False):
        """
        Incantator class constructor
        """
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
        self.allowed_incantation_mns = 1
        self.goto = (0, self.limit[1] - 1)
        self.dir = None
        self.first_round = True
        self.pos = [0, 0]
        self.map = [[0 for _ in range(self.limit[0])] for _ in range(self.limit[1])]
        self.have_linemate = False
        self.count_pos = 0
        self.comback = []
        self.unset = True
        self.ready = False
        self.count = 0

    def goto_place(self, i: int) -> None:
        """
        This method makes the incantator go to the case i.

        :param i: int - The case to go to.
        :return: None
        """
        if i != 0:
            self.queue.append('Forward')
        if i == 1:
            self.queue.append('Left')
            self.queue.append('Forward')
        elif i == 3:
            self.queue.append('Right')
            self.queue.append('Forward')
        self.queue.append(('Take', 'linemate'))

    def addapt_map(self, vision : str) -> None:
        """
        This method adapts the map to the look message.

        :param look: str - The look message.
        :return: None
        """
        vi = vision.replace('[', '').replace(']', '')
        list_vision = vi.split(',')
        for i in range(len(list_vision)):
            case = list_vision[i].split(' ')
            if self.debug_mode:
                print(f'case: {case} and i: {i}')
            if 'linemate' in case and self.have_linemate == False:
                self.goto_place(i)
                return
            else:
                vertical = int(i ** 0.5)
                horizontal = i - vertical * (vertical + 1)
                if self.debug_mode:
                    print(f'horizontal: {horizontal} and vertical: {vertical}')
                if self.dir == 0:
                    x = (self.pos[0] + vertical) % self.limit[0]
                    y = (self.pos[1] - horizontal) % self.limit[1]
                elif self.dir == 1:
                    x = (self.pos[0] + horizontal) % self.limit[0]
                    y = (self.pos[1] - vertical) % self.limit[1]
                elif self.dir == 2:
                    x = (self.pos[0] - vertical) % self.limit[0]
                    y = (self.pos[1] - horizontal) % self.limit[1]
                else:
                    x = (self.pos[0] + horizontal) % self.limit[0]
                    y = (self.pos[1] + vertical) % self.limit[1]
                if self.debug_mode:
                    print (f'x: {x} and y: {y}')
                    print (f'pos: {self.pos}')
                    print (f'dir: {self.dir}')
                self.map[x][y] = 1
                if self.debug_mode:
                    for k in self.map:
                        for j in k:
                            print(j, end=' ')
                        print()
                    print('-------------------------------------------------')

    def goto_01(self) -> None:
        """
        This method makes the incantator go to the case (0, 1).

        :return: None
        """
        self.queue = self.comback
        self.queue.insert(0, 'Right')
        self.queue.insert(0, 'Right')
        self.comback = []

    def npos(self, old_pos :tuple[int, int]) -> list[int, int]:
        pos = [old_pos[0], old_pos[1]]
        if self.dir == 0:
            pos[0] = (pos[0] + 1) % self.limit[0]
        elif self.dir == 3:
            pos[1] = (pos[1] + 1) % self.limit[1]
        elif self.dir == 2:
            pos[0] = (pos[0] - 1) % self.limit[0]
        else:
            pos[1] = (pos[1] - 1) % self.limit[1]
        return pos

    def recv_treatment(self, buf: str) -> None:
        """
        This method treats the received message.

        :param buf: str - The received message.
        :return: None
        """
        if len(self.actions) == 0:
            recv_list = self.message.receive(buf, incantator=True)
        else:
            recv_list = self.message.receive(buf, self.actions, incantator=True)
        for recv_type, msgs in recv_list:
            if self.debug_mode:
                print(f'recv_type: {recv_type} and msgs: {msgs}')
            if recv_type == 'ok':
                if msgs[0] == 'Take' and msgs[1] == 'food':
                    self.life += self.FOOD
                if msgs[0] == 'Take' and msgs[1] == 'linemate':
                    self.have_linemate = True
                    self.goto_01()
                if msgs == 'Forward':
                    self.map[self.pos[0]][self.pos[1]] = 1
                    self.pos[0], self.pos[1] = self.npos((self.pos[0], self.pos[1]))
                    self.map[self.pos[0]][self.pos[1]] = 2
                if msgs == 'Right':
                    self.dir = (self.dir - 1) % 4
                if msgs == 'Left':
                    self.dir = (self.dir + 1) % 4
            elif recv_type == 'ko':
                # print(f'ko for incantator : {msgs}')
                if msgs == 'Incantation':
                    self.queue.append('Inventory')
                if isinstance(msgs, list) and msgs[0] == 'Take' and msgs[1] == 'food':
                    self.message.buf_messages('cibo opus est')
                    self.waiting_food = True
                    self.queue.append('Broadcast')
            elif recv_type == 'inventory':
                self.inventory = extract_inventory(msgs)
                self.life = self.inventory['food'] * self.FOOD
                # print(f'life incantator: {self.life}')
                # print(self)
            elif recv_type == 'look':
                if self.ready == False:
                    self.addapt_map(msgs) #TODO: @Cyprien: implement a real look, and only watch the case 0, put a condition of level up and if true call incantation
                                          #TODO: @Cyprien: if false, call the inventory
            elif recv_type == 'elevation':
                if self.debug_mode:
                    print('elevation: incant', msgs)
                if len(self.actions) > 0 and self.actions[0] == 'Incantation':
                    # print("take care of")
                    self.actions.pop(0)
                    continue
                # try:
                if msgs[-1] != 'y' and int(msgs[-1]) > 1:
                    self.level += 1
                    if self.level == 2:
                        # print('I am level 2, here, get out')
                        self.queue.append('Right')
                        self.queue.append('Right')
                        self.queue.append('Forward')
                        self.message.buf_messages(message='nobilis incantatio')
                        self.queue.append('Broadcast')
                        self.ready = True
                    self.queue.append(('Take', 'food'))
                    self.queue.append(('Take', 'food'))
                    self.queue.append(('Take', 'food'))
                    self.queue.append('Inventory')
                    self.queue.append('Incantation')
                # except Exception:
                    # pass
                # print(f'level: {self.level}')
                # print(f'queue: {self.queue}')
                # print(f'actions: {self.actions}')
                continue
            elif recv_type == 'broadcast':
                if msgs[0] == 'ko' or not msgs or isinstance(msgs, str):
                    continue
                for msg in msgs:
                    self.broadcast_traitement(msg)
                continue
            else:
                print("problems there")
                print(f"recv {recv_type}, msgs {msgs}")
            try:
                # if self.actions[0] != recv_type:
                #     print("recv", recv_type, "action", self.actions[0])
                self.actions.pop(0)
            except Exception as e:
                print(e)
                print(f'incatator recv_type: {recv_type} and msgs: {msgs} and buf {buf}')
            # self.actions.pop(0)

    def broadcast_traitement(self, message: tuple | str) -> None:
        if message['msg'] == 'facultates positas carmina':
            self.allowed_incantation_mns += 1
        if message['msg'] == 'movere ad : ':
            self.goto = message['infos']
        if message['msg'] == 'est dominus aquilonis':
            if self.path.facing is None:
                if self.dir is not None:
                    self.unset = False
                self.path.get_north(message['direction'])
                self.dir = self.path.facing
        if message['msg'] == 'motus sum':
            self.count_pos += 1

    def set_path_to_watch_linemate(self) -> None:
        """
        This method sets the path to the linemate.
        """
        pos = self.npos((self.pos[0], self.pos[1]))
        if self.debug_mode:
            print(f'pos: {pos}\nself.pos: {self.pos}\nself.map: {self.map}')
        if self.map[pos[0]][pos[1]] == 1:
            if pos[0] == self.pos[0]:
                if self.map[pos[0]][(self.pos[1] + 1) % self.limit[1]] == 0:
                    self.queue.append('Right')
                    self.queue.append('Look')
                    return
            else:
                if self.map[(self.pos[0] - 1) % self.limit[1] ][pos[1]] == 0:
                    self.queue.append('Right')
                    self.queue.append('Look')
                    return
            self.queue.append('Forward')
            self.queue.append('Look')
        else:
            self.queue.append('Look')

    def make_action(self) -> None:
        """
        This method makes the action of the incantator.
        """
        if len(self.queue) > 0 and len(self.actions) == 0:
            if self.queue[0] == 'Forward':
                self.comback.insert(0, 'Forward')
            if self.queue[0] == 'Right':
                self.comback.insert(0, 'Left')
            if self.queue[0] == 'Left':
                self.comback.insert(0, 'Right')
            self.apply_action()
            # print("the queue is", self.queue,
            #       "the action is :", self.actions)
        if len(self.actions) > 0 or self.dir is None:
            # if self.count % 100007 == 0:
            #     print(f"Incantator {self.level} alive")
            # self.count += 1
            return
        if self.first_round:
            # self.queue.append(('Set', 'food'))
            self.first_round = False
        if self.life <= 400:
            self.queue.append(('Take', 'food'))
            self.queue.append(('Take', 'food'))
            self.queue.append(('Take', 'food'))
            self.queue.append('Incantation') #TODO: @Cyprien: change the incantation to look
            return
        if self.dir == None:
            self.queue.append('Look')
            return
        if self.dir is not None and self.level < 2 and self.have_linemate == False and not self.ready:
            self.set_path_to_watch_linemate()
        if self.ready:
            if self.count_pos == 5:
                if self.have_linemate:
                    self.queue.append(('Set', 'linemate'))
                    self.queue.append('Incantation')
                    self.have_linemate = False
                else:
                    self.queue.append('Incantation') #TODO: @Cyprien: change the incantation to look
                self.ready = False
            else:
                self.queue.append('Inventory')
        if self.have_linemate and not self.ready:
            if self.unset:
                self.path.facing = None
                return
            self.queue.append('Look')
            self.turn_to_the_north()
            self.queue.append('Left')
            self.queue.append('Forward')
            self.ready = True
        if self.level >= 2:
            self.queue.append('Inventory')
            self.queue.append('Incantation') #TODO: @Cyprien: change the incantation to look
        # if self.allowed_incantation > self.level:
        #     self.queue.append('Incantation')
        # else:
        #     self.queue.append('Look')
            #TODO: commmunicate with the mastermind on the look
