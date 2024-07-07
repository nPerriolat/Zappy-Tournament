##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# See.py
##

"""
@file See.py
"""

from __future__ import annotations

from ...Behaviors.Action import IAction
from ...Map import Map, ResourceType, resourcetype_from_str
from ... import Player
from ...Behaviors.Action import ActionResultType, IAction

from ..Commands import Com_Look


class See(IAction):
    def __init__(self):
        super().__init__(-1, "See")

    def update(self, player: Player.Player) -> ActionResultType:
        command = Com_Look()
        if player.get_life() < command.time:
            return ActionResultType.GIVE_UP

        self.cur_command = command
        return ActionResultType.CONTINUE

    def post(self, player: Player.Player, result: bool | list[str] | int) -> ActionResultType:
        if not result:
            return ActionResultType.CONTINUE  # wtf ? try again
        player.map.add_resources(self.__parse_payload(result))  # type: ignore
        return ActionResultType.DONE

    def __parse_payload(self, result: list[str]) -> list[list[ResourceType]]:
        try:
            return [[resourcetype_from_str(resource.strip()) for resource in resources.split(' ') if resource.strip() != ''] for resources in result]
        except Exception as e:
            print("Error See:", e, f"({result})")
            return []
