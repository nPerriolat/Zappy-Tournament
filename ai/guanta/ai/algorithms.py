#!/usr/bin/env python3

import re
import time
from typing import Tuple

from ai.commands import *
import ai.constants as constants
from ai.data import Data

def turn_back(data):
    return right(data) and right(data)

# move to the given relative coordinate (relative to the player)
# > raise Dead if the player is dead
# > return false if the destination asked is farther than the reach of a look
# > return true if the destination has been reached
def pathfinding(data : Data, x : int, y : int) -> bool:
    diffY = y - data.player.y
    diffX = x - data.player.x
    if diffX == 0 and diffY == 0:
        return True
    elif data.player.facing == "UP" and diffY > 0:
        while data.player.y != y:
            forward(data)
        if diffX > 0:
            right(data)
        elif diffX < 0:
            left(data)
    elif data.player.facing == "RIGHT" and diffX > 0:
        while data.player.x != x:
            forward(data)
        if diffY > 0:
            left(data)
        elif diffY < 0:
            right(data)
    elif data.player.facing == "DOWN" and diffY < 0:
        while data.player.y != y:
            forward(data)
        if diffX > 0:
            left(data)
        elif diffX < 0:
            right(data)
    elif data.player.facing == "LEFT" and diffX < 0:
        while data.player.x != x:
            forward(data)
        if diffY > 0:
            right(data)
        elif diffY < 0:
            left(data)
    else:
        if data.player.facing == "UP":
            if diffX > 0:
                right(data)
            elif diffX < 0:
                left(data)
            else:
                turn_back(data)
        elif data.player.facing == "RIGHT":
            if diffY > 0:
                left(data)
            elif diffY < 0:
                right(data)
            else:
                turn_back(data)
        elif data.player.facing == "DOWN":
            if diffX > 0:
                left(data)
            elif diffX < 0:
                right(data)
            else:
                turn_back(data)
        elif data.player.facing == "LEFT":
            if diffY > 0:
                right(data)
            elif diffY < 0:
                left(data)
            else:
                turn_back(data)
        pathfinding(data, x, y)
    diffY = y - data.player.y
    diffX = x - data.player.x
    if diffX == 0 and diffY == 0:
        return True
    if data.player.facing == "UP" and diffY > 0:
        while data.player.y != y:
            forward(data)
    elif data.player.facing == "RIGHT" and diffX > 0:
        while data.player.x != x:
            forward(data)
    elif data.player.facing == "DOWN" and diffY < 0:
        while data.player.y != y:
            forward(data)
    elif data.player.facing == "LEFT" and diffX < 0:
        while data.player.x != x:
            forward(data)
    diffY = y - data.player.y
    diffX = x - data.player.x
    if diffX == 0 and diffY == 0:
        return True
    return False

# search and take the given ressource if able
# > raise Dead if the player is dead
# > return false if the ressource hasn't been found in the last look
# > return true if the ressource has been collected
def gather(data : Data, ressource : str) -> bool:
    if data.map == []:
        if not look(data):
            return False
    target = data.map[0]
    ratio = target.get(ressource)
    for tile in data.map:
        try:
            tmp_ratio = tile.get(ressource) / (abs(tile.x) + tile.y)
        except:
            tmp_ratio = tile.get(ressource)
        if tmp_ratio > ratio:
            target = tile
            ratio = tmp_ratio
    if target.get(ressource) == 0:
        return False
    succeed = pathfinding(data, target.x, target.y)
    for x in range(target.get(ressource)):
        succeed = succeed and take(data, ressource)
        data.player.add(ressource)
    return succeed

# eject the closest player from his tile
# > raise Dead if the player is dead
# > return false if no players has been found
# > return true if at least one player has been ejected
def attack(data : Data) -> bool:
    target = data.map[0]
    ratio = target.get("player")
    for tile in data.map:
        tmp_ratio = tile.get("player")
        if tmp_ratio > ratio:
            target = tile
            ratio = tmp_ratio
    if target.get("player") == 0 or (target.get("player") == 1 and target.x == data.player.x and target.y == data.player.y):
        return False
    return pathfinding(data, target.x, target.y) and eject(data)

def setup(data):
    for item in range(data.player.linemate):
        set_down(data, "linemate")
    for item in range(data.player.deraumere):
        set_down(data, "deraumere")
    for item in range(data.player.sibur):
        set_down(data, "sibur")
    for item in range(data.player.mendiane):
        set_down(data, "mendiane")
    for item in range(data.player.phiras):
        set_down(data, "phiras")
    for item in range(data.player.thystame):
        set_down(data, "thystame")

# actualize informations stored in data
# > raise Dead if the player is dead
# > return false if the actualization failed
# > return true if the actualization succeed
def actualize(data : Data) -> bool:
    return inventory(data) and connect_nbr(data)

def is_ally_broadcast(received : str) -> bool:
    return received.startswith(constants.BROADCAST_HEADER)

def parse_broadcast_message(received : str) -> None | Tuple[int, str]:
    """
    Checks if a string is formatted as a broadcast message response.
    Returns (tile, message) if correctly formatted, None otherwise
    """
    if re.fullmatch("message [^,]+, .*", received) is None: # command isn't message
        return None
    tile, message = received[len("message "):].split(',')
    return (tile, message)

def read_broadcast_message(data : Data, timeout_seconds : float = 0.1) -> None | Tuple[int, str]:
    """
    Checks if a string is formatted as a broadcast message response.
    Returns (tile, message) if correctly formatted, None otherwise
    """
    received = ""
    START = time.time_ns()
    while not received:
        NOW = time.time_ns()
        if (NOW - START) / 1e9 >= timeout_seconds:
            return None
        received = data.sock.recv(1024).decode()
    return parse_broadcast_message(received)

def confirm_ally_in_incantation() -> None:
    """
    Broadcasts a message to inform the player is involved in an incantation, mainly
    to prevent soldiers from ejecting him.
    """
    broadcast(constants.BROADCAST_HEADER + constants.BROADCAST_INCANTATION_CONFIRMED)

def ask_if_ally_in_incantation(data : Data) -> None | int:
    """
    Broadcasts a message to ask if there is an ally in an incantation mainly
    to prevent soldiers from ejecting him.
    """
    broadcast(constants.BROADCAST_HEADER + constants.BROADCAST_INCANTATION_ASK)
    try:
        tile, msg = read_broadcast_message(data)
        return tile
    except: # Nothing was read
        return None

def tile_index_to_player_distance(tile_index : int) -> Tuple[int]:
    """
    Converts a tile index (1-8, 0 being the player position) to a player direction.
    """
    match tile_index:
        case 0: return (0, 0)
        case 1: return (0, 1)
        case 2: return (-1, 1)
        case 3: return (-1, 0)
        case 4: return (-1, -1)
        case 5: return (0, -1)
        case 6: return (1, -1)
        case 7: return (1, 0)
        case 8: return (1, 1)
        case _: raise ValueError(f"Tile {tile_index} doesn't exist ! Tiles are only from 0 to 8 (both included) !")