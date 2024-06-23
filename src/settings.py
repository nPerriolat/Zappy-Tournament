#!/usr/bin/env python3

import os
import time
import math
from typing import List

from src.color import *

def header_case(width : int):
    print(f"╔{"".ljust(width - 2, "═")}╗")

def footer_case(width : int):
    print(f"╚{"".ljust(width - 2, "═")}╝")

def body_case(width : int, text : str, color : str = ""):
    print(f"║{color}", f"{text}".ljust(width - 4), f"{BLANK}║")

class Settings:
    def __init__(self, teams : List[str], hostname : str = "localhost", port : int = 8080, x : int = 30, y : int = 30, c : int = 1, frequence : int = 100, needed_wins : int = 3, timeout : int = 5):
        self.hostname = hostname
        self.port = port
        self.teams = teams
        self.x = x
        self.y = y
        self.starting_eggs = c
        self.frequence = frequence
        self.needed_wins = needed_wins
        self.timeout = timeout
        self.is_ready = True

    def display(self):
        width = os.get_terminal_size().columns
        header_case(width)
        body_case(width, "ZAPPY TOURNAMENT SETTINGS", YELLOW)
        body_case(width, "")
        if 0 < self.port:
            body_case(width, f"Socket address: {self.hostname}:{self.port}")
        else:
            body_case(width, f"Socket address: {self.hostname}:{self.port}", RED)
            self.is_ready = False
        body_case(width, "")
        if 2 <= len(self.teams):
            body_case(width, f"Number of teams: {len(self.teams)}")
        else:
            body_case(width, f"Number of teams: {len(self.teams)}", RED)
            self.is_ready = False
        body_case(width, "List of registered teams:")
        for team in self.teams:
            if team != "GRAPHIC":
                body_case(width, f" - {team}")
            else:
                body_case(width, f" - {team}", RED)
                self.is_ready = False
        body_case(width, "")
        body_case(width, "Server settings:")
        if 10 <= self.x <= 30 and 10 <= self.y <= 30:
            body_case(width, f"    Dimensions: ({self.x}, {self.y})")
        else:
            body_case(width, f"    Dimensions: ({self.x}, {self.y})", RED)
            self.is_ready = False
        if 1 <= self.starting_eggs:
            body_case(width, f"    Starting eggs per team: {self.starting_eggs}")
        else:
            body_case(width, f"    Starting eggs per team: {self.starting_eggs}", RED)
            self.is_ready = False
        if 2 <= self.frequence <= 2000:
            body_case(width, f"    Frequence: {self.frequence}")
        else:
            body_case(width, f"    Frequence: {self.frequence}", RED)
            self.is_ready = False
        body_case(width, "")
        body_case(width, "Tournament format:")
        if 1 <= self.needed_wins:
            body_case(width, f"    Win condition: BO{(self.needed_wins - 1) * 2 + 1}")
        else:
            body_case(width, f"    Win condition: BO{(self.needed_wins - 1) * 2 + 1}", RED)
            self.is_ready = False
        if 1 <= self.timeout:
            body_case(width, f"    Timeout: {self.timeout}min")
        else:
            body_case(width, f"    Timeout: {self.timeout}min", RED)
            self.is_ready = False
        body_case(width, "")
        if self.is_ready:
            body_case(width, f"Status: READY TO RUN", GREEN)
            body_case(width, f"Runtime (longest estimate): {time.strftime("%Hh %Mmin", time.gmtime(math.comb(len(self.teams), 2) * ((self.needed_wins - 1) * 2 + 1) * self.timeout * 60))}")
        else:
            body_case(width, f"Status: UNABLE TO RUN", RED)
        footer_case(width)
