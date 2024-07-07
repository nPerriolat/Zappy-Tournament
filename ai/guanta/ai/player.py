#!/usr/bin/env python3

from enum import IntEnum

from ai.print import exprint

class Player:
    def __init__(self):
        self.level = 1
        self.x = 0
        self.y = 0
        self.facing = "UP"
        self.food = 10
        self.linemate = 0
        self.deraumere = 0
        self.sibur = 0
        self.mendiane = 0
        self.phiras = 0
        self.thystame = 0

    def display(self):
        print("player:", self.level, self.x, self.y, self.facing)
        print("\tfood =", self.food)
        print("\tlinemate =", self.linemate)
        print("\tderaumere =", self.deraumere)
        print("\tsibur =", self.sibur)
        print("\tmendiane =", self.mendiane)
        print("\tphiras =", self.phiras)
        print("\tthystame =", self.thystame)

    def turn(self, direction):
        if direction == "RIGHT":
            match self.facing:
                case "UP":
                    self.facing = "RIGHT"
                case "RIGHT":
                    self.facing = "DOWN"
                case "DOWN":
                    self.facing = "LEFT"
                case "LEFT":
                    self.facing = "UP"
        elif direction == "LEFT":
            match self.facing:
                case "UP":
                    self.facing = "LEFT"
                case "RIGHT":
                    self.facing = "UP"
                case "DOWN":
                    self.facing = "RIGHT"
                case "LEFT":
                    self.facing = "DOWN"
        else:
            pass

    def forward(self):
        if self.facing == "UP":
            self.y += 1
        elif self.facing == "RIGHT":
            self.x += 1
        elif self.facing == "DOWN":
            self.y -= 1
        elif self.facing == "LEFT":
            self.x -= 1

    def add(self, ressource):
        match ressource:
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
            case _:
                pass

    def remove(self, ressource):
        match ressource:
            case "food":
                self.food -= 1
            case "linemate":
                self.linemate -= 1
            case "deraumere":
                self.deraumere -= 1
            case "sibur":
                self.sibur -= 1
            case "mendiane":
                self.mendiane -= 1
            case "phiras":
                self.phiras -= 1
            case "thystame":
                self.thystame -= 1
            case _:
                pass

    def get(self, ressource):
        match ressource:
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
            case _:
                pass

    def is_goal_reached(self, goal):
        enough = self.linemate >= goal.total.linemate
        enough = enough and self.deraumere >= goal.total.deraumere
        enough = enough and self.sibur >= goal.total.sibur
        enough = enough and self.mendiane >= goal.total.mendiane
        enough = enough and self.phiras >= goal.total.phiras
        enough = enough and self.thystame >= goal.total.thystame
        return enough
