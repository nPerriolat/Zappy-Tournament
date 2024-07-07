##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Locomotion.py
##

"""
@file Locomotion.py
"""

from enum import Enum


class LocomotionAction(Enum):
    FORWARD = 0
    TURN_LEFT = 1
    TURN_RIGHT = 2


class LocomotionDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Direction(Enum):
    SAME_TILE = -1
    NORTH = 0
    NORTH_EAST = 1
    EAST = 2
    SOUTH_EAST = 3
    SOUTH = 4
    SOUTH_WEST = 5
    WEST = 6
    NORTH_WEST = 7


def get_direction_from_str(direction: str) -> Direction:
    """
    Direction is already relative to current direction
    """
    match direction:
        case "0":
            return Direction.SAME_TILE
        case "1":
            return Direction.NORTH
        case "2":
            return Direction.NORTH_WEST
        case "3":
            return Direction.WEST
        case "4":
            return Direction.SOUTH_WEST
        case "5":
            return Direction.SOUTH
        case "6":
            return Direction.SOUTH_EAST
        case "7":
            return Direction.EAST
        case _: # "8"
            return Direction.NORTH_EAST

def get_absolute_direction(direction: Direction, current_direction: LocomotionDirection) -> Direction:
    match current_direction:
        case LocomotionDirection.UP:
            return direction
        case LocomotionDirection.RIGHT:
            return Direction((direction.value + 2) % 8)
        case LocomotionDirection.DOWN:
            return Direction((direction.value + 4) % 8)
        case LocomotionDirection.LEFT:
            return Direction((direction.value + 6) % 8)

def get_reversed_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.SAME_TILE:
            return Direction.SAME_TILE
        case Direction.NORTH:
            return Direction.SOUTH
        case Direction.NORTH_EAST:
            return Direction.SOUTH_WEST
        case Direction.EAST:
            return Direction.WEST
        case Direction.SOUTH_EAST:
            return Direction.NORTH_WEST
        case Direction.SOUTH:
            return Direction.NORTH
        case Direction.SOUTH_WEST:
            return Direction.NORTH_EAST
        case Direction.WEST:
            return Direction.EAST
        case Direction.NORTH_WEST:
            return Direction.SOUTH_EAST

def change_locomotion_direction(og_dir: LocomotionDirection, action: LocomotionAction) -> LocomotionDirection:
    match action:
        case LocomotionAction.TURN_LEFT:
            match og_dir:
                case LocomotionDirection.UP:
                    return LocomotionDirection.RIGHT
                case LocomotionDirection.RIGHT:
                    return LocomotionDirection.DOWN
                case LocomotionDirection.DOWN:
                    return LocomotionDirection.LEFT
                case LocomotionDirection.LEFT:
                    return LocomotionDirection.UP
        case LocomotionAction.TURN_RIGHT:
            match og_dir:
                case LocomotionDirection.UP:
                    return LocomotionDirection.LEFT
                case LocomotionDirection.RIGHT:
                    return LocomotionDirection.UP
                case LocomotionDirection.DOWN:
                    return LocomotionDirection.RIGHT
                case LocomotionDirection.LEFT:
                    return LocomotionDirection.DOWN
        case _:
            raise RuntimeError("Invalid action")

def locomotion_direction_to_direction(dir: LocomotionDirection):
    match dir:
        case LocomotionDirection.UP:
            return Direction.NORTH
        case LocomotionDirection.RIGHT:
            return Direction.EAST
        case LocomotionDirection.DOWN:
            return Direction.SOUTH
        case LocomotionDirection.LEFT:
            return Direction.WEST
        case _:
            raise RuntimeError("Invalid direction")

def direction_to_locomotion_direction(dir: Direction):
    match dir:
        case Direction.NORTH:
            return LocomotionDirection.UP
        case Direction.EAST:
            return LocomotionDirection.RIGHT
        case Direction.SOUTH:
            return LocomotionDirection.DOWN
        case Direction.WEST:
            return LocomotionDirection.LEFT
        case _:
            raise RuntimeError("Invalid direction")
