#!/usr/bin/env python3

import os
import socket

from ai.data import Data
from ai.exceptions import Dead, ConnectionRefused, BroadcastReceived, BroadcastDeny, Forked
from ai.tile import Tile
from ai.traduction import translate

# ===========================================================================\\
#                                DO NOT USE                                  ||
# ===========================================================================//
def check_broadcast(data, text):
    brs = text.split('\n')
    if len(brs) > 1:
        for br in brs:
            if check_broadcast(data, br):
                return True
        return False
    words = text.split(' ')
    if words[0] != "message":
        return False
    words = words[2].split('_')
    if words[0] != data.team_id:
        raise BroadcastDeny
    if words[1] in data.broadcast_registry and words[2] in data.broadcast_registry[words[1]]:
        raise BroadcastDeny
    if words[1] in data.broadcast_registry:
        data.broadcast_registry[words[1]].append(words[2])
        return True
    data.broadcast_registry[words[1]] = [words[2]]
    return True

def listen_broadcast(data, text):
    received = data.sock.recv(1024).decode()
    while True:
        while received == "":
            received = data.sock.recv(1024).decode()
        brs = received.split('\n')
        while brs != []:
            received = brs[0]
            if received == "dead":
                raise Dead(data.role)
            if received == "ko":
                return False
            try:
                if check_broadcast(data, received):
                    data.last_broadcast = received.split(' ')[1][:-1] + " " + received.split(' ')[2].split('_')[3]
                    brs.pop(0)
                    continue
            except BroadcastDeny:
                brs.pop(0)
                continue
            if text == "":
                return received
            if received == text:
                return True
            brs.pop(0)

def imperative_command(data : Data, command : str) -> bool:
    data.sock.send((command + "\n").encode())
    return listen_broadcast(data, "ok")

def imperative_command_with_args(data : Data, command : str, arg : str) -> bool:
    return imperative_command(data, command + " " + arg)

def ask_command(data : Data, command : str) -> str:
    data.sock.send((command + "\n").encode())
    return listen_broadcast(data, "")

# ===========================================================================\\
#                                 COMMANDS                                   ||
# ===========================================================================//
def initialize(data : Data) -> bool:
    data.reset()
    try:
        data.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data.sock.connect((data.hostname, data.port))
    except:
        raise ConnectionRefused(f"Failed to connect to {data.hostname}:{data.port}")
    received = data.sock.recv(1024).decode()
    if received == "ko\n":
        raise ConnectionRefused("Server refused the connexion")
    data.sock.send(data.team.encode())
    listens = data.sock.recv(1024).decode().split()
    try:
        data.remaining_places = int(listens[0])
        data.dimensions = [int(listens[1]), int(listens[2])]
    except:
        raise ConnectionRefused("Server send corrupted informations at connexion initialization")
    return True

def forward(data : Data) -> bool:
    result = imperative_command(data, "Forward")
    if result:
        data.player.forward()
    return result

def right(data : Data) -> bool:
    result = imperative_command(data, "Right")
    if result:
        data.player.turn("RIGHT")
    return result

def left(data : Data) -> bool:
    result = imperative_command(data, "Left")
    if result:
        data.player.turn("LEFT")
    return result

def look(data : Data) -> bool:
    panorama = ask_command(data, "Look")
    if not panorama:
        return False
    try:
        panorama = panorama[2:][:-2].split(",")
        data.map = []
        x = 0
        y = 0
        for zone in panorama:
            tile = Tile(x, y)
            for item in zone.split(' '):
                tile.add(item)
            data.map.append(tile)
            if x + 1 > y:
                if y + 1 > data.player.level:
                    break
                y += 1
                x = -y
            else:
                x += 1
        data.player.x = 0
        data.player.y = 0
        data.player.facing = "UP"
    except:
        return False
    return True

def inventory(data : Data) -> bool:
    inv = ask_command(data, "Inventory")
    if not inv:
        return False
    tmp = data
    try:
        inv = inv[2:][:-2].split(", ")
        data.player.food = int(inv[0].split(" ")[1])
        data.player.linemate = int(inv[1].split(" ")[1])
        data.player.deraumere = int(inv[2].split(" ")[1])
        data.player.sibur = int(inv[3].split(" ")[1])
        data.player.mendiane = int(inv[4].split(" ")[1])
        data.player.phiras = int(inv[5].split(" ")[1])
        data.player.thystame = int(inv[6].split(" ")[1])
    except:
        data = tmp
        return False
    return True

def broadcast(data : Data, text : str) -> bool:
    data.broadcast_count += 1
    return imperative_command(data, "Broadcast " + data.team_id + "_" + data.player_id + "_" + translate(data.broadcast_count) + "_" + text)

def connect_nbr(data : Data) -> bool:
    received = ask_command(data, "Connect_nbr")
    if not received:
        return False
    tmp = data.remaining_places
    try:
        data.remaining_places = int(received.split()[0])
    except:
        data.remaining_places = tmp
        return False
    return True

def reproduct(data : Data, strategy : str) -> None:
    id = os.fork()
    if id == 0:
        data.reset()
        raise Forked(strategy)

# ATTENTION: The instruction Fork isn't a process fork but ask the server to hatch an egg.
def fork(data : Data) -> bool:
    return imperative_command(data, "Fork")

def eject(data : Data) -> bool:
    return imperative_command(data, "Eject")

def take(data : Data, ressource : bool) -> bool:
    result = imperative_command_with_args(data, "Take", ressource)
    if result:
        data.player.add(ressource)
    return result

def set_down(data : Data, ressource : str) -> bool:
    result = imperative_command_with_args(data, "Set", ressource)
    if result:
        data.player.remove(ressource)
    return result

def incantation(data : Data) -> bool:
    command = "Incantation"
    data.sock.send((command + "\n").encode())
    if not listen_broadcast(data, "Elevation underway"):
        return False
    received = listen_broadcast(data, "")
    while not received or received.split(': ')[0] != "Current level":
        received = listen_broadcast(data, "")
    data.player.level = int(received.split(': ')[1])
    if data.player.level >= 8:
        print("\033[0;32mVictory!\033[0m")
    return True
