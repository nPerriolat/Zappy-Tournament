##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Actions.py
##

from __future__ import annotations

from typing import Callable, Optional
from enum import Enum

from ..Utils.OrderedEnum import OrderedEnum
from .. import Player


class ActionResultType(Enum):
    NONE = -1
    CONTINUE = 0			# continue executing this action next frame - nothing has changed
    CHANGE_TO = 1			# change actions next frame
    SUSPEND_FOR = 2		    # put the current action on hold for the new action
    DONE = 3				# this action has finished, resume suspended action
    SUSTAIN = 4			    # for use with event handlers - a way to say "It's important to keep doing what I'm doing"
    GIVE_UP = 5			    # stop everything, drone is dead anyway
    WAIT_POST = 6           # Wait for the post


class EventResultPriorityType(OrderedEnum):
    RESULT_NONE = 0		        # no result
    RESULT_TRY = 1			    # use this result, or toss it out, either is ok
    RESULT_IMPORTANT = 2        # try extra-hard to use this result
    RESULT_CRITICAL = 3         # this result must be used - emit an error if it can't be
    RESULT_CRITICAL_WIPE = 4    # this result must be used, and all other actions are removed


class QueryResultType(Enum):
    ANSWER_UNDECIDED = -1      # no answer has been given yet
    ANSWER_NO = 0
    ANSWER_YES = 1

class IncantationStatus(Enum):
    NONE = -1
    WAIT = 1
    FINISH = 2
    BAD = 3


class Command:
    def __init__(self, payload: str, time: int, parse_result_callback: Callable[[str], bool | list[str] | int]) -> None:
        self.payload = payload
        self.time = time
        self.parse_callback = parse_result_callback


class IAction:
    def __init__(self, time: int, name: str = ""):
        self.name = name
        self.time = time
        self.cur_command = Command("", 0, lambda x: False)
        self.done = False

    def update(self, player: Player.Player) -> ActionResultType: # type: ignore
        pass

    def post(self, player, result: bool | list[str] | int) -> ActionResultType:  # type: ignore
        pass

    def get_cur_command(self) -> Command:
        return self.cur_command


class AActionResult:
    def __init__(self, type: ActionResultType = ActionResultType.CONTINUE, action: Optional[IAction] = None, reason: str = "") -> None:
        self.type = type
        self.action = action
        self.reason = reason


class ActionResult(AActionResult):
    def __init__(self, type: ActionResultType = ActionResultType.CONTINUE, action: Optional[IAction] = None, reason: str = ""):
        super().__init__(type, action, reason)


class EventDiseredResult(AActionResult):
    def __init__(self, priority: EventResultPriorityType, type: ActionResultType = ActionResultType.CONTINUE, action: Optional[IAction] = None, reason: str = ""):
        super().__init__(type, action, reason)
        self.priority = priority
