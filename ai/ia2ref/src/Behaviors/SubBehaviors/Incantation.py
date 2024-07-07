##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Incantation.py
##

"""
@file Incantation.py
"""
from __future__ import annotations

from typing import Optional

from ... import Player
from ...Behavior import ABehavior
from ..Action import Command, IAction, ActionResultType
from ...Map import ResourceType

from ...Constants import INCANTATION_ABANDON_THRESHOLD_FOOD, INCANTATION_MIN_FOOD
from ..Actions.Incantation import Incantation as IncantationAction
from .SearchAndFind import SearchAndFind


class SoloIncantation(ABehavior):
    def __init__(self):
        super().__init__()

        self.__reset()

        self.should_wait = True

        self.finish_abandonned = False

    def update(self, player: Player.Player) -> Optional[Command]:
        if self.finished:
            return None

        if self.action_status == ActionResultType.CHANGE_TO:
            if not player.my_drone.unwanted_incant:
                self.finish_abandonned = False
            else:
                player.my_drone.unwanted_incant = False
            self.finished = True
            return None
        elif player.get_life() < INCANTATION_ABANDON_THRESHOLD_FOOD:
            self.finish_abandonned = True
            self.finished = True
            return None

        self.action_status = self.unique_action.update(player)
        return self.unique_action.get_cur_command()

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return

        self.action_status = self.unique_action.post(
            player, callback_result)
        if self.action_status == ActionResultType.DONE:
            self.finished = True

    def handle_eject(self, player, direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        super().handle_eject(player, direction)
        self.__reset()

    def wants_to_wait(self) -> bool:
        return self.should_wait and (self.action_status == ActionResultType.CONTINUE)

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        if self.finish_abandonned:  # failed, need to find another linemate
            return (ActionResultType.SUSPEND_FOR, SearchAndFind(ResourceType.FOOD, INCANTATION_MIN_FOOD, -1, should_pick_random=False))
        return (ActionResultType.DONE, None)

    def finish_suspended(self, player: Player.Player):
        self.__reset()
        self.finish_abandonned = False
        return super().finish_suspended(player)

    ## Private ##

    def __reset(self):
        self.unique_action = IncantationAction()
        self.action_status = ActionResultType.NONE
