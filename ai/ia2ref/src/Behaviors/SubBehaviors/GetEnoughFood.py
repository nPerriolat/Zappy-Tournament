##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# GetEnoughFood.py
##

"""
@file GetEnoughFood.py
"""
from __future__ import annotations

from typing import Optional

from ... import Player
from ...Behavior import ABehavior
from ..Action import Command, IAction, ActionResultType
from ..Actions.Broadcast import Broadcast
from ...Map import ResourceType

from ...Communications.Broadcasts.Ready import CDSendReady

from .SearchAndFind import SearchAndFind


class GetEnoughFood(ABehavior):
    def __init__(self, player: Player.Player, thres_max: int):
        super().__init__()

        self.thres_max = thres_max
        self.unique_behavior = SearchAndFind(thres_max=thres_max)
        self.unique_action = Broadcast(CDSendReady(player.my_drone.jefe_pid))
        self.action_status = ActionResultType.NONE

        self.should_wait = True

    def update(self, player: Player.Player) -> Optional[Command]:
        if self.finished:
            return None
        if not self.unique_behavior.is_finished():
            return self.unique_behavior.update(player)

        res, behavior = self.unique_behavior.finish(player)
        if res != ActionResultType.DONE:
            if behavior is None:
                self.unique_behavior = SearchAndFind(thres_max=self.thres_max)
            else:
                self.unique_behavior = behavior
            return None

        self.action_status = self.unique_action.update(player)
        return self.unique_action.get_cur_command()

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if not self.unique_behavior.is_finished():
            return self.unique_behavior.post(player, callback_result)

        if callback_result is None:
            return
        self.action_status = self.unique_action.post(player, callback_result)
        if self.action_status == ActionResultType.DONE:
            self.finished = True

    def handle_eject(self, player, direction):
        if not self.unique_behavior.is_finished():
            return self.unique_behavior.handle_eject(player, direction)
        super().handle_eject(player, direction)

    def wants_to_wait(self) -> bool:
        if not self.unique_behavior.is_finished():
            return self.unique_behavior.wants_to_wait()
        return self.should_wait and (self.action_status == ActionResultType.CONTINUE)

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        return (ActionResultType.DONE, None)
