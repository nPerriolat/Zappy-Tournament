#!/usr/bin/python3
import socket
import sys

import socket
import time
import select
from abc import abstractmethod

from ai.src.server import connexion
from ai.src.communication import cipher, messages, latin


class Bot(object):
    """
    The Bot class is designed to interact with a server by sending specific action commands and managing the bot's state based on server information.
    """
    INCANTATION = 300
    FORK = 42
    INVENTORY = 1
    ACTION = 7
    FOOD = 126

    def __init__(self, serv_info: list[int], cli_socket: socket, debug_mode: bool = False):
        """
        Initialize the Bot object with the client number and dimensions.

        Parameters:
        - serv_info: list[int] - Information about the server.
        - cli_socket: socket - The client socket for communication.

        This method initializes the Bot object with the provided client number and dimensions.
        """
        self.cli_num = serv_info[0]
        self.dimensions = serv_info[1:]
        self.cli_socket = cli_socket
        self.debug_mode = debug_mode
        self.inout = [cli_socket]
        self.cipher = cipher.Cipher("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum posuere leo eget iaculis bibendu") #m. Donec fringilla lectus et imperdiet hendrerit. Morbi eget risus volutpat, tincidunt tellus quis, maximus augue. Proin ac hendrerit mauris. Sed egestas sapien ac tellus sagittis laoreet. Cras sed pretium erat. Etiam ac aliquet ante. Vivamus ornare tellus quis ante eleifend, egestas fringilla velit suscipit. Nulla sollicitudin, erat non eleifend lobortis, lacus tortor luctus mi, at volutpat neque arcu facilisis dolor. Pellentesque eros sapien, dapibus eget mauris at, rhoncus gravida odio. Integer viverra velit eu mi tincidunt efficitur. Aenean vitae sem ipsum. Integer quam nibh, semper eu venenatis a, egestas et sem.")
        self.language = latin.Latin()
        self.message = messages.Messages(self.cipher, self.cli_num, self.language)
        self.life = 10 * self.FOOD
        if self.debug_mode:
            print(self.cli_num)
            print(self.dimensions)
            print(self.cli_socket)

    def send_action(self, action: str) -> None:
        """
        Send an action command to the server.

        :param action: The action command to be sent after validation.
        :return: None
        """
        if self.debug_mode:
            print(f"Sending action: {action}")
        self.cli_socket.send(action.encode())

    def recv_action(self) -> str:
        """
        Receive an action command from the server.

        :return: str - The received action command from the server.
        """
        try:
            rec: str = self.cli_socket.recv(100_000).decode()
        except Exception:
            # print("Server disconnected")
            self.cli_socket.close()
            sys.exit(0)
        if self.debug_mode:
            print(f"Received action: {rec}")
        # if rec == "" or rec == "dead\n":
        # TODO - test avoid suicide
        if rec == "dead\n" or rec == "":
            # print("Server disconnected")
            self.cli_socket.close()
            sys.exit(0)

        return rec

    def forward(self) -> None:
        """
        Sends a 'Forward' command to the server to move up one tile.
        :return: None
        """
        self.life -= self.ACTION
        self.send_action("Forward\n")

    def right(self) -> None:
        """
        Sends a 'Right' command to the server to move the bot to turn 90° right.

        :return: None
        """
        self.life -= self.ACTION
        self.send_action("Right\n")

    def left(self) -> None:
        """
        Sends a 'Left' command to the server to move the bot to turn 90° left.

        :return: None
        """
        self.life -= self.ACTION
        self.send_action("Left\n")

    def look_around(self) -> None:
        """
        Send a 'Look' command to look around.

        :return: None
        """
        self.life -= self.ACTION
        self.send_action("Look\n")

    def check_inventory(self) -> None:
        """
        Send a 'Inventory' command to check the inventory.

        :return: None
        """
        self.life -= self.INVENTORY
        self.send_action("Inventory\n")

    def broadcast(self) -> None:
        """
         Send a broadcast message to all bots.

         :return: None
         """
        self.life -= self.ACTION
        self.send_action(f'{self.message.send_buf()}\n')
        if self.debug_mode:
            print('message send')

    def broadcast_bis(self) -> None:
        """
         Send a broadcast message to all bots.

         :return: None
         """
        self.life -= self.ACTION
        self.send_action(f'{self.message.send_buf_bis()}\n')
        if self.debug_mode:
            print('message send')

    def nbr_of_slot(self) -> None:
        """
        Send a 'Connect_nbr' command to check the number of team unused slots.

        :return: None
        """
        self.send_action("Connect_nbr\n")

    def fork_player(self) -> None:
        """
        Fork a new player from the current player.

        This method sends a 'Fork' command to the server to create a new player.

        :return: None
        """
        self.life -= self.FORK
        self.send_action("Fork\n")

    def eject(self) -> None:
        """
        Eject the bot from its current position.

        This method sends an 'Eject' command to the server to remove the bot from its current position.

        :return: None
        """
        self.send_action("Eject\n")

    def take_obj(self, obj: str) -> None:
        """
        Take an object from the current tile.

        This method sends a 'Take object' command to the server to pick up an object from the current tile.

        :return: None
        """
        self.life -= self.ACTION
        self.send_action(f"Take {obj}\n")

    def set_obj(self, obj: str) -> None:
        """
        Set the specified object on the current tile.

        :return: None
        """
        self.life -= self.ACTION
        self.send_action(f"Set {obj}\n")

    def incantation(self) -> None:
        """
        Perform the incantation action on the server.

        This method sends an 'Incantation' command to the server to start the incantation process.

        :return: None
        """
        self.life -= self.INCANTATION
        self.send_action("Incantation\n")

    @abstractmethod
    def run(self) -> None:
        pass


def display_help() -> None:
    """

    :return:
    """
    print('USAGE: ./zappy_ai.py -p port -n name -h machine')


def connection(port: str, name: str, machine: str):
        server_info, cli_socket = connexion.connect(port, name, machine)
        # print(f"Connected to {machine}:{port}")
        return server_info, cli_socket
