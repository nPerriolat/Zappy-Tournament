import os
from random import randint

from collections import Counter

from ai.src.gameplay.evolution import EVOLUTION_RESOURCES
from ai.src.player.parrot import Parrot
from ai.src.player.progenitor import Progenitor
from ai.src.player.collector import Collector
from ai.src.player.incantator import Incantator
from ai.src.player.player import Player
from ai.src.player.pnj import Pnj
from ai.src.player.first_born import First_born
from ai.src.player.north_guard import NorthGuard, ViceNorthGuard
from ai.src.player.hansel import Hansel
from ai.src.player.pusher import Pusher, VicePusher, Spartiate
from ai.src.utils.messages import extract_inventory
from ai.src.utils.info_look import look_resources
from ai.src.zappy_ai import connection
from socket import socket
from ai.src.gameplay.enum_gameplay import RoleInGame, FOCUS

class ParentAI(Player):

    ROLE = [
            RoleInGame.PROGENITOR,
            RoleInGame.PROGENITOR,
            RoleInGame.PROGENITOR,
            RoleInGame.NORTH_GUARD,
            RoleInGame.INCANTATOR,
            RoleInGame.PNJ,
            RoleInGame.PNJ,
            RoleInGame.PNJ,
            RoleInGame.PNJ,
            RoleInGame.PNJ,
            RoleInGame.HANSEL,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            # RoleInGame.PUSHER,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            # RoleInGame.PUSHER,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            # RoleInGame.PUSHER,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            # RoleInGame.PUSHER,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            RoleInGame.COLLECTOR,
            RoleInGame.HANSEL,
            # TODO - stop la list ici
            # RoleInGame.HANSEL,
            # RoleInGame.HANSEL,
            # RoleInGame.PUSHER,
            # RoleInGame.COOCKER,
            # RoleInGame.COLLECTOR,
            # RoleInGame.COLLECTOR,
            # RoleInGame.COLLECTOR,
            # RoleInGame.COLLECTOR,
            ]
    DEFAULT_ROLE = [
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    # RoleInGame.COLLECTOR,
                    RoleInGame.HANSEL,
                    RoleInGame.HANSEL,
                    RoleInGame.INCANTATOR,
                    RoleInGame.PNJ,
                    RoleInGame.PNJ,
                    RoleInGame.PNJ,
                    RoleInGame.PNJ,
                    RoleInGame.PNJ,

                    ]
    
    DEFENDER_ROLE = [
                    RoleInGame.SPARTIATE,
                    RoleInGame.HANSEL,
                    RoleInGame.SPARTIATE,
                    RoleInGame.HANSEL,
                    ]

    BIND = {
        RoleInGame.PROGENITOR: Progenitor,
        RoleInGame.COLLECTOR: Collector,
        RoleInGame.INCANTATOR: Incantator,
        RoleInGame.NORTH_GUARD: NorthGuard,
        RoleInGame.PNJ: Pnj,
        RoleInGame.FIRST_BORN: First_born,
        RoleInGame.HANSEL: Hansel,
        RoleInGame.PUSHER: Pusher,
        RoleInGame.VICE_NORTH_GUARD: ViceNorthGuard,
        RoleInGame.VICE_PUSHER: VicePusher,
        RoleInGame.SPARTIATE: Spartiate,
        RoleInGame.PARROT: Parrot
    }



    def __init__(self, serv_info: list[int], cli_socket: socket, debug_mode: bool = False,
                 machine: str = None, port: str = None, name: str = None):
        super().__init__(serv_info, cli_socket, debug_mode)
        self.serv_info = serv_info
        self.cli_socket = cli_socket
        self.debug_mode = debug_mode
        self.id: int = 0
        self.counter = self.INCUBATION_TIME
        self.gave_birth = 0
        self.role = RoleInGame.PROGENITOR
        self.machine = machine
        self.port = port
        self.name = name
        self.first_round = [True, True]
        self.index = 0
        self.give_role = []
        self.can_incant = False
        self.level_to_give = 1
        self.fork_gave = 0
        self.coll_ressources = {}
        self.level_incant = 1
        self.global_ressources = self.based_ressources
        self.new_focus = False
        self.ressources_focus = {}
        self.allow_incantation = False
        self.in_depot: int = -1
        self.exist_north = False
        self.pusher_count = 1
        self.second_phase = False
        self.spoke: bool = False
        self.legione_honoris: bool = False
        self.legione_prima: bool = False
        self.legione_secunda: bool = False
        self.legione_tertia: bool = False
        self.level_resources: int = 0

    def get_role(self, serv_info: list[int], cli_socket: socket):
        role = 0
        if self.first_round[1]:
            role = RoleInGame.FIRST_BORN.value
        elif len(self.give_role) > 0:
            role = self.give_role[0].value
        elif self.second_phase:
            role = self.DEFENDER_ROLE[self.index % len(self.DEFENDER_ROLE)].value
        else:
            role = self.DEFAULT_ROLE[self.index % len(self.DEFAULT_ROLE)].value
        return role

    def fork(self, role, cli_socket: socket, serv_info: list[int]) -> None:
        match role:
            case 0: role = Progenitor(serv_info, cli_socket, self.debug_mode)
            case 1: role = Incantator(serv_info, cli_socket, self.debug_mode)
            case 2: role = Collector(serv_info, cli_socket, self.debug_mode)
            case 3: role = Pusher(serv_info, cli_socket, self.debug_mode)
            case 4: role = Pnj(serv_info, cli_socket, self.debug_mode)
            case 5: role = First_born(serv_info, cli_socket, self.debug_mode)
            case 6: role = NorthGuard(serv_info, cli_socket, self.debug_mode)
            case 7: role = Hansel(serv_info, cli_socket, self.debug_mode)
            case 8: role = ViceNorthGuard(serv_info, cli_socket, self.debug_mode)
            case 10: role = VicePusher(serv_info, cli_socket, self.debug_mode)
            case 11: role = Spartiate(serv_info, cli_socket, self.debug_mode)
            case 12: role = Parrot(serv_info, cli_socket, self.debug_mode)
            case _: print("DEFAULT CASE")
        while role is not None:
            role = role.run()
        cli_socket.close()
        exit(0)

    def real_fork(self) -> bool:
        serv_info, cli_socket = connection(self.port, self.name, self.machine)
        if serv_info is None or cli_socket is None:
            cli_socket.close()
            return False
        self.index = (self.index + 1)
        pid = os.fork()
        if pid == 0:
            self.fork(self.get_role(serv_info, cli_socket), cli_socket, serv_info)
        elif pid == -1:
            cli_socket.close()
            print('error')
        if len(self.give_role) > 0 and self.give_role[0] == RoleInGame.NORTH_GUARD:
            self.exist_north = True
        if len(self.give_role) != 0 and self.give_role[0] == RoleInGame.VICE_PUSHER:
            my_id_0 = None
            my_id_1 = None
            my_id_2 = None
            my_id_3 = None
            if self.legione_honoris is True:
                my_id_0 = 0
                self.legione_honoris = False
            if self.legione_prima is True:
                my_id_1 = 1
                self.legione_prima = False
            if self.legione_secunda is True:
                my_id_2 = 2
                self.legione_secunda = False
            if self.legione_tertia is True:
                my_id_3 = 3
                self.legione_tertia = False
            if my_id_0 is not None:
                self.message.buf_messages('occupat exercitum : ', my_id=my_id_0)
                self.queue.insert(0, 'Broadcast')
            if my_id_1 is not None:
                self.message.buf_messages('occupat exercitum : ', my_id=my_id_1)
                self.queue.insert(0, 'Broadcast')
            if my_id_2 is not None:
                self.message.buf_messages('occupat exercitum : ', my_id=my_id_2)
                self.queue.insert(0, 'Broadcast')
            if my_id_3 is not None:
                self.message.buf_messages('occupat exercitum : ', my_id=my_id_3)
                self.queue.insert(0, 'Broadcast')
        return True

    def real_fork_addaptativ(self) -> None:
        if len(self.give_role) == 0:
            self.index = (self.index + 1) % len(self.DEFAULT_ROLE)
            return self.DEFAULT_ROLE[self.index]
    
    def count_element(self, resources: list) -> None:
        my_resources = dict(Counter(resources))
        for need in self.need_ressources.keys():
            if need not in my_resources or my_resources[need] < self.need_ressources[need]:
                return
        self.second_phase = True

    def slot_treatment(self, msgs: str) -> None:
        for _ in range(msgs):
            if msgs != 0:
                has_forked = self.real_fork()
                if len(self.give_role) > 0 and has_forked:
                    self.give_role.pop(0)

    def mastermind_treatment(self, buf) -> None:
        """"
        mastermind treatment informations

        :return false: if he received a broadcast
        :return None
        """
        if len(self.actions) == 0:
            recv_list = self.message.receive(buf)
        else:
            recv_list = self.message.receive(buf, self.actions)
        for recv_type, msgs in recv_list:
            if recv_type == 'slots':
                self.slot_treatment(msgs)
            elif recv_type == 'ok':
                if msgs[0] == 'Take' and msgs[1] == 'food':
                    pass
            elif recv_type == 'broadcast':
                if msgs is None or msgs[0] == 'ko' or isinstance(msgs, str):
                    continue
                for msg in msgs:
                    self.broadcast_traitement(msg)
                continue
            elif recv_type == 'look':
                if self.second_phase is False:
                    self.count_element(look_resources(msgs, FOCUS)[0])
            elif recv_type == 'ko':
                pass
            elif recv_type == 'eject':
                continue
            elif recv_type == 'inventory':
                self.inventory = extract_inventory(msgs)
                self.life = self.inventory['food'] * self.FOOD
                if self.debug_mode:
                    print("inventory")
            else:
                print(f"mmS  PBs: rec {recv_type}, msgs {msgs}, Buff {buf}")
            self.actions.pop(0)

    def broadcast_traitement(self, message: tuple | str | dict) -> None:
        if message['msg'] == 'opes in meo inventario sunt : ':
            if message['id'] not in self.coll_ressources.keys():
                self.coll_ressources[message['id']] = self.based_ressources
            for keys, nbrs in zip(message['info'], message['nbr']):
                self.coll_ressources[message['id']][keys] = nbrs
                self.global_ressources[keys] += nbrs
        if message['msg'] == 'Ego plus viribus':
            self.give_role.insert(0, RoleInGame.VICE_NORTH_GUARD)
        if message['msg'] == 'opes deposita':
            for keys, nbrs in zip(message['info'], message['nbr']):
                self.global_ressources[keys] -= nbrs
                self.ressources_focus[keys] -= nbrs
            if any(item <= 0 for item in self.ressources_focus.values()):
                self.new_focus = True
                self.message.buf_messages('facultates positas carmina')
        if message['msg'] == 'defecit carmen':
            #TODO: problem to make the incantation
            pass
        if message['msg'] == 'Quis es':
            self.message.buf_messages('Ego sum dominus tuus')
            self.queue.insert(0, 'Broadcast')
        if message['msg'] == 'felix carmen':
            self.level_incant += 1
            self.level_resources += 1
            self.update_needed()
        if message['msg'] == 'situm intrare':
            self.enter_depot()
        if message['msg'] == 'sum extra domum':
            self.exit_depot()
        if message['msg'] == 'Dimissus a Legione Honoris':
            self.legione_honoris = True
        elif message['msg'] == 'Dimissus a legione prima':
            self.legione_prima = True
            self.give_role.insert(0, RoleInGame.VICE_PUSHER)
        elif message['msg'] == 'Dimissus a legione secunda':
            self.legione_secunda = True
            self.give_role.insert(0, RoleInGame.VICE_PUSHER)
        elif message['msg'] == 'Dimissus a legione tertia':
            self.legione_tertia = True
            self.give_role.insert(0, RoleInGame.VICE_PUSHER)
        if message['msg'] == 'pugnae consilia' and self.pusher_count < 25:
            self.satus_testudo()

    def enter_depot(self) -> None:
        """

        :return:
        """
        if self.in_depot == -1:
            self.in_depot = 0
        self.in_depot += 1

    def exit_depot(self) -> None:
        """

        :return:
        """
        if self.in_depot == -1:
            return
        self.in_depot -= 1
        if self.in_depot == 0:
            self.message.buf_messages(message='Non Potes dominum facti')
            self.queue.append('Broadcast')
            self.life -= self.ACTION
            self.in_depot = -1

    def progenitor_treatment(self, buf: str) -> None:
        if len(self.actions) == 0:
            recv_list = self.message.receive(buf)
        else:
            recv_list = self.message.receive(buf, self.actions)
        for recv_type, msgs in recv_list:
            if recv_type == 'eject':
                continue
            if recv_type == 'slots':
                self.slot_treatment(msgs)
                if self.first_round[1]:
                    self.first_round[1] = False
                    self.give_role = self.ROLE
            elif recv_type == 'broadcast':
                if msgs[0] == 'ko':
                    continue
                for msg in msgs:
                    self.broadcast_traitement(msg)
                continue
            self.actions.pop(0)

    def recv_treatment(self, buf: str) -> None:
        if self.role == RoleInGame.PROGENITOR:
            if not self.progenitor_treatment(buf):
                return
        elif self.role == RoleInGame.MASTERMIND:
            if not self.mastermind_treatment(buf):
                return

    def action_as_progenitor(self) -> None:
        """
        This is being used when parent_ai is a progenitor
        """
        self.queue.append('Fork')
        if self.counter > 0:
            self.counter -= self.FORK_ACTION
        if self.counter <= 0:
            self.queue.append('Slots')
            self.fork_gave += 1
        if self.fork_gave == 1:
            self.role = RoleInGame.MASTERMIND

    def communicate_orders(self) -> bool:
        """
        This method communicates the orders to the mastermind.
        """
        #TODO: implement the communication between the mastermind and the putas

        if self.allow_incantation:
            self.message.buf_messages('facultates positas carmina')
            self.queue.append('Broadcast')
            self.allow_incantation = False
            return True
        if self.level_to_give == self.level_incant and self.new_focus:
            self.message.buf_messages('quid habes ut nobis offerat')
            self.queue.append('Broadcast')
            self.level_to_give += 1
            self.new_focus = False
            return True
        return False

    def action_as_mastermind(self) -> None:
        """
        This is being used when parent_ai is a mastermind
        """
        if self.life <= 400:
            self.queue.append(('Take', 'food'))
            self.queue.append('Inventory')
        elif not self.communicate_orders():
            self.queue.append('Inventory')
            self.queue.append('Look')
        self.queue.append('Slots')

    def make_action(self) -> None:
        """
        This method makes the action of the player.
        """
        # if self.cli_num != len(self.mms):
        #     return
        if self.first_round[0]:
            # self.mms.append(randint(0, 100_000_000))
            # self.message.buf_messages('auxilium postulo', my_id=self.mms[0])
            self.queue.append('Slots')
            # self.queue.append('Broadcast')
            # self.spoke = True
            self.first_round[0] = False
            self.apply_action()
        if self.first_round[1]:
            return
        # if self.mms_start:
        #     self.mms_start = False
        #     self.queue.append('Slots')
        #     self.apply_action()
        #     return
        # if len(self.mms) <= self.cli_num:
        #     if len(self.queue) > 0:
        #         self.apply_action()
        #     return
        # if self.spoke:
        #     self.spoke = False
        #     self.mms = self.mms.sort()
        #     if self.mms[0] != self.mms_id:
        #         Pnj(self.serv_info, self.cli_socket, self.debug_mode).run()
        #         exit(0)
        #     return
        if self.role == RoleInGame.PROGENITOR:
            if len(self.queue) > 0:
                self.apply_action()
            if len(self.actions) > 0:
                return
            self.action_as_progenitor()
        elif self.role == RoleInGame.MASTERMIND:
            if len(self.queue) > 0 and len(self.actions) == 0:
                self.apply_action()
            if len(self.actions) > 0:
                return
            self.action_as_mastermind()

    def get_broadcast(self, broadcast_recv: str):
        print(broadcast_recv)

    def satus_testudo(self) -> None:
        self.message.buf_messages('satus testudo : ', my_id=self.pusher_count)
        self.queue.append('Broadcast')
        self.pusher_count += 1

    def update_needed(self) -> None:
        result = {key: self.need_ressources[key] - EVOLUTION_RESOURCES[self.level_resources - 1].get(key, 0)
                  for key in self.need_ressources.keys()}
        self.need_ressources = result
