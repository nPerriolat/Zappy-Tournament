#!/usr/bin/env python3

import random as rd
from os import getpid
from typing import List

from ai.goal import Goal
from ai.player import Player
from ai.tile import Tile
from ai.traduction import translate

class Data:
    def __init__(self, port : int, team : str, hostname : str = "localhost"):
        self.port = port
        self.team = team + "\n"
        self.hostname = hostname
        self.role = "worker"
        self.remaining_places = -1
        self.dimensions = []
        self.player = Player()
        self.map : List[Tile] = []
        self.goal = Goal()
        self.team_id = "关塔那摩"
        self.player_id = translate(rd.randint(0, 999999999))
        self.broadcast_count = 0
        self.broadcast_registry = {}
        self.last_broadcast = ""

    def display(self):
        print("pid:", getpid())
        print("\tport =", self.port)
        print("\tteam =", self.team)
        print("\thostname =", self.hostname)
        print("\tremaining =", self.remaining_places)
        print("\tdimensions =", self.dimensions)

    def reset(self):
        self.role = "worker"
        self.remaining_places = -1
        self.dimensions = []
        self.player = Player()
        self.map = []
        self.goal = Goal()
        self.player_id = translate(rd.randint(0, 999999999))
        self.broadcast_count = 0
        self.broadcast_registry = {}
        self.last_broadcast = ""
