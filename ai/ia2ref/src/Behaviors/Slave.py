##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Slave.py
##

"""
@file Slave.py
"""
from __future__ import annotations

from typing import Optional

from .. import Player
from ..Behavior import ABehavior

from ..BehaviorScheduler import SubBehaviorScheduler
from .Action import Command, ActionResultType
from ..Map import ResourceType
from ..Communications.Communication import CommunicationRecv
from ..Communications.CommunicationType import CommunicationType
from ..Communications.Broadcasts.MasterMoveToMe import CDRecvMoveToMe, CDRecvMoveBase

from .SubBehaviors.SearchAndFind import SearchAndFind
from .SubBehaviors.GetEnoughFood import GetEnoughFood
from .SubBehaviors.Incantation import SoloIncantation
from .SubBehaviors.IncantationShared import IncantationSharedSlave
from .SubBehaviors.NewSpawn import NewSpawnSlave
from .SubBehaviors.MoveToBroadcaster import MoveToBroadcaster

from ..Constants import READY_MAX_THRESHOLD, FOOD_MULTIPLIER


class Slave(ABehavior):
    def __init__(self, jefe_pid: int, is_fast_spawn: bool = False):
        super().__init__()

        self.cur_childs = 0
        if not is_fast_spawn:
            def_search_and_find = SearchAndFind(thres_max=150)
            new_spawn = NewSpawnSlave(jefe_pid)
            self.behaviors = SubBehaviorScheduler(
                first_behavior=new_spawn, default_behavior=def_search_and_find)
        else:
            saf = SearchAndFind(
                    ResourceType.LINEMATE, 1, 100, take=False)
            self.behaviors = SubBehaviorScheduler(first_behavior=saf, default_behavior=saf)

        self.told_im_spawned = is_fast_spawn
        self.is_in_base = False
        self.moving = False
        self.moving_demand: Optional[CDRecvMoveToMe] = None
        self.awaiting_order = False
        self.send_ready = False
        self.went_get_enough_food = False

    def update(self, player: Player.Player) -> Optional[Command]:
        is_done, command = self.behaviors.update(player)
        if is_done == ActionResultType.CONTINUE or is_done == ActionResultType.NONE:
            return command

        if not self.told_im_spawned:
            if is_done == ActionResultType.DONE:
                self.told_im_spawned = True
                self.behaviors.set_cur_behavior(SearchAndFind(
                    ResourceType.LINEMATE, 1, 100, take=False))
        elif not player.my_drone.unwanted_incant and player.my_drone.level == 1:
            self.behaviors.set_cur_behavior(SoloIncantation())
        elif not self.is_in_base:
            if self.moving_demand is None or not self.awaiting_order:
                if not self.went_get_enough_food or player.get_life() < READY_MAX_THRESHOLD:
                    self.behaviors.set_cur_behavior(GetEnoughFood(
                        player, READY_MAX_THRESHOLD + 2 * FOOD_MULTIPLIER))
                    self.went_get_enough_food = True
                else:
                    self.awaiting_order = True
                    self.behaviors.set_cur_behavior(SearchAndFind())
            else:
                self.moving = True
                self.behaviors.set_cur_behavior(
                    MoveToBroadcaster(player, self.moving_demand))
                self.is_in_base = True
        elif player.my_drone.level < 8:
            self.behaviors.set_cur_behavior(IncantationSharedSlave(player))
        else:
            # ==> https://music.youtube.com/watch?v=1HqpFoHv6qg
            self.behaviors.set_cur_behavior(SearchAndFind(
                thres_max=800 * FOOD_MULTIPLIER, should_pick_random=False))
        return None

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return
        self.behaviors.post(player, callback_result)

    def handle_eject(self, player, direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        self.behaviors.handle_eject(player, direction)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        if not self.moving \
                and self.moving_demand is None \
                and recv.type == CommunicationType.MOVE_TO_ME:
            # automatically set the diff between drone's base_coords and new ones
            deco_recv = CDRecvMoveToMe(recv)
            if not deco_recv.unpack(player):
                raise RuntimeError("Failed to unpack MOVE_TO_COORDS")
            if not deco_recv.concerned:  # don't care
                return False
            if self.awaiting_order:
                self.moving = True
                self.behaviors.set_cur_behavior(
                    MoveToBroadcaster(player, deco_recv))
                self.is_in_base = True
            else:
                self.moving_demand = deco_recv
            # DON'T RETURN

        if self.behaviors.handle_broadcast(player, recv):
            return True

        return False

    def wants_to_wait(self) -> bool:
        return self.behaviors.wants_to_wait()

    def have_to_wait(self) -> bool:
        return self.behaviors.have_to_wait()
