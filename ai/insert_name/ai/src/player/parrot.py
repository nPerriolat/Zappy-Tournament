from socket import socket
from abc import ABC

from ai.src.player.player import Player
from ai.src.communication.messages import Messages


class Parrot(Player):
    """
    The Parrot class represents a player character in the game.
    The Parrot repeat every message he eared.
    """

    def __init__(self, serv_info: list[int] | None = None, cli_socket: socket | None = None, debug_mode: bool = False):
        if serv_info is not None:
            super().__init__(serv_info, cli_socket, debug_mode)
            self.message = Messages(self.cipher, self.cli_num, self.language, parrot=True)
            self.empty_broadcast()

    def empty_broadcast(self) -> None:
        """
        This method send an empty message to test the robustness of opposing teams
        :return: None
        """
        self.message.msg = 'Broadcast "'
        self.queue.append('Broadcast')
        self.life -= self.ACTION

    def repeat(self, msg: str, delay: int = 0) -> None:
        """
        This method send the same message as received
        :param msg: str - The message to be repeated.
        :param delay: int - The delay before repeating the message (default is 0).
        :return: None
        """
        for _ in range(delay):
            self.queue.append(('Take', 'player'))
            self.life -= self.ACTION
        self.message.msg += msg
        self.queue.append('Broadcast')

    def make_action(self) -> None:
        if len(self.actions) >= 1 or len(self.queue) > 6:
            return
        if 0 < len(self.queue) and len(self.actions) < 1:
            self.apply_action()

    def broadcast_traitement(self, msg: tuple | str) -> None:
        if msg:
            self.repeat(msg, 1)
