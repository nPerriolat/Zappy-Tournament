from socket import socket
from random import randint

from ai.src.player.player import Player
from ai.src.gameplay.enum_gameplay import RoleInGame
from ai.src.player.progenitor import Progenitor
from ai.src.player.collector import Collector
from ai.src.player.incantator import Incantator
from ai.src.player.pnj import Pnj
from ai.src.player.north_guard import NorthGuard

class First_born(Player):

    ROLE = [
        RoleInGame.NORTH_GUARD,
        RoleInGame.PROGENITOR
    ]

    DEFAULT_ROLE = RoleInGame.PNJ

    BIND = {
        RoleInGame.PROGENITOR: [Progenitor, 'Progenitor'],
        RoleInGame.COLLECTOR: [Collector, 'Collector'],
        RoleInGame.INCANTATOR: [Incantator, 'Incantator'],
        RoleInGame.PNJ: [Pnj, 'Pnj'],
        RoleInGame.NORTH_GUARD: [NorthGuard, 'North guard']
    }

    def __init__(self, serv_info: list[int] | None = None, cli_socket: socket | None = None, debug_mode: bool = False):
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
        self.map = [[0 for _ in range(self.limit[0])] for _ in range(self.limit[1])]
        self.dir = 0
        self.pos = [0, 0]
        self.role = self.ROLE
        self.transformation = False
        self.serv_info = serv_info
        self.cli_socket = cli_socket
        self.debug_mode = debug_mode
        self.waiting_answer = False


    def change_role(self) -> None:
        self.message.buf_messages('Ego me transform : ', infos=[[self.BIND[self.role[0]][1]]])
        self.queue.append('Broadcast')
        self.transformation = True
    
    def who_are_you(self) -> None:
        self.message.buf_messages('Quis es')
        self.queue.append('Broadcast')
        for _ in range(7):
            self.queue.append('Look')
        self.waiting_answer = True

    def make_action(self) -> None:
        if len(self.queue) > 0 and len(self.actions) == 0:
            # if self.queue[0] == 'Newborn':
            #     self.queue.pop(0)
            #     self.who_are_you()
            self.apply_action()
        if len(self.actions) > 0:
            return
        self.queue.append('Forward')
        # if self.waiting_answer:
        #     self.death = self.INQUISITOR
        # else:
        #     self.queue.append('Look')

    def goto_reborn(self, i: int) -> None:
        if i != 0:
            self.queue.append('Forward')
        if i == 1:
            self.queue.append('Left')
            self.queue.append('Forward')
        elif i == 3:
            self.queue.append('Right')
            self.queue.append('Forward')
        self.queue.append('Newborn')
    
    def update_map(self, vision: str) -> bool:
        vi = vision.replace('[ ', '').replace(' ]', '')
        list_vision = vi.split(',')
        for i in range(len(list_vision)):
            case = list_vision[i].split(' ')
            if case.count('egg') > 2 and case.count('player') >= 1:
                self.goto_reborn(i)
                return False
            horizontal = i - i * (i + 1)
            vertical = int(i ** 0.5)
            if self.dir == 0:
                x = (self.pos[0] + horizontal) % self.limit[0]
                y = (self.pos[1] + vertical) % self.limit[1]
            elif self.dir == 1:
                x = (self.pos[0] + vertical) % self.limit[0]
                y = (self.pos[1] - horizontal) % self.limit[1]
            elif self.dir == 2:
                x = (self.pos[0] - horizontal) % self.limit[0]
                y = (self.pos[1] - vertical) % self.limit[1]
            else:
                x = (self.pos[0] - vertical) % self.limit[0]
                y = (self.pos[1] + horizontal) % self.limit[1]
            self.map[x][y] = 1
        return True

    def adaptativ_walk(self, i, j) -> None | tuple[int, int]:
        result_x = self.pos[0] + i
        result_y = self.pos[1] + j
        if self.dir == 1:
            result_x = self.pos[0] + j
            result_y = self.pos[1] - i
        elif self.dir == 2:
            result_x = self.pos[0] - i
            result_y = self.pos[1] - j
        elif self.dir == 3:
            result_x = self.pos[0] - j
            result_y = self.pos[1] + i
        if self.map[result_x % self.limit[0]][result_y % self.limit[1]] == 1:
            return None
        return [result_x % self.limit[0], result_y % self.limit[1]]

    def goto(self, rd: int) -> None:
        if rd != 1 and rd != 4:
            self.queue.append('Forward')
            if rd != 0 or rd != 6:
                self.queue.append('Forward')
        if rd < 3:
            self.queue.append('Right')
        elif rd > 3:
            self.queue.append('Left')
        if rd != 3:
            self.queue.append('Forward')
            if rd == 0 or rd == 6:
                self.queue.append('Forward')

    def update_actions(self) -> None:
        action = []
        x = self.pos[0]
        y = self.pos[1]
        if self.dir % 2 == 1:
            x = self.pos[1]
            y = self.pos[0]
        for i in range(-2, 2):
            if i % 2 == 0 and i != 0:
                action.append(self.adaptativ_walk(i, 1))
            if i % 2 == 1:
                action.append(self.adaptativ_walk(i, 0))
            if -1 <= i <= 1:
                action.append(self.adaptativ_walk(i, 2))
                action.append(self.adaptativ_walk(i, 2))
        action.append((self.pos[0], self.pos[1]))

        if all(element is None for element in action):
            self.queue.append('Forward')
            self.queue.append('Forward')
            self.queue.append('Forward')
            rd = randint(0, 2)
            if rd == 0:
                self.queue.append('Right')
                self.queue.append('Forward')
            if rd == 2:
                self.queue.append('Left')
                self.queue.append('Forward')
        else:
            rd = randint(0, len(action) - action.count(None) - 1)
            self.goto(rd)        

    # def recv_treatment(self, buf: str) -> None:
    #     if len(self.actions) == 0:
    #         recv_list = self.message.receive(buf)
    #     else:
    #         recv_list = self.message.receive(buf, self.actions)
    #     for recv_type, msgs in recv_list:
    #         if recv_type == 'look':
    #             if self.update_map(msgs):
    #                 self.update_actions()
    #         elif recv_type == 'ok':
    #             if msgs == 'Forward':
    #                 if self.dir == 0:
    #                     self.pos[0] = (self.pos[0] + 1) % self.limit[0]
    #                 elif self.dir == 1:
    #                     self.pos[1] = (self.pos[1] + 1) % self.limit[1]
    #                 elif self.dir == 2:
    #                     self.pos[0] = (self.pos[0] - 1) % self.limit[0]
    #                 else:
    #                     self.pos[1] = (self.pos[1] - 1) % self.limit[1]
    #             if msgs == 'Left':
    #                 self.dir = (self.dir + 1) % 4
    #             if msgs == 'Right':
    #                 self.dir = (self.dir - 1) % 4
    #             if msgs == 'Broadcast':
    #                 if self.transformation:
    #                     if len(self.role) > 0:
    #                         self.death = self.role[0]
    #                     else:
    #                         self.death = self.DEFAULT_ROLE
    #         elif recv_type == 'eject':
    #             continue
    #         elif recv_type == 'broadcast':
    #             if msgs[0] == 'ko':
    #                 continue
    #             for msg in msgs:
    #                 self.broadcast_traitement(msg)
    #             continue
    #         self.actions.pop(0)

    def broadcast_traitement(self, msg: dict[str, str] | str | tuple) -> None:
        if msg['msg'] == 'Ego me transform : ':
            if msg['infos'] is not self.BIND[self.DEFAULT_ROLE][1]:
                self.role.pop(0)
        if msg['msg'] == 'est dominus aquilonis':
            if len(self.role) > 0 and self.role[0] == RoleInGame.NORTH_GUARD:
                self.role.pop(0)
        if self.waiting_answer and msg['msg'] == 'Ego sum dominus tuus' and msg['direction'] == 0:
            self.queue = []
            self.change_role()
        if self.waiting_answer and msg['msg'] == 'Ego sum dominus tuus' and msg['direction'] != 0:
            self.queue = []
            self.death = RoleInGame.INQUISITOR

