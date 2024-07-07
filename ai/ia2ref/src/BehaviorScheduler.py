##
# EPITECH PROJECT, 2023
# zappy [Dev Container: zappy_docker @ unix:///run/user/1002/docker.sock]
# File description:
# BehaviorScheduler.py
##

"""
@file BehaviorScheduler.py
"""

from __future__ import annotations

from collections import deque
from typing import Optional

from .Behavior import ABehavior
from .Behaviors.Action import ActionResultType
from . import Player
from .Locomotion import Direction
from .Behaviors.Action import Command
from .Communications.Communication import CommunicationRecv


class BehaviorScheduler:
    def __init__(self, first_behavior: ABehavior, default_behavior: ABehavior) -> None:
        """
        Player can only have this scheuler
        The default behavior is the most parent behavior, like Master behavior
        """
        self.default_behavior = default_behavior
        self.cur_behavior: ABehavior = first_behavior
        self.behavior_stack: deque[ABehavior] = deque()

    def update(self, player: Player.Player, callback_results: Optional[list[bool | list[str] | int]], push_dirs: list[Direction]) -> Optional[Command]:
        if callback_results is not None:
            if len(callback_results) > 1:
                print("ERROR: Unintended behavior, multiple callback results in one update call.", callback_results)
            for res in callback_results:
                self.cur_behavior.post(player, res)
        for dir in push_dirs:
            self.cur_behavior.handle_eject(player, dir)
        broadcasts = player.controller.broadcastHandler.pop_broadcasts()
        for broadcast in broadcasts:
            self.cur_behavior.handle_broadcast(player, broadcast)
        _, command = self._update_current(player)
        return command

    def set_cur_behavior(self, behavior: ABehavior):
        self.cur_behavior = behavior
        self.behavior_stack.clear()

    def wants_to_wait(self) -> bool:
        return self.cur_behavior.wants_to_wait()

    def have_to_wait(self) -> bool:
        return self.cur_behavior.have_to_wait()

    ## PRIVATE METHODS ##

    def _update_current(self, player: Player.Player) -> tuple[ActionResultType, Optional[Command]]:
        command = self.cur_behavior.update(player)
        action_res = ActionResultType.NONE
        if self.cur_behavior.is_finished():
            action_res, next_behavior = self.cur_behavior.finish(player)
            if action_res != ActionResultType.CONTINUE:
                action_res = self._handle_behavior_change(
                    player, action_res, next_behavior)
        if command is not None and command.payload == "":
            return (action_res, None)
        return action_res, command

    def _handle_behavior_change(self, player: Player.Player, action_res: ActionResultType, next_behavior: Optional[ABehavior]) -> ActionResultType:
        match action_res:
            case ActionResultType.CHANGE_TO:  # we imagine what's behind is not important
                if next_behavior is None:
                    return ActionResultType.CHANGE_TO
                self.cur_behavior = next_behavior
                self.behavior_stack.clear()
            case ActionResultType.SUSPEND_FOR: # should never none
                self.cur_behavior.was_suspended = True
                if next_behavior is not None:
                    self.behavior_stack.appendleft(self.cur_behavior)
                    self.cur_behavior = next_behavior
            case ActionResultType.DONE:
                if next_behavior is None:
                    if len(self.behavior_stack) == 0:
                        # self.cur_behavior = self.default_behavior
                        return ActionResultType.DONE
                    self.cur_behavior = self.behavior_stack.pop()
                    self.cur_behavior.finish_suspended(player)
                    return ActionResultType.CONTINUE
                # keep the stack intact, just change the current behavior
                self.cur_behavior = next_behavior
        return ActionResultType.CONTINUE


class SubBehaviorScheduler(BehaviorScheduler):
    """
    @brief SubBehaviorScheduler class used by ABehaviors
    """

    def __init__(self, first_behavior: ABehavior, default_behavior: ABehavior) -> None:
        super().__init__(first_behavior, default_behavior)

    def update(self, player: Player.Player) -> tuple[ActionResultType, Optional[Command]]:
        return self._update_current(player)

    def post(self, player: Player.Player, callback_result: bool | list[str] | int):
        self.cur_behavior.post(player, callback_result)

    def handle_eject(self, player: Player.Player, direction: Direction):
        self.cur_behavior.handle_eject(player, direction)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        # suspended process must know what's happening
        for behavior in reversed(self.behavior_stack):
            # TODO: create system to cancel suspended process
            if behavior.handle_broadcast(player, recv):
                return True
        return self.cur_behavior.handle_broadcast(player, recv)
