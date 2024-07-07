##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## Nearest.py
##

"""
@file: Nearest.py
"""

from __future__ import annotations

from typing import Optional

from ..Map import Map, Position, ResourceType
from .. import Player
from ..Locomotion import LocomotionDirection
from ..Constants import PLAYER_DENSITY_THRESHOLD

def has_resource(p_map: Map, pos: Position, resource: ResourceType, time_max: int | None, is_same_pos = False) -> bool:
    """
    Returns True if the given position has the given resource
    """
    tile = p_map.get_resource(pos.x, pos.y)
    if tile is None or (time_max is not None and tile.last_check_time <= time_max):
        return False
    if PLAYER_DENSITY_THRESHOLD > p_map.player_density:
        if tile.types.count(ResourceType.PLAYER) > 1 - (0 if is_same_pos else 1):
            return False # TODO : maybe incantation, don't interrupt unless is enemy (base is broadcasted)
    if p_map.bases and pos in p_map.bases: # don't take resources from bases
        return False
    return resource in tile.types

def __sub_calculate(player: Player.Player, resource: ResourceType, time_max: int | None = None) -> Optional[Position]:
    """
    Returns the nearest position of the given resource
    """
    map = player.map
    og = player.map.player_pos
    dir = player.map.player_dir

    if (has_resource(map, og, resource, time_max, True)):
        return og

    match dir:
        case LocomotionDirection.UP | LocomotionDirection.DOWN:
            if dir == LocomotionDirection.UP:
                factor = 1
                ranging = range(1, 6)
            else:
                factor = -1
                ranging = range(-1, -6, -1)
            forward_max = map.forward_max_y
            backward_max = map.backward_max_y

            for i in ranging: # POIDS : nombre de movements maxi dans notre algo, sinon on fait un gros move aléatoire
                abs_i = abs(i)
                # strict forward
                if abs_i <= forward_max:
                    pos = Position(og.x, og.y + i)
                    if (has_resource(map, pos, resource, time_max)):
                        return pos

                if abs_i >= 2:
                    # lateral
                    pos = Position(og.x + i + 1, og.y)
                    if (has_resource(map, pos, resource, time_max)):
                        return pos
                    pos = Position(og.x - i - 1, og.y)
                    if (has_resource(map, pos, resource, time_max)):
                        return pos

                if abs_i >= 3:
                    # strict backward
                    if i <= backward_max:
                        pos = Position(og.x, og.y - i + 2)
                        if (has_resource(map, pos, resource, time_max)):
                            return pos
                    # diagonals up
                    add = abs_i - 3
                    for j in range(1, abs_i - 2 + 1):
                        pos = Position(og.x - j * factor + add, og.y + j * factor + add)
                        if (has_resource(map, pos, resource, time_max)):
                            return pos
                        pos = Position(og.x + j * factor + add, og.y + j * factor + add)
                        if (has_resource(map, pos, resource, time_max)):
                            return pos
                # if abs_i >= 4:
                #     # diagonals down
                #     add = abs_i - 4
                #     for j in range(1, abs_i - 3 + 1):
                #         pos = Position(og.x - j * factor + add, og.y - j * factor + add)
                #         if (has_resource(map, pos, resource, time_max)):
                #             return pos
                #         pos = Position(og.x + j * factor + add, og.y - j * factor + add)
                #         if (has_resource(map, pos, resource, time_max)):
                #             return pos
        case LocomotionDirection.LEFT | LocomotionDirection.RIGHT:
            if dir == LocomotionDirection.RIGHT:
                factor = 1
                ranging = range(1, 6)
            else:
                factor = -1
                ranging = range(-1, -6, -1)
            forward_max = map.forward_max_x
            backward_max = map.backward_max_x

            for i in ranging: # POIDS : nombre de movements maxi dans notre algo, sinon on fait un gros move aléatoire
                abs_i = abs(i)
                # strict forward
                if abs_i <= forward_max:
                    pos = Position(og.x + i, og.y)
                    if (has_resource(map, pos, resource, time_max)):
                        return pos

                if abs_i >= 2:
                    # lateral
                    pos = Position(og.x, og.y + i + 1)
                    if (has_resource(map, pos, resource, time_max)):
                        return pos
                    pos = Position(og.x, og.y - i - 1)
                    if (has_resource(map, pos, resource, time_max)):
                        return pos

                if abs_i >= 3:
                    # strict backward
                    if i <= backward_max:
                        pos = Position(og.x - i + 2, og.y)
                        if (has_resource(map, pos, resource, time_max)):
                            return pos
                    # diagonals up
                    add = abs_i - 3
                    for j in range(1, abs_i - 2 + 1):
                        pos = Position(og.x + j *factor + add, og.y + j *factor + add)
                        if (has_resource(map, pos, resource, time_max)):
                            return pos
                        pos = Position(og.x + j *factor + add, og.y - j *factor + add)
                        if (has_resource(map, pos, resource, time_max)):
                            return pos
                # if abs_i >= 4:
                #     # diagonals down
                #     add = abs_i - 4
                #     for j in range(1, abs_i - 3 + 1):
                #         pos = Position(og.x - j *factor + add, og.y - j *factor + add)
                #         if (has_resource(map, pos, resource, time_max)):
                #             return pos
                #         pos = Position(og.x - j *factor + add, og.y + j *factor + add)
                #         if (has_resource(map, pos, resource, time_max)):
                #             return pos

    return None

def calculate_nearest(player: Player.Player, resource: ResourceType, time_max: int | None = None) -> Optional[Position]:
    res = __sub_calculate(player, resource, time_max)
    if res is None:
        return res
    return Position(res.x % player.map.max_x, res.y % player.map.max_y)
