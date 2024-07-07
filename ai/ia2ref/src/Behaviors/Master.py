##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# Master.py
##

"""
@file Master.py
"""
from __future__ import annotations

from typing import Optional

from .. import Player
from ..Behavior import ABehavior

from ..BehaviorScheduler import SubBehaviorScheduler
from .Action import Command, ActionResultType
from ..Map import ResourceType

from .SubBehaviors.SearchAndFind import SearchAndFind
from .SubBehaviors.Incantation import SoloIncantation
from .SubBehaviors.IncantationShared import IncantationSharedMaster
from .SubBehaviors.MoveToBroadcaster import MoveToMe
from ..Communications.Communication import CommunicationRecv
from ..Communications.CommunicationType import CommunicationType
from ..Communications.Broadcasts.Ready import CDRecvReady
from .SubBehaviors.NewSpawn import NewSpawnMaster

from ..Constants import MASTER_MIN_FORKS


class Master(ABehavior):
    def __init__(self, player: Player.Player, nb_connects: int):
        super().__init__()

        self.cur_childs = 0
        def_search_and_find = SearchAndFind(thres_max=150)
        search_and_find = SearchAndFind(
            ResourceType.LINEMATE, 1, 100, take=False)
        self.behaviors = SubBehaviorScheduler(
            first_behavior=search_and_find, default_behavior=def_search_and_find)

        self.nb_forks = min(nb_connects - 1, MASTER_MIN_FORKS)
        self.min_forks = MASTER_MIN_FORKS
        self.nb_ready = 0
        for _ in range(self.nb_forks):
            pid = player.fork(True)
            if pid is not None and pid != -1:
                player.other_drones[pid] = Player.Drone(
                    pid, Player.PlayerRole.SLAVE, player.my_drone.pid)

        self.give_enough_birth = self.nb_forks >= self.min_forks
        self.gathered_everyone = False

    def update(self, player: Player.Player) -> Optional[Command]:
        is_done, command = self.behaviors.update(player)
        if is_done == ActionResultType.CONTINUE or is_done == ActionResultType.NONE:
            return command

        if player.my_drone.level == 1:
            self.behaviors.set_cur_behavior(
                SoloIncantation())  # solo incantation
        elif not self.give_enough_birth:
            if is_done == ActionResultType.DONE:
                self.behaviors.set_cur_behavior(NewSpawnMaster())
                self.nb_forks += 1
                self.give_enough_birth = self.nb_forks >= self.min_forks
            else:
                self.behaviors.set_cur_behavior(SearchAndFind(thres_max=400))
        elif self.nb_ready != self.min_forks and not self.gathered_everyone:
            # wait for readiness of child drones
            self.behaviors.set_cur_behavior(SearchAndFind())
        elif player.my_drone.level < 8:
            if not self.gathered_everyone:
                self.behaviors.set_cur_behavior(MoveToMe(
                    player, player.my_drone.base_coords if player.my_drone.knows_base else None))
                self.gathered_everyone = True
            else:
                self.behaviors.set_cur_behavior(
                    IncantationSharedMaster(player, self.nb_forks))
        else:
            self.behaviors.set_cur_behavior(SearchAndFind(
                thres_max=900, should_pick_random=False))
        return None

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return
        self.behaviors.post(player, callback_result)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        if self.nb_ready != self.min_forks and recv.type == CommunicationType.READY:
            # automatically set the diff between drone's base_coords and new ones
            deco_recv = CDRecvReady(recv)
            if not deco_recv.unpack(player):
                raise RuntimeError("Failed to unpack MOVE_TO_COORDS")
            if not deco_recv.concerned:  # don't care
                return False
            if deco_recv.ready:
                self.nb_ready += 1
                if self.nb_ready == self.min_forks:
                    self.behaviors.set_cur_behavior(MoveToMe(
                        player, player.my_drone.base_coords if player.my_drone.knows_base else None))
                    self.gathered_everyone = True
            else:
                self.nb_ready = min(0, self.nb_ready - 1)

        if self.behaviors.handle_broadcast(player, recv):
            return True
        return False

    def handle_eject(self, player, direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        self.behaviors.handle_eject(player, direction)

    def wants_to_wait(self) -> bool:
        return self.behaviors.wants_to_wait()

    def have_to_wait(self) -> bool:
        return self.behaviors.have_to_wait()
