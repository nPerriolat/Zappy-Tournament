##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## ZappySocket.py
##

"""
@file zappy_socket.py
"""

import socket
from typing import Optional, List
import errno

class ZappySocket:
    """
    @class ZappySocket
    @brief Socket class for Zappy AI
    @details
    This class is used to communicate with the Zappy server.
    """
    def __init__(self, port: int, host: str):
        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = ""
        self.connected = False

    def send(self, msg: str) -> bool:
        """
        @brief Send a message to the server
        @param msg: Message to send
        """
        try:
            res = self.socket.send(f"{msg}\n".encode('ascii'))
            if res == 0:
                raise RuntimeError("Socket connection broken")
            return True
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                return False
            raise RuntimeError("Socket error :", err)

    def connect(self) -> None:
        """
        @brief Connect to the server
        """
        self.socket.connect((self.host, self.port))
        if self.socket is None:
            raise ConnectionError("Could not connect to the server")
        self.connected = True

    def recv(self) -> Optional[List[str]]:
        """
        @brief Receive a message from the server
        @return: Message received
        """
        payloads: list[str]  = []
        while True:
            try:
                chunk = self.socket.recv(2048)
                if chunk == b'':
                    raise RuntimeError("Server disconnected")
                self.buffer += chunk.decode('ascii')
                if b'\n' in chunk:
                    sub_payloads = self.buffer.split('\n')
                    remain = sub_payloads[-1]
                    if not remain: # server fininshed sending all
                        self.buffer = ""
                        return sub_payloads[:-1]
                    payloads += sub_payloads
                    [payloads.extend(l) for l in sub_payloads[:-1]]
                    self.buffer = remain
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    return None
                raise RuntimeError("Socket error :", err)

    def close(self) -> None:
        """
        @brief Close the connection with the server
        """
        self.socket.close()

    def reset(self) -> None:
        """
        @brief Reset the socket
        """
        self.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_blocking(self, value: Optional[bool] = None) -> None:
        """
        @brief Toggle the socket to blocking or non-blocking mode
        """
        if value is None:
            value = not self.socket.getblocking()
        self.socket.setblocking(value)

    def __del__(self) -> None:
        self.close()
