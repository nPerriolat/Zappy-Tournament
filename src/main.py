#!/usr/bin/env python3

import os
from sys import argv, exit

from src.parsing import parsing
from src.color import YELLOW, BLANK
from src.match import Match
from src.schedule import scheduling
from src.result import Duel, ScoreBoard

if __name__ == "__main__":
    try:
        settings = parsing(argv)
        answer = ""
        while answer not in ["y", "yes", "n", "no"]:
            print("Do you confirm this settings?: (y/n)")
            answer = input().lower()
        if answer in ["n", "no"]:
            print("You've choosed to refuse the above settings, abort.")
            exit(0)
        print(f"{YELLOW}The tournament simulation is about to start. Please make sure this processus will not be interupted.{BLANK}")
        schedule = scheduling(settings)
        scoreboard = ScoreBoard(settings)
        i = 0
        filename = f"log/zappy_tournament_{i}.log"
        while os.path.exists(filename):
            i += 1
            filename = f"log/zappy_tournament_{i}.log"
        log = open(filename, "x")
        for part in schedule:
            for adversary in part[1]:
                duel = Duel(part[0], adversary, settings)
                while duel.winner == None:
                    match = Match(part[0], adversary, settings)
                    result = match.safe_run()
                    duel.add(result)
                    log.write(result.display())
                log.write(duel.display())
                scoreboard.add(duel)
        log.write(scoreboard.display())
        log.close()
        print(f"The tournament is over. You will find the results in {filename}.")
    except KeyboardInterrupt:
        print("Processus aborted by user")
    exit(0)
