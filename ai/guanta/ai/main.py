#!/usr/bin/env python3

import socket
from sys import argv, exit

from ai.algorithms import *
from ai.commands import *
from ai.exceptions import Dead, ConnectionRefused, Forked
from ai.parsing import parsing
from ai.print import exprint
from ai.strategies import strategies, recruiter

if __name__ == "__main__":
    data = parsing(argv)
    alive = True
    while alive:
        try:
            try:
                recruiter(data)
            except Forked:
                strategies[data.role](data)
        except KeyboardInterrupt:
            print("AI stopped by user")
            alive = False
        except Dead as death:
            print(f"\033[0;31m{death.args[0]} Dead\033[0m")
            alive = False
        except ConnectionRefused as cr:
            print(f"\033[0;31m{cr.args[0]}\033[0m")
            alive = False
        except (ConnectionResetError, UnicodeDecodeError):
            print("\033[0;31mSocket closes, AI stopped !\033[0m")
            alive = False
    data.sock.close()
    exit(0)
