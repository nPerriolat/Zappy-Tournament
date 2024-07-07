#!/usr/bin/env python3

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food = 0
        self.linemate = 0
        self.deraumere = 0
        self.sibur = 0
        self.mendiane = 0
        self.phiras = 0
        self.thystame = 0
        self.player = 0

    def display(self):
        print("tile:", self.x, self.y)
        print("\tfood =", self.food)
        print("\tlinemate =", self.linemate)
        print("\tderaumere =", self.deraumere)
        print("\tsibur =", self.sibur)
        print("\tmendiane =", self.mendiane)
        print("\tphiras =", self.phiras)
        print("\tthystame =", self.thystame)
        print("\tplayer =", self.player)
    
    def add(self, item):
        match item:
            case "food":
                self.food += 1
            case "linemate":
                self.linemate += 1
            case "deraumere":
                self.deraumere += 1
            case "sibur":
                self.sibur += 1
            case "mendiane":
                self.mendiane += 1
            case "phiras":
                self.phiras += 1
            case "thystame":
                self.thystame += 1
            case "player":
                self.player += 1
            case "egg":
                print("I found an egg!")
            case "":
                pass
            case _:
                pass

    def get(self, item):
        match item:
            case "food":
                return self.food
            case "linemate":
                return self.linemate
            case "deraumere":
                return self.deraumere
            case "sibur":
                return self.sibur
            case "mendiane":
                return self.mendiane
            case "phiras":
                return self.phiras
            case "thystame":
                return self.thystame
            case "player":
                return self.player
            case _:
                pass