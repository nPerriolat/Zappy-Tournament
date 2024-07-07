#!/usr/bin/env python3

from sys import exit, stderr

# Print a message to stderr
def eprint(msg):
    print("zappy_ai : ERROR : " + msg, file=stderr)

# Print a message to stderr then exit 84
def exprint(msg):
    eprint(msg)
    exit(84)

# Print the usage then exit 0
def help():
    print("USAGE")
    print("\t./zappy_ai -p port -n name [-h machine]")
    print("")
    print("DESCRIPTION")
    print("\t-p port\t\tport number")
    print("\t-n name\t\tname of the team")
    print("\t-h machine\thostname; localhost by default")
    exit(0)
