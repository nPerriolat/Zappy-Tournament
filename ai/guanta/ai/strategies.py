#!/usr/bin/env python3

import random

from ai.commands import *
import ai.algorithms as algo
import ai.constants as constants
from ai.data import Data

# prioritize repeating any not ally broadcast, without broadcast to repeat it gather food
def parrot_first(data : Data):
    broadcasts = []

    while True:
        if data.player.get("food") <= constants.FOOD_THRESHOLD * 3:
            look(data)
            if not algo.gather(data, "food"):
                forward(data)
        else:
            if data.last_broadcast != "" and len(broadcasts) < 20 and not algo.is_ally_broadcast(data.last_broadcast):
                broadcasts.append(data.last_broadcast)
                data.last_broadcast = ""
            broadcast(data, random.choice(broadcasts))

# prioritize repeating any not ally broadcast, without broadcast to repeat it gather food
def parrot_last(data : Data):
    while True:
        if data.player.get("food") <= constants.FOOD_THRESHOLD * 3:
            look(data)
            if not algo.gather(data, "food"):
                forward(data)
        else:
            if data.last_broadcast != "" and not algo.is_ally_broadcast(data.last_broadcast):
                for _ in range(random.randint(1, 5)):
                    broadcast(data, data.last_broadcast)
                data.last_broadcast = ""

def check_assemble(data : Data, br : BroadcastReceived):
    direction = int(br.args[0].split(' ')[0])
    message = br.args[0].split(' ')[1]
    if message == constants.BROADCAST_ASSEMBLE:
        data.player.x = 0
        data.player.y = 0
        data.player.facing = "UP"
        coord = algo.tile_index_to_player_distance(direction)
        if coord[0] == 0 and coord[1] == 0:
            while data.player.get("food") > constants.FOOD_THRESHOLD:
                inventory(data)
                if data.last_broadcast != "":
                    brcst = data.last_broadcast.split(' ')
                    coord = algo.tile_index_to_player_distance(int(brcst[0]))
                    if (coord[0] != 0 or coord[1] != 0) and brcst[1] == constants.BROADCAST_ASSEMBLE:
                        break
        else:
            algo.pathfinding(data, coord[0], coord[1])
            data.last_broadcast = ""
        return True
    return False

def worker_priority(data : Data):
    if data.map == []:
        if not look(data):
            return [[],0]
    target = data.map[0]
    score = data.goal.priority_score(data.player, target)
    for tile in data.map:
        tmp_score = data.goal.priority_score(data.player, tile)
        if tmp_score > score:
            target = tile
            score = tmp_score
    return [target, score]

# prioritize level up by gathering ressources
def worker(data : Data):
    initialize(data)
    data.role = "Worker"
    connect_nbr(data)
    end_game = False
    caster = False
    while True:
        try:
            inventory(data)
            look(data)
            # Si l'ia passe en dessous d'un certain seuil de bouffe, elle passe en mode farm de bouffe jusqu'à se mettre bien
            if data.player.get("food") <= constants.FOOD_THRESHOLD:
                while data.player.get("food") <= (constants.FOOD_THRESHOLD * 10):
                    look(data)
                    if not algo.gather(data, "food"):
                        forward(data)
                    else:
                        inventory(data)
                continue
            # Montée au niveau 2 dès que possible
            if data.player.level == 1 and (data.player.linemate >= 1 or (len(data.map) >= 1 and data.map[0].linemate >= 1)):
                if data.map[0].linemate < 1:
                    set_down(data, "linemate")
                incantation(data)
                continue
            # S'il y a un broadcast à gérer on s'en occupe prioritairement
            if data.last_broadcast != "" and data.player.level == 2:
                raise BroadcastReceived(data.last_broadcast)
            # S'il n'y a pas encore eu d'incitation au rassemblement et qu'il a toutes les ressources pour aller au lvl 8, rassemble les autres
            if data.player.is_goal_reached(data.goal) and not end_game:
                if not caster:
                    caster = True
                    continue
                while data.map[0].player < data.goal.total.player:
                    broadcast(data, constants.BROADCAST_ASSEMBLE)
                    look(data)
                    inventory(data)
                else:
                    algo.setup(data)
                    while incantation(data):
                        pass
                continue
            # Ramasse des ressources
            if end_game:
                if not algo.gather(data, "food"):
                    forward(data)
            else:
                target = worker_priority(data)
                if target[1] == 0:
                    algo.pathfinding(data, 1, data.player.level)
                    continue
                target = target[0]
                algo.pathfinding(data, target.x, target.y)
                if data.player.thystame < data.goal.total.thystame:
                    for x in range(target.thystame):
                        take(data, "thystame")
                if data.player.phiras < data.goal.total.phiras:
                    for x in range(target.phiras):
                        take(data, "phiras")
                if data.player.mendiane < data.goal.total.mendiane:
                    for x in range(target.mendiane):
                        take(data, "mendiane")
                if data.player.sibur < data.goal.total.sibur:
                    for x in range(target.sibur):
                        take(data, "sibur")
                if data.player.deraumere < data.goal.total.deraumere:
                    for x in range(target.deraumere):
                        take(data, "deraumere")
                if data.player.linemate < data.goal.total.linemate:
                    for x in range(target.linemate):
                        take(data, "linemate")
                for x in range(target.food):
                    take(data, "food")
        except BroadcastReceived as br:
            if check_assemble(data, br):
                end_game = True

# prioritize to create new players
def recruiter(data : Data):
    initialize(data)
    data.display()
    data.role = "Recruiter"
    connect_nbr(data)
    nb_workers = 1 + data.remaining_places
    while True:
        try:
            look(data)
            if data.player.get("food") <= constants.FOOD_THRESHOLD:
                while data.player.get("food") <= (constants.FOOD_THRESHOLD * 3):
                    look(data)
                    if not algo.gather(data, "food"):
                        forward(data)
                    else:
                        inventory(data)
                continue
            if data.player.level == 1 and data.map[0].linemate >= 1:
                incantation(data)
                continue
            if data.last_broadcast != "":
                raise BroadcastReceived(data.last_broadcast)
            connect_nbr(data)
            if data.remaining_places > 0:
                reproduct(data, "worker")
                continue
            if nb_workers < 24:
                fork(data)
                nb_workers += 1
                continue
            if not algo.gather(data, "food"):
                forward(data)
        except BroadcastReceived as br:
            check_assemble(data, br)

strategies = {
    "parrot_first": parrot_first,
    "parrot_last": parrot_last,
    "worker": worker,
    "recruiter": recruiter
}
