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
