from socket import socket

from ai.src.player.player import Player


class Progenitor(Player):

    def __init__(self, serv_info: list[int] | None = None, cli_socket: socket | None = None, debug_mode: bool = False):
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
        self.need_eat = 0
        self.pos = (0, 0)
        self.the_place_to_be = (0, 0)
        self.nbr_of_child_to_create = -1
    
    def make_action(self) -> None:
        if len(self.queue) > 0:
            self.apply_action()
        if len(self.actions) > 2:
            return
        if self.life <= self.INCANTATION + self.FORK:
            self.queue.append(('Take', 'food'))
        else:
            if self.nbr_of_child_to_create > 0 or self.nbr_of_child_to_create == -1:
                self.queue.append('Fork')
                if self.nbr_of_child_to_create != -1:
                    self.nbr_of_child_to_create -= 1
    
    def broadcast_traitement(self, message: tuple | str) -> None:
        self.global_message(message)
