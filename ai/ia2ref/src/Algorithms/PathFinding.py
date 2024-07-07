##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# PathFinding.py
##

"""
@file PathFinding.py
"""

from ..Locomotion import LocomotionAction, LocomotionDirection
from ..Map import Position

def get_d(start: int, dest: int, maxi: int) -> tuple[int, int]:
    if start == dest:
        return (0, 0)

    a = dest - start
    x = (a, abs(a))

    b = (maxi - start) + dest
    y = (b, abs(b))

    c = (maxi - dest) + start
    z = (-c, abs(c))

    mini = min(x[1], y[1], z[1])
    if mini == x[1]:
        return x
    if mini == y[1]:
        return y
    return z


def get_action_x(actions, current_direction, dx, abs_dx) -> LocomotionDirection:
    if dx < 0:
        match current_direction:
            case LocomotionDirection.UP:
                actions.append(LocomotionAction.TURN_RIGHT)
            case LocomotionDirection.DOWN:
                actions.append(LocomotionAction.TURN_LEFT)
            case LocomotionDirection.RIGHT:
                actions.append(LocomotionAction.TURN_LEFT)
                actions.append(LocomotionAction.TURN_LEFT)
        actions.extend([LocomotionAction.FORWARD] * abs_dx)
        return LocomotionDirection.LEFT
    elif dx > 0:
        match current_direction:
            case LocomotionDirection.UP:
                actions.append(LocomotionAction.TURN_LEFT)
            case LocomotionDirection.DOWN:
                actions.append(LocomotionAction.TURN_RIGHT)
            case LocomotionDirection.LEFT:
                actions.append(LocomotionAction.TURN_LEFT)
                actions.append(LocomotionAction.TURN_LEFT)
        actions.extend([LocomotionAction.FORWARD] * dx)
        return LocomotionDirection.RIGHT
    return current_direction


def get_action_y(actions, current_direction, dy, abs_dy):
    if dy < 0:
        match current_direction:
            case LocomotionDirection.RIGHT:
                actions.append(LocomotionAction.TURN_LEFT)
            case LocomotionDirection.LEFT:
                actions.append(LocomotionAction.TURN_RIGHT)
            case LocomotionDirection.UP:
                actions.append(LocomotionAction.TURN_LEFT)
                actions.append(LocomotionAction.TURN_LEFT)
        actions.extend([LocomotionAction.FORWARD] * abs_dy)
        return LocomotionDirection.DOWN
    elif dy > 0:
        match current_direction:
            case LocomotionDirection.RIGHT:
                actions.append(LocomotionAction.TURN_RIGHT)
            case LocomotionDirection.LEFT:
                actions.append(LocomotionAction.TURN_LEFT)
            case LocomotionDirection.DOWN:
                actions.append(LocomotionAction.TURN_LEFT)
                actions.append(LocomotionAction.TURN_LEFT)
        actions.extend([LocomotionAction.FORWARD] * dy)
        return LocomotionDirection.UP
    return current_direction


def calculate_shortest_path(
    current_direction: LocomotionDirection,
    start: Position, dest: Position,
    max_x: int, max_y: int
):
    """
    Returns the shortest path to go from start to dest
    This supports cirucular maps
    Normally, the current_direction should changed when the command is executed
    """
    if start.x == dest.x and start.y == dest.y:
        return []

    dx, abs_dx = get_d(start.x, dest.x, max_x)
    dy, abs_dy = get_d(start.y, dest.y, max_y)

    actions: list[LocomotionAction] = []
    if current_direction == LocomotionDirection.UP or current_direction == LocomotionDirection.DOWN:
        current_direction = get_action_y(
            actions, current_direction, dy, abs_dy)
        get_action_x(
            actions, current_direction, dx, abs_dx)
    else:
        current_direction = get_action_x(
            actions, current_direction, dx, abs_dx)
        get_action_y(
            actions, current_direction, dy, abs_dy)

    return actions
