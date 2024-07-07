#!/usr/bin/env python3

from os import system
from sys import exit
from typing import List

from ai.data import Data
from ai.print import eprint, exprint, help

# Check if the hostname is accessible with a single ping
# if the ping fail it return False, otherwise True
def ping(hostname : str) -> bool:
    return system("ping -c 1 " + hostname + " 2>&1 >/dev/null") == 0

# Parse arguments and handle arguments errors
def parsing(argv : List[str]) -> Data:
    argc = len(argv)
    if argc == 2 and argv[1] == "-h":
        help()
    if argc != 5 and argc != 7:
        exprint("Wrong number of arguments. Try -h instead.")
    if argv[1] != "-p":
        eprint("Wrong arguments. Try -h instead.")
        exprint("Remember to respect arguments order.")
    try:
        port = int(argv[2])
        if port < 0:
            exit(84)
    except:
        exprint("The port must be a positive integer.")
    if argv[3] != "-n":
        eprint("Wrong arguments. Try -h instead.")
        exprint("Remember to respect arguments order.")
    if argv[4] == "GRAPHIC":
        exprint("The GRAPHIC team name is reserved, you must use another one.")
    data = Data(port, argv[4])
    if argc == 7:
        if argv[5] != "-h":
            eprint("Wrong arguments. Try -h instead.")
            exprint("Remember to respect arguments order.")
        data.hostname = argv[6]
    if not ping(data.hostname):
        exprint("The machine " + data.hostname + " is inaccessible.")
    return data
