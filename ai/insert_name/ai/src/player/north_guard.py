from socket import socket
from abc import ABC
from re import match

from ai.src.player.player import Player
from ai.src.mvt import path
from ai.src.utils.messages import extract_inventory


class NorthGuard(Player):

    def __init__(self,
                 serv_info: list[int] | None = None,
                 cli_socket: socket | None = None,
                 debug_mode: bool = False):
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
        self.exist_north: bool = False
        self.said: bool = False
        self.in_pos: bool = False
        self.count = 0

    def say_the_north(self):
        """

        """
        if self.eject_security is False:
            self.eject_security = True
        self.message.buf_messages(message='est dominus aquilonis')
        self.queue.append('Broadcast')

    def take_the_pole(self) -> None:
        self.eject_security = False
        self.queue.append('Forward')
        self.queue.append('Forward')
        self.queue.append('Forward')
        self.queue.append('Forward')
        self.life -= self.ACTION * 4
        self.exist_north = True
        self.in_pos = True
        self.path.facing = 0

    def broadcast_traitement(self, message: tuple | str) -> None:
        if message['msg'] == 'est dominus aquilonis' and self.exist_north is True:
            if self.path.facing is None:
                self.path.get_north(message['direction'])
                self.turn_to_the_north()
                self.take_the_pole()
        self.global_message(message)

    def make_action(self) -> None:
        """

        """
        if len(self.queue) > 0 and len(self.actions) < 1:
            # if self.queue[0] == 'Forward':
                # print(f'action North: {self.actions}')
                # print(f'queue North: {self.queue}')
            self.apply_action()
        if len(self.actions) > 0:
            return
        if (self.exist_north is False and self.path.facing is None) and self.in_pos is False:
            self.take_the_pole()
        elif self.exist_north is True and self.path.facing is None:
            self.queue.append('Look')
            self.queue.append('Inventory')
        elif self.life < 260 and self.said is False:
            self.message.buf_messages(message='Ego plus viribus')
            self.queue.insert(0, 'Broadcast')
            # print("je suis faible")
            self.said = True
        else:
            self.say_the_north()
            self.life -= self.ACTION


class ViceNorthGuard(Player):

    def __init__(self,
                 serv_info: list[int] | None = None,
                 cli_socket: socket | None = None,
                 debug_mode: bool = False,):
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
        self.exist_north: bool = True
        self.said: bool = False
        self.in_pos: bool = False
        self.count = 0

    def say_the_north(self):
        """

        """
        if self.eject_security is False:
            self.eject_security = True
        self.message.buf_messages(message='est dominus aquilonis')
        self.queue.append('Broadcast')

    def take_the_pole(self) -> None:
        self.eject_security = False
        self.queue.append('Forward')
        self.queue.append('Forward')
        self.queue.append('Forward')
        self.queue.append('Forward')
        self.life -= self.ACTION * 4
        self.exist_north = True
        self.in_pos = True
        self.path.facing = 0

    def broadcast_traitement(self, message: tuple | str) -> None:
        if message['msg'] == 'est dominus aquilonis' and self.exist_north is True:
            if self.path.facing is None:
                self.path.get_north(message['direction'])
                self.turn_to_the_north()
                self.take_the_pole()
        self.global_message(message)

    def make_action(self) -> None:
        """

        """
        if len(self.queue) > 0 and len(self.actions) < 1:
            # if self.queue[0] == 'Forward':
                # print(f'action North: {self.actions}')
                # print(f'queue North: {self.queue}')
            self.apply_action()
        if len(self.actions) > 0:
            return
        if (self.exist_north is False and self.path.facing is None) and self.in_pos is False:
            self.take_the_pole()
        elif self.exist_north is True and self.path.facing is None:
            self.queue.append('Look')
            self.queue.append('Inventory')
        elif self.life < 260 and self.said is False:
            self.message.buf_messages(message='Ego plus viribus')
            self.queue.insert(0, 'Broadcast')
            # print("je suis faible")
            self.said = True
        else:
            self.say_the_north()
            self.life -= self.ACTION