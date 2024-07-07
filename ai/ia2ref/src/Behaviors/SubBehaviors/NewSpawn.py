##
# EPITECH PROJECT, 2023
# zappy [Dev Container: zappy_docker @ unix:///run/user/1002/docker.sock]
# File description:
# NewSpawn.py
##

"""
@file NewSpawn.py
"""

from __future__ import annotations

from typing import Optional

from ... import Player
from ...Behavior import ABehavior
from ..Action import Command, ActionResultType
from ...Map import ResourceType
from ...Utils.OSUtils import get_pid


from ...Communications.Communication import CommunicationRecv
from ...Communications.CommunicationType import CommunicationType
from ...Communications.Broadcasts.InitSpawn import CDRecvInitSpawn, CDSendInitSpawn
from ...Communications.Broadcasts.ISpawn import CDRecvISpawn, CDSendISpawn
from ...Communications.Broadcasts.Acknowledge import CDRecvAcknowledge, CDSendAcknowledge

from ..Actions.Broadcast import Broadcast
from ..Actions.Fork import Fork
from .SearchAndFind import SearchAndFind


class NewSpawnSlave(ABehavior):
    def __init__(self, jefe_pid: int):
        super().__init__()

        self.unique_action = Broadcast(CDSendISpawn(jefe_pid))
        self.action_status = ActionResultType.NONE

        self.sent_spawn_info = False
        self.sent_ack = False

        self.finish_abandonned = False

        self.should_wait = True

    def update(self, player: Player.Player) -> Optional[Command]:
        if self.action_status == ActionResultType.CONTINUE:
            self.action_status = self.unique_action.update(player)
            return self.unique_action.get_cur_command()

        if self.action_status == ActionResultType.DONE:
            if not self.sent_spawn_info:
                self.sent_spawn_info = True
                self.must_wait = True
                return None  # Just wait the receive from master
            else:
                self.finished = True
                return None

        self.action_status = self.unique_action.update(player)
        return self.unique_action.get_cur_command()

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return

        if self.unique_action is None:
            return
        self.action_status = self.unique_action.post(
            player, callback_result)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        if recv.type == CommunicationType.BORN_SET:
            player.my_drone.jefe_pid = recv.drone_id
            dec_recv = CDRecvInitSpawn(recv)
            player.controller.broadcastHandler.activate(dec_recv)
            self.unique_action = Broadcast(
                CDSendAcknowledge(dec_recv.ack_id, True))
            self.action_status = ActionResultType.CONTINUE
            self.must_wait = False
            return True
        return False

    def wants_to_wait(self) -> bool:
        return self.should_wait and (self.action_status == ActionResultType.CONTINUE or self.sent_spawn_info)

    def have_to_wait(self) -> bool:
        return self.must_wait

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        return (ActionResultType.DONE, None)

####################################################################################################


class NewSpawnMaster(ABehavior):
    """
    It's to the responsability of the behavior to ensure eveyrthing was received from post.
    TODO: fork tells if the next is a different master, or his own slave
    """

    def __init__(self):
        super().__init__()

        self.unique_action = Fork()
        self.unique_behavior = SearchAndFind()
        self.action_status = ActionResultType.NONE

        self.sent_spawn_info = False
        self.await_ack = False

        self.finish_abandonned = False

        self.wait_until_msg = False

        self.id_ack = get_pid()
        self.should_wait = True

        self.already_sent = False

    def update(self, player: Player.Player) -> Optional[Command]:
        if self.finished:
            return None

        if not self.wait_until_msg and self.action_status == ActionResultType.DONE:
            if not self.sent_spawn_info:
                self.sent_spawn_info = True
                self.wait_until_msg = True
            elif not self.await_ack:
                self.await_ack = True
                self.wait_until_msg = True

        if self.wait_until_msg:
            return self.unique_behavior.update(player)

        self.action_status = self.unique_action.update(player)
        return self.unique_action.get_cur_command()

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return

        if self.wait_until_msg:
            self.already_sent = False
            self.unique_behavior.post(player, callback_result)
            return
        self.action_status = self.unique_action.post(
            player, callback_result)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        if recv.type == CommunicationType.BORN_NEW:
            deco_recv = CDRecvISpawn(recv)
            if not deco_recv.unpack(player):
                raise RuntimeError("Failed to unpack ISpawn")
            if not deco_recv.concerned:
                return False
            self.wait_until_msg = False

            dic = player.controller.broadcastHandler.get_activation()
            if dic is None:
                raise RuntimeError(
                    "Activation dict is not activated while Master")

            # make an id unique and somewhat random
            self.id_ack += recv.drone_id
            self.unique_action = Broadcast(CDSendInitSpawn(self.id_ack, dic))
            self.action_status = ActionResultType.CHANGE_TO
            return True
        elif recv.type == CommunicationType.ACKNOWLEDGE:
            self.wait_until_msg = False

            dec_recv = CDRecvAcknowledge(recv, self.id_ack)
            if dec_recv.unpack():
                if not dec_recv.did_acknowledge():
                    self.unique_action = Fork()  # so... we restart ??
                    self.action_status = ActionResultType.CHANGE_TO
                    return True
            self.finished = True
            return True
        return False

    def handle_eject(self, player: Player.Player, direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        if self.wait_until_msg:
            return self.unique_behavior.handle_eject(player, direction)
        super().handle_eject(player, direction)

    def wants_to_wait(self) -> bool:
        if self.wait_until_msg:
            return self.unique_behavior.wants_to_wait()
        return self.should_wait and (self.action_status == ActionResultType.CONTINUE)

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        return (ActionResultType.DONE, None)
