#!/usr/bin/env python3

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
        for part in schedule:
            for adversary in part[1]:
                duel = Duel(part[0], adversary, settings)
                while duel.winner == None:
                    match = Match(part[0], adversary, settings)
                    result = match.run()
                    duel.add(result)
                scoreboard.add(duel)
        scoreboard.display()
    except KeyboardInterrupt:
        print("Processus aborted by user")
    exit(0)
