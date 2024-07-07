from socket import socket

from ai.src.player.player import Player
from ai.src.mvt.path import Path
from ai.src.mvt.tsp import Held_krap
from ai.src.gameplay.evolution import evolution
from ai.src.gameplay.enum_gameplay import Ressources as res
from ai.src.gameplay.utils import is_all_val0
from ai.src.gameplay.enum_gameplay import Directions as dir
import select

class Role(Player):

    def __init__(self, serv_info: list[int] | None = None, cli_socket: socket | None = None, debug_mode: bool = False):
        """
        This class is the role of the player.

        :param serv_info: list[int] - Information about the server.
        :param cli_socket: socket - The client socket for communication.
        :param debug: bool - The debug mode.
        """
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
        self.level = 1
        self.goal = evolution()
        self.mvt = Held_krap(self.limit, self.pos)
        self.vitals = {'food': 1}
        self.viewed = False
        self.is_watching = False
        self.update_actions = False
        self.allow_action = False
        self.dir = None

    def set_goal(self) -> None:
        """
        This method sets the goal of the player.

        :return: None
        """
        self.goal = evolution(self.level)
        self.mvt = Held_krap(self.limit, self.pos)

    def check_goals(self) -> bool:
        """
        This method checks if the player has reached its main goals.

        :return: bool - True if the player has reached its main goals, False otherwise.
        """
        for ele in self.goal.keys():
            if ele in self.inv and self.inv[ele] >= self.goal[ele]:
                return True
        return False

    def update_goals(self) -> None:
        """
        This method updates the goals of the player when it is necessary.
        
        :return: None
        """
        if self.life < 300:
            #TODO: change goals for vital needs
            i=1
        if self.check_goals():
            self.actions = [Path(self.limit, self.pos, (0, 0)).opti_path()[0]]
            self.incantation()

    def strategy(self) -> None:
        """
        This method is the strategy of the ai.
        
        :return: None
        """
        actions = Held_krap(self.limit, self.pos).algo(self.map_knowledge)
        for ele in actions:
            if type(ele) == list:
                if type(ele[0]) == tuple:
                    for elem in ele:
                        self.queue.append(elem)
            else:
                self.queue.append(ele)
                

    def empty_queue(self) -> None:
        """
        This method empties the queue of actions.
        """
        self.look_around()
    
    def actions_update(self) -> None:
        """
        This method updates the actions done by the player.
        
        :return: None
        """
        if len(self.queue) == 0:
            return
        if self.queue[0] == 'Forward\n':
            if self.dir == dir.NORTH:
                self.pos = (self.pos[0] + 1, self.pos[1])
            elif self.dir == dir.SOUTH:
                self.pos = (self.pos[0] - 1, self.pos[1])
            elif self.dir == dir.EAST:
                self.pos = (self.pos[0], self.pos[1] + 1)
            elif self.dir == dir.WEST:
                self.pos = (self.pos[0], self.pos[1] - 1)
        if self.queue[0] == 'Right\n':
            self.dir = (self.dir + 1) % 4
        if self.queue[0] == 'Left\n':
            self.dir = (self.dir - 1) % 4
        if self.queue[0].__contains__('Take'):
            self.queue[0] = self.queue[0].removesuffix('Take ')
            if self.queue[0] not in self.inv:
                self.inv[self.queue[0]] = 0
            self.inv[self.queue[0]] += 1
        if self.queue[0] == 'Death\n':
            self.level = 8
        if self.queue[0] == 'Elevation\n':
            self.level += 1
            self.set_goal()


    def run(self) -> None:
        """
        This method is the main loop of the ai.

        :return: None
        """
        while self.level < 8:
            infds, outfds, errfds = select.select(self.inout, self.inout, [])

            """
            infds: list[socket] - The list of sockets to read from.
            """
            if len(infds) != 0:
                buf = self.recv_action()
                #TODO: check if the player is dead or if he receved a broadcast or other msg
                if buf == 'ok\n':
                    self.actions_update()
                    self.update_goals()
                elif len(buf) != 0 and buf != 'ko\n':
                    self.update_map(buf, self.dir)
                    self.viewed = True
                    self.is_watching = False
                if len(self.actions) >= 9:
                    self.allow_action = True
                self.actions.pop(0)

            """
            outfds: list[socket] - The list of sockets to write to.
            """
            if len(outfds) != 0 and len(self.actions) < 9:
                if self.viewed:
                    self.viewed = False
                    self.strategy()
                    self.allow_action = True
                if len(self.queue) != 0 and len(self.actions) != len(self.queue):
                    self.actions.append(self.queue[0])
                    self.allow_action = True
                    self.queue.pop(0)
                if len(self.actions) != 0 and self.allow_action:
                    self.apply_action()
                    self.allow_action = False
                if len(self.queue) == 0 and len(self.actions) == 0:
                    self.empty_queue()
                # print(f"actions: {len(self.actions)}")
                # print(f"actions: {self.actions}")
                # print(f"queue: {len(self.queue)}")

