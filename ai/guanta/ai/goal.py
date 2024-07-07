#!/usr/bin/env python3

class Level:
    def __init__(self, player : int, linemate : int, deraumere : int, sibur : int, mendiane : int, phiras : int, thystame : int):
        self.player = player
        self.linemate = linemate
        self.deraumere = deraumere
        self.sibur = sibur
        self.mendiane = mendiane
        self.phiras = phiras
        self.thystame = thystame

class Goal:
    def __init__(self):
        self.total = Level(8, 9, 8, 10, 5, 6, 1)
        self.levels = [
            Level(1, 1, 0, 0, 0, 0, 0),
            Level(2, 1, 1, 1, 0, 0, 0),
            Level(2, 2, 0, 1, 0, 2, 0),
            Level(4, 1, 1, 2, 0, 1, 0),
            Level(4, 1, 2, 1, 3, 0, 0),
            Level(6, 1, 2, 3, 0, 1, 0),
            Level(6, 2, 2, 2, 2, 2, 1)
        ]

    def consume(self, level : int):
        level -= 1 # indices are 0-based whereas levels are 1-based
        self.total.linemate -= self.levels[level].linemate
        self.total.deraumere -= self.levels[level].deraumere
        self.total.sibur -= self.levels[level].sibur
        self.total.mendiane -= self.levels[level].mendiane
        self.total.phiras -= self.levels[level].phiras
        self.total.thystame -= self.levels[level].thystame
        return self.levels[level]

    def priority_score(self, inventory, tile):
        score = 0
        if inventory.food < 11:
            score += tile.food * 2
        if inventory.linemate < self.total.linemate:
            diff = self.total.linemate - inventory.linemate
            if tile.linemate > diff:
                score += diff * 4
            else:
                score += tile.linemate * 4
        if inventory.deraumere < self.total.deraumere:
            diff = self.total.deraumere - inventory.deraumere
            if tile.deraumere > diff:
                score += diff * 7
            else:
                score += tile.deraumere * 7
        if inventory.sibur < self.total.sibur:
            diff = self.total.sibur - inventory.sibur
            if tile.sibur > diff:
                score += diff * 10
            else:
                score += tile.sibur * 10
        if inventory.mendiane < self.total.mendiane:
            diff = self.total.mendiane - inventory.mendiane
            if tile.mendiane > diff:
                score += diff * 10
            else:
                score += tile.mendiane * 10
        if inventory.phiras < self.total.phiras:
            diff = self.total.phiras - inventory.phiras
            if tile.phiras > diff:
                score += diff * 13
            else:
                score += tile.phiras * 13
        if inventory.thystame < self.total.thystame:
            diff = self.total.thystame - inventory.thystame
            if tile.thystame > diff:
                score += diff * 20
            else:
                score += tile.thystame * 20
        return score
