#!/usr/bin/env python3

import os
import time
import math
from typing import List

from src.color import *

class Result:
    def __init__(self, teamA : str, teamB : str, winner : str, time : float):
        self.teamA = teamA
        self.teamB = teamB
        self.winner = winner
        self.time = time
    
    def display(self):
        print(f"{self.teamA} VS {self.teamB}")
        print(f"winner: {self.winner}")
        print(f"time: {time.strftime("%Mmin %Ss", time.gmtime(self.time))}")
