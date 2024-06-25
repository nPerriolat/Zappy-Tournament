#!/usr/bin/env python3

from sys import argv, exit

from src.parsing import parsing
from src.color import YELLOW, BLANK
from src.match import Match
from src.schedule import scheduling

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
        match = Match("team1", "team2", settings)
        result = match.run()
        result.display()
    except KeyboardInterrupt:
        print("Processus aborted by user")
    exit(0)
