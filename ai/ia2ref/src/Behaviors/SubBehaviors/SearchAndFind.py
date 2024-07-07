##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# SearchAndFind.py
##

"""
@file SearchAndFind.py
"""
from __future__ import annotations

from typing import Optional
from random import randint
from collections import deque

from ... import Player
from ...Behavior import ABehavior
from ..Action import Command, IAction, ActionResultType
from ..Actions.Move import Move
from ..Actions.See import See
from ..Actions.Take import Take
from ..Actions.Turn import Turn

from ...Map import ResourceType, Position, INCANTATION_ACCUMULATION
from ...Locomotion import LocomotionAction
from ...Constants import ABANDON_THRESHOLD_FOOD, NB_TIME_PICK_RANDOM_RESOURCES, ABSOLUTE_MIN_FOOD_THRES_RANDOM_RESOURCES

from ...Algorithms.Nearest import calculate_nearest


class SearchAndFind(ABehavior):
    def __init__(self, resouce_type: ResourceType = ResourceType.FOOD, thres_max: int = -1, thres_abandon_food: int = -1, take: bool = True, should_pick_random: bool = True):
        super().__init__()

        self.actions: deque[IAction] = deque()
        self.action_status = ActionResultType.NONE

        self.has_see = False
        self.is_moving = False
        self.has_found_food = False
        self.nb_turning = 0
        self.resouce_type = resouce_type
        self.thres_max = thres_max
        self.thres_abandon_food = thres_abandon_food

        self.should_pick_random = should_pick_random
        self.should_take_resource = take

        self.finish_abandonned = False
        self.should_wait = True

    def update(self, player: Player.Player) -> Optional[Command]:
        if self.action_status == ActionResultType.CONTINUE:
            return self.__send_command(player)

        if self.actions:
            self.actions.popleft()

        if self.thres_max != -1 and player.get_inventory()[self.resouce_type] >= self.thres_max:
            self.finish_abandonned = False
            self.finished = True
            return None
        if self.thres_abandon_food != -1 and player.get_life() <= self.thres_abandon_food:
            self.__reset()
            self.finish_abandonned = True
            self.finished = True
            return None

        if not self.actions:
            if not self.has_see:
                self.has_see = True
                self.actions.append(See())
            elif self.has_see and not self.is_moving:
                if not self.__find_the_food(player):  # sets the action
                    if self.nb_turning >= 3:
                        self.nb_turning = 0
                        coords = Position((player.map.player_pos.x + randint(-4, 4)) % player.map.max_x,
                                          (player.map.player_pos.y + randint(-4, 4)) % player.map.max_y)
                        self.actions.append(Move(
                            player.map.player_pos, coords, player.map.player_dir,
                            player.map.max_x, player.map.max_y))
                        self.is_moving = True
                        self.has_found_food = False
                    else:
                        self.has_see = False
                        self.actions.append(Turn(
                            LocomotionAction.TURN_LEFT, player.map.player_dir))
                        self.nb_turning += 1
                else:
                    self.nb_turning = 0
                    self.is_moving = True
                    self.has_found_food = True
                if self.should_pick_random:
                    tile = player.map.get_cur_resource()
                    if tile is not None:
                        tile_filtered = [x for x in tile.types if x !=
                                         self.resouce_type and x != ResourceType.PLAYER]
                        # because player is on it
                        tile_len = len(tile_filtered)
                        for i in range(min(NB_TIME_PICK_RANDOM_RESOURCES, tile_len)):
                            res = tile_filtered[i]
                            if player.get_inventory()[res] >= INCANTATION_ACCUMULATION[res]:
                                continue
                            if player.get_life() - 7 * i <= ABSOLUTE_MIN_FOOD_THRES_RANDOM_RESOURCES:
                                break
                            self.actions.appendleft(Take(tile_filtered[i]))
            elif self.is_moving:
                self.is_moving = False
                if self.has_found_food and self.action_status == ActionResultType.DONE:
                    if self.should_take_resource:
                        self.has_see = False
                        self.actions.append(Take(self.resouce_type))
                    else:  # example : used for getting to the linemate for level 1, don't take it
                        self.finish_abandonned = False
                        self.finished = True
                        return None
                else:
                    self.actions.append(See())

        return self.__send_command(player)

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return

        self.action_status = self.actions[0].post(player, callback_result)

    def handle_eject(self, player, direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        super().handle_eject(player, direction)
        # reset everything
        self.action_status = ActionResultType.CHANGE_TO
        self.__reset()

    def wants_to_wait(self) -> bool:
        return self.should_wait and (self.action_status != ActionResultType.NONE)

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        if self.finish_abandonned:
            return (ActionResultType.SUSPEND_FOR, SearchAndFind(ResourceType.FOOD, ABANDON_THRESHOLD_FOOD, -1))
        return (ActionResultType.DONE, None)

    ## PRIVATE ##

    def __reset(self):
        self.has_see = False
        self.is_moving = False
        self.has_found_food = False
        self.nb_turning = 0
        self.actions.clear()

    def __find_the_food(self, player: Player.Player) -> bool:
        res = calculate_nearest(player, self.resouce_type)
        if not res:
            return False
        self.actions.append(Move(
            player.map.player_pos, res, player.map.player_dir,
            player.map.max_x, player.map.max_y))
        return True

    def __send_command(self, player: Player.Player) -> Optional[Command]:
        self.action_status = self.actions[0].update(player)
        if self.action_status == ActionResultType.GIVE_UP:
            raise RuntimeError("I can't do it anymore...")
        return self.actions[0].get_cur_command()
