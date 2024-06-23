#!/usr/bin/env python3

from sys import argv, exit
from src.parsing import parsing

if __name__ == "__main__":
    settings = parsing(argv)
    exit(0)
