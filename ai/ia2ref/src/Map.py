##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Map.py
##

"""
@file Map.py
"""

from __future__ import annotations

from typing import Optional
from time import time
from enum import Enum

from .Locomotion import LocomotionAction, LocomotionDirection, Direction, change_locomotion_direction
from .Constants import PLAYER_DENSITY_DECR, PLAYER_DENSITY_INCR, PLAYER_DENSITY_THRESHOLD

class ResourceType(Enum):
    FOOD = 1
    LINEMATE = 2
    DERAUMERE = 3
    SIBUR = 4
    MENDIANE = 5
    PHIRAS = 6
    THYSTAME = 7
    PLAYER = 8
    EGG = 8

# 8 level * 6 types = 42... Bizarre...
INCANTATION_RESOURCES = {
    2: {ResourceType.PLAYER: 1,  ResourceType.LINEMATE: 1, ResourceType.DERAUMERE: 0, ResourceType.SIBUR: 0, ResourceType.MENDIANE: 0, ResourceType.PHIRAS: 0, ResourceType.THYSTAME: 0},
    3: {ResourceType.PLAYER: 2,  ResourceType.LINEMATE: 1, ResourceType.DERAUMERE: 1, ResourceType.SIBUR: 1, ResourceType.MENDIANE: 0, ResourceType.PHIRAS: 0, ResourceType.THYSTAME: 0},
    4: {ResourceType.PLAYER: 2,  ResourceType.LINEMATE: 2, ResourceType.DERAUMERE: 0, ResourceType.SIBUR: 1, ResourceType.MENDIANE: 0, ResourceType.PHIRAS: 2, ResourceType.THYSTAME: 0},
    5: {ResourceType.PLAYER: 4,  ResourceType.LINEMATE: 1, ResourceType.DERAUMERE: 1, ResourceType.SIBUR: 2, ResourceType.MENDIANE: 0, ResourceType.PHIRAS: 1, ResourceType.THYSTAME: 0},
    6: {ResourceType.PLAYER: 4,  ResourceType.LINEMATE: 1, ResourceType.DERAUMERE: 2, ResourceType.SIBUR: 1, ResourceType.MENDIANE: 3, ResourceType.PHIRAS: 0, ResourceType.THYSTAME: 0},
    7: {ResourceType.PLAYER: 6,  ResourceType.LINEMATE: 1, ResourceType.DERAUMERE: 2, ResourceType.SIBUR: 3, ResourceType.MENDIANE: 0, ResourceType.PHIRAS: 1, ResourceType.THYSTAME: 0},
    8: {ResourceType.PLAYER: 6,  ResourceType.LINEMATE: 2, ResourceType.DERAUMERE: 2, ResourceType.SIBUR: 2, ResourceType.MENDIANE: 2, ResourceType.PHIRAS: 2, ResourceType.THYSTAME: 1},
}

INCANTATION_ACCUMULATION = {ResourceType.FOOD: 10000000000000}
# Accumulate the values for each key
for level, resources in INCANTATION_RESOURCES.items():
    for resource, value in resources.items():
        INCANTATION_ACCUMULATION[resource] = sum([rs[resource] for rs in INCANTATION_RESOURCES.values()]) + 2

def calculate_length_to_see() -> list[int]:
    acc = 0
    return [acc := acc + i for i in range(1, 8 * 2, 2)]


LENGHT_TO_SEE = calculate_length_to_see()


def resourcetype_from_str(resource: str) -> ResourceType:
    match resource:
        case "food":
            return ResourceType.FOOD
        case "linemate":
            return ResourceType.LINEMATE
        case "deraumere":
            return ResourceType.DERAUMERE
        case "sibur":
            return ResourceType.SIBUR
        case "mendiane":
            return ResourceType.MENDIANE
        case "phiras":
            return ResourceType.PHIRAS
        case "thystame":
            return ResourceType.THYSTAME
        case "player":
            return ResourceType.PLAYER
        case "egg":
            return ResourceType.EGG
        case _:
            raise ValueError(f"Unknown resource type : {resource}")

def resourcetype_to_str(resource: ResourceType) -> str:
    match resource:
        case ResourceType.FOOD:
            return "food"
        case ResourceType.LINEMATE:
            return "linemate"
        case ResourceType.DERAUMERE:
            return "deraumere"
        case ResourceType.SIBUR:
            return "sibur"
        case ResourceType.MENDIANE:
            return "mendiane"
        case ResourceType.PHIRAS:
            return "phiras"
        case ResourceType.THYSTAME:
            return "thystame"
        case ResourceType.PLAYER:
            return "player"
        case ResourceType.EGG:
            return "egg"
        case _:
            raise ValueError(f"Unknown resource type : {resource}")


class Tile:
    def __init__(self, x: int, y: int, types: list[ResourceType], time: int = round(time() * 1000)) -> None:
        self.types = types
        self.last_check_time = time
        self.coords: Position = Position(x, y)

    def __str__(self) -> str:
        return f"Tile : {self.coords.x}, {self.coords.y} : {self.types}"


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Position : {self.x}, {self.y}"

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, value: Position) -> bool:
        return self.x == value.x and self.y == value.y

    def __ne__(self, value: Position) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __iter__(self):
        yield self.x
        yield self.y


class Map:
    def __init__(self, x: int, y: int, detect_enemy_base: bool) -> None:
        """
        Inits the map with the given size
        Notice : the player position is not stored in the map but stored in coordinates
        The player position once inited is (x / 2, y / 2)
        """
        if x == y:
            self.max_x = x
            self.max_y = y
        else:
            # since we can't know for sure the direction of the map, we need to store the max x and y
            # WARNING : if the player takes a resource where the place is false duplicate (mirror), the server will tell it's wrong.
            # the ai will be less effective of course.
            # worst case scenario, the difference between x and y is very big, TODO: maybe try other algorithms if that's the case ?
            maxi = max(x, y)
            self.max_x = maxi
            self.max_y = maxi
        self.map: list[list[Optional[Tile]]] = [
            [None for _ in range(self.max_x)] for _ in range(self.max_y)
        ]

        middle_x = self.max_x // 2
        middle_y = self.max_y // 2
        self.player_pos = Position(middle_x, middle_y)
        self.player_dir = LocomotionDirection.UP

        # algorithms
        self.forward_max_x = (middle_x + 1)
        self.backward_max_x = (middle_x - 1)
        self.forward_max_y = (middle_y + 1)
        self.backward_max_y = (middle_y - 1)

        # Explnation : some IA are virus like, we need to take resouce at one point !!
        self.player_density = 0

        self.bases: set[Position] = set()
        self.detect_enemy_base = detect_enemy_base
        if detect_enemy_base:
            self.enemy_bases: set[Position] = set()

    def __str__(self) -> str:
        return str(self.map)

    def add_resource(self, x: int, y: int, resources: list[ResourceType]) -> None:
        self.map[y][x] = Tile(x, y, resources)

    def get_resource(self, x: int, y: int) -> Optional[Tile]:
        return self.map[y % self.max_y][x % self.max_x]

    def get_cur_resource(self):
        return self.map[self.player_pos.y][self.player_pos.x]

    def take_resource(self, resource: ResourceType) -> bool:
        l = self.map[self.player_pos.y][self.player_pos.x]
        if l is None:
            return False
        try:
            l.types.remove(resource)
            return True
        except:
            return False

    def move_player_abs_direction(self, abs_direction: Direction) -> None:
        # the direction is up
        match abs_direction:
            case Direction.SOUTH:
                if self.player_pos.y - 1 < 0:
                    self.player_pos.y = self.max_y - 1
                    return
                self.player_pos.y -= 1
            case Direction.EAST:
                if self.player_pos.x - 1 < 0:
                    self.player_pos.x = self.max_x - 1
                    return
                self.player_pos.x -= 1
            case Direction.NORTH:
                if self.player_pos.y + 1 >= self.max_y:
                    self.player_pos.y = 0
                    return
                self.player_pos.y += 1
            case Direction.WEST:
                if self.player_pos.x + 1 >= self.max_x:
                    self.player_pos.x = 0
                    return
                self.player_pos.x += 1


    def move_player_direction(self, player_dir: LocomotionDirection, direction: Direction) -> None:
        match player_dir:
            case LocomotionDirection.UP:
                self.move_player_abs_direction(direction)
            case LocomotionDirection.DOWN:
                match direction:
                    case Direction.NORTH:
                        self.move_player_abs_direction(Direction.SOUTH)
                    case Direction.WEST:
                        self.move_player_abs_direction(Direction.EAST)
                    case Direction.SOUTH:
                        self.move_player_abs_direction(Direction.NORTH)
                    case Direction.EAST:
                        self.move_player_abs_direction(Direction.WEST)
            case LocomotionDirection.LEFT:
                match direction:
                    case Direction.NORTH:
                        self.move_player_abs_direction(Direction.EAST)
                    case Direction.WEST:
                        self.move_player_abs_direction(Direction.NORTH)
                    case Direction.SOUTH:
                        self.move_player_abs_direction(Direction.WEST)
                    case Direction.EAST:
                        self.move_player_abs_direction(Direction.SOUTH)
            case LocomotionDirection.RIGHT:
                match direction:
                    case Direction.NORTH:
                        self.move_player_abs_direction(Direction.WEST)
                    case Direction.WEST:
                        self.move_player_abs_direction(Direction.SOUTH)
                    case Direction.SOUTH:
                        self.move_player_abs_direction(Direction.EAST)
                    case Direction.EAST:
                        self.move_player_abs_direction(Direction.NORTH)


    def move_player(self, action: LocomotionAction) -> None:
        match action:
            case LocomotionAction.FORWARD:
                match self.player_dir:
                    case LocomotionDirection.UP:
                        if self.player_pos.y + 1 >= self.max_y:
                            self.player_pos.y = 0
                            return
                        self.player_pos.y += 1
                    case LocomotionDirection.RIGHT:
                        if self.player_pos.x + 1 >= self.max_x:
                            self.player_pos.x = 0
                            return
                        self.player_pos.x += 1
                    case LocomotionDirection.DOWN:
                        if self.player_pos.y - 1 < 0:
                            self.player_pos.y = self.max_y - 1
                            return
                        self.player_pos.y -= 1
                    case LocomotionDirection.LEFT:
                        if self.player_pos.x - 1 < 0:
                            self.player_pos.x = self.max_x - 1
                            return
                        self.player_pos.x -= 1
            case LocomotionAction.TURN_LEFT | LocomotionAction.TURN_RIGHT:
                self.player_dir = LocomotionDirection(change_locomotion_direction(
                    self.player_dir, action))
            case _:
                pass

    def add_resources(self, resources: list[list[ResourceType]]):
        match self.player_dir:
            case LocomotionDirection.UP:
                return self.__add_resource_to_map(False, False, resources)
            case LocomotionDirection.RIGHT:
                return self.__add_resource_to_map(True, False, resources)
            case LocomotionDirection.DOWN:
                return self.__add_resource_to_map(False, True, resources)
            case LocomotionDirection.LEFT:
                return self.__add_resource_to_map(True, True, resources)
            case _:
                pass

    def update_db_base(self, new_coords: Position, old_coords: Optional[Position] = None) -> None:
        if old_coords is not None:
            try:
                self.bases.remove(old_coords)
            except KeyError:
                pass
        self.bases.add(new_coords)

    @staticmethod
    def __calculate_ranging(is_x_axis: bool, decrease: bool, i: int):
        if is_x_axis:
            if decrease:
                mini = i - i * 2 - 1
                maxi = i * 2 - i
                return range(maxi, mini, -1)
            else:
                mini = i - i * 2
                maxi = i * 2 - i + 1
                return range(mini, maxi)
        else:
            if decrease:
                mini = i - i * 2
                maxi = i * 2 - i + 1
                return range(mini, maxi)
            else:
                mini = i - i * 2 - 1
                maxi = i * 2 - i
                return range(maxi, mini, -1)

    def __add_resource_to_map(self, is_x_axis: bool, decrease: bool, resources: list[list[ResourceType]]):
        if not resources:
            return
        length = LENGHT_TO_SEE.index(len(resources))
        dec_factor = -1 if decrease else 1
        counter = 0
        cur_time = round(time() * 1000)
        if is_x_axis:
            for i in range(length + 1):
                ranging = self.__calculate_ranging(is_x_axis, decrease, i)
                for j in ranging:
                    y = (self.player_pos.y + j) % self.max_y
                    x = (self.player_pos.x + i * dec_factor) % self.max_x
                    self.__set_tile_resource(x, y, resources[counter], cur_time)
                    counter += 1
        else:
            for i in range(length + 1):
                ranging = self.__calculate_ranging(is_x_axis,decrease, i)
                for j in ranging:
                    y = (self.player_pos.y + i * dec_factor) % self.max_y
                    x = (self.player_pos.x + j) % self.max_x
                    self.__set_tile_resource(x, y, resources[counter], cur_time)
                    counter += 1

    def __set_tile_resource(self, x: int, y: int, resources: list[ResourceType], cur_time: int):
        tile_ptr = self.map[y][x]
        if not resources:
            tile_ptr = None
            self.player_density = max(0, self.player_density - PLAYER_DENSITY_DECR)
        else:
            # TODO : maybe directly modify the list instead of checking each time the date
            if tile_ptr is not None and tile_ptr.last_check_time == cur_time:
                return
            tile_density = resources.count(ResourceType.PLAYER)
            if tile_density > 0 + (1 if x == self.player_pos.x and y == self.player_pos.y else 0):
                incr_density = PLAYER_DENSITY_INCR * tile_density
                self.player_density += incr_density
                if incr_density >= PLAYER_DENSITY_THRESHOLD and self.detect_enemy_base:
                    pos = Position(x, y)
                    if self.bases and pos not in self.bases:
                        self.enemy_bases.add(pos) # there is an unknown incentation going on !!!
                        self.player_density -= incr_density
            else:
                self.player_density = max(0, self.player_density - PLAYER_DENSITY_DECR)
            self.map[y][x] = Tile(x, y, resources, cur_time)
