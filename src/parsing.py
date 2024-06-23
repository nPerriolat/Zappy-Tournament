#!/usr/bin/env python3

from sys import exit

from src.settings import Settings

def help():
    print("USAGE")
    print("\tzts -t <teams> [-f <optional>]")
    print("")
    print("DESCRIPTION")
    print("\t-t\tlist of the team's names")
    print("\t\tMust be formated like \"team1 team2 team3 team4\"")
    print("\t-h\tTo set the hostname")
    print("\t-p\tTo set the port")
    print("\t-x\tTo set the map's width")
    print("\t-y\tTo set the map's length")
    print("\t-c\tTo set the starting eggs per teams")
    print("\t-f\tTo set the server's frequence")
    exit(0)

# Parse arguments and handle arguments errors
def parsing(argv):
    argc = len(argv)
    if argc == 2 and argv[1] == "-h":
        help()
    if argc < 3 or 15 < argc or argc % 2 == 0:
        print("Wrong number of arguments, abort.")
        exit(1)
    if argv[1] != "-t":
        print("The team's flag was expected, abort.")
        exit(1)
    settings = Settings(argv[2].split(" "))
    last_was_flag = False
    i = 0
    for arg in argv:
        if i < 3:
            i += 1
            continue
        if last_was_flag:
            last_was_flag = False
            i += 1
            continue
        last_was_flag = True
        match arg:
            case "-h":
                settings.hostname = argv[i + 1]
            case "-p":
                try:
                    settings.port = int(argv[i + 1])
                except:
                    print("Invalid port, abort.")
                    exit(1)
            case "-x":
                try:
                    settings.x = int(argv[i + 1])
                except:
                    print("Invalid map width (x), abort.")
                    exit(1)
            case "-y":
                try:
                    settings.y = int(argv[i + 1])
                except:
                    print("Invalid map length (y), abort.")
                    exit(1)
            case "-c":
                try:
                    settings.starting_eggs = int(argv[i + 1])
                except:
                    print("Invalid starting eggs number, abort.")
                    exit(1)
            case "-f":
                try:
                    settings.frequence = int(argv[i + 1])
                except:
                    print("Invalid frequence, abort.")
                    exit(1)
            case _:
                print("Invalid flag, abort.")
                exit(1)
        i += 1
    settings.display()
    if not settings.is_ready:
        print("Wrong values, cannot start. Please retry correcting the incorrect values.")
        exit(1)
    return settings
