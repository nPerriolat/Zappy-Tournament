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
from collections import deque
from copy import copy

from ... import Player
from ...Behavior import ABehavior
from ..Action import Command, IAction, ActionResultType
from ..Actions.Broadcast import Broadcast
from ..Actions.Inventory import Inventory
from ..Actions.Move import Move
from ..Actions.Set import Set
from ..Actions.Take import Take
from ...Map import ResourceType, INCANTATION_RESOURCES

from ...Constants import INCANTATION_ABANDON_THRESHOLD_FOOD, INCANTATION_MIN_FOOD, BALANCE_FOOD_MASTER_BIAS, FOOD_MULTIPLIER
from ..Actions.Incantation import Incantation as IncantationAction
from .SearchAndFind import SearchAndFind

from ...Communications.Communication import CommunicationRecv
from ...Communications.CommunicationType import CommunicationType

from ...Communications.Broadcasts.Incantation import CDRecvInventory, CDSendInventory, CDRecvDrop, CDSendDrop, CDRecvIncantStatus, CDSendIncantStatus, CDRecvDoneDrop, CDSendDoneDrop, CDRecvAskInventory, CDSendAskInventory, CDRecvGatherResources, CDSendGatherResources
from ...Communications.Broadcasts.SlaveMoveToMe import CDRecvSlaveCancelMove, CDSendSlaveCancelMove, CDRecvDoneMove, CDSendDoneMove
from ...Communications.Broadcasts.MasterMoveToMe import CDSendMoveBase, CDRecvMoveBase


def get_actions_drop(player: Player.Player, diff_inv: dict[ResourceType, int]):
    if not diff_inv:
        return []
    return [Set(res) if nb > 0 else Take(res, True) for res, nb in diff_inv.items() for _ in range(abs(nb)) if nb != 0]


######################################################################################################


class IncantationSharedSlave(ABehavior):
    def __init__(self, player: Player.Player, max_level_to_incant: int = 8):
        """ The player will not be able to incant if he is not the master, he's waiting the orders """
        super().__init__()

        self.actions: deque[IAction] = deque([Inventory()])
        self.action_status = ActionResultType.CONTINUE

        self.should_wait = True
        self.has_received_post = True
        self.max_level_to_incant = max_level_to_incant
        self.wait_incant = False

        self.not_yet_in_base = False
        self.ready_to_begin = True

        # technically sets the values
        self.__reset()

        self.finish_specific = False
        self.wanted_resource = ResourceType.FOOD
        self.wanted_amount = 0

        self.actions_stack: deque[IAction] = deque()

        self.finish_abandonned = False

    def update(self, player: Player.Player) -> Optional[Command]:
        if self.finished:
            return None

        if not self.finish_abandonned and player.get_life() < INCANTATION_ABANDON_THRESHOLD_FOOD:
            self.finish_abandonned = True
            self.actions.append(
                Broadcast(CDSendSlaveCancelMove(player.my_drone.jefe_pid, False)))
            return self.__send_command(player)

        if not self.has_received_post:
            return None

        if self.wait_incant:
            return None

        if self.action_status == ActionResultType.CONTINUE:
            return self.__send_command(player)

        if self.actions:
            prev = self.actions.popleft()
            if self.action_status == ActionResultType.DONE:
                if self.not_yet_in_base:  # has moved to the base
                    self.not_yet_in_base = False
                    # tells to then he's ready
                    return self.__send_command(player)
                elif not self.ready_to_begin:
                    self.ready_to_begin = True

                if self.finish_abandonned or player.my_drone.level >= self.max_level_to_incant:
                    self.ready_to_begin = False
                    self.finished = True
                    return None
                elif self.ask_drop:
                    if self.nb_drops == 0:
                        self.ask_drop = False
                        self.actions.append(
                            Broadcast(CDSendDoneDrop(player.my_drone.jefe_pid)))
                        return self.__send_command(player)
                    else:
                        self.nb_drops -= 1
                        return self.__send_command(player)
            elif self.action_status == ActionResultType.CHANGE_TO:
                if isinstance(prev, Take) or isinstance(prev, Set):
                    if self.nb_drops == 0:
                        self.ask_drop = False
                        self.actions.append(
                            Broadcast(CDSendDoneDrop(player.my_drone.jefe_pid)))
                        return self.__send_command(player)
                    else:
                        self.nb_drops -= 1
                        return self.__send_command(player)
                print("dedede")
                return None

        # keep the inventory updated, in case when there is nothing to do
        if len(self.actions) == 0:
            self.actions.append(Inventory(True))
        return self.__send_command(player)

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return
        self.has_received_post = True
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
        return self.should_wait and (self.action_status == ActionResultType.CONTINUE)

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        if self.finish_abandonned:
            return (ActionResultType.SUSPEND_FOR, SearchAndFind(ResourceType.FOOD, INCANTATION_MIN_FOOD, -1, should_pick_random=False))
        if self.finish_specific:
            return (ActionResultType.SUSPEND_FOR, SearchAndFind(self.wanted_resource, self.wanted_amount, -1))
        return (ActionResultType.DONE, None)

    def finish_suspended(self, player: Player.Player):
        # normally, the base coordinates may have changed
        self.wait_incant = False
        self.asked_incante = False
        self.wants_to_finish = False

        self.finish_abandonned = False
        self.finish_specific = False
        self.action_status = ActionResultType.CONTINUE
        if player.map.player_pos != player.my_drone.base_coords:
            self.not_yet_in_base = True
            self.actions.append(Move(player.map.player_pos, player.my_drone.base_coords, player.map.player_dir,
                                     player.map.max_x, player.map.max_y))
        self.actions.append(
            Broadcast(CDSendDoneMove(player.my_drone.jefe_pid)))
        self.actions.extend(self.actions_stack)
        self.actions_stack.clear()
        return super().finish_suspended(player)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        match recv.type:
            case CommunicationType.ASK_INVENTORY:
                deco_recv = CDRecvAskInventory(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack ASK_INVENTORY")
                if not deco_recv.concerned:
                    return False

                send_inventory = Broadcast(CDSendInventory(
                    player.my_drone.jefe_pid, player.get_inventory()))
                if not self.ready_to_begin:  # can't do anything here
                    self.actions_stack.append(send_inventory)
                else:
                    self.actions.append(send_inventory)
                    self.action_status = ActionResultType.CONTINUE
                return True
            case CommunicationType.DROP_RESOURCES:
                deco_recv = CDRecvDrop(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack DROP_RESOURCE")
                if not deco_recv.concerned:  # don't care
                    return False

                diff_inv = deco_recv.diff_inventory
                actions = get_actions_drop(player, diff_inv)
                if not actions:
                    return True
                self.nb_drops = len(actions)
                self.ask_drop = True
                if not self.ready_to_begin:  # can't do anything here
                    self.actions_stack.extend(actions)
                else:
                    self.actions.extend(actions)
                    self.action_status = ActionResultType.CONTINUE
                return True
            case CommunicationType.INCANT_STATUS:  # when we know the base / when we need to move because we got attacked
                deco_recv = CDRecvIncantStatus(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack INCANT_STATUS")
                if not deco_recv.concerned:  # don't care
                    return False

                if not self.ready_to_begin:
                    return True
                if deco_recv.is_done:
                    # player.my_drone.level += 1
                    self.finished = True
                else:
                    self.wait_incant = True
                return True
            case CommunicationType.GATHER_RESOURCES:
                deco_recv = CDRecvGatherResources(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack INCANT_STATUS")
                if not deco_recv.concerned:  # don't care
                    return False

                if not self.ready_to_begin:
                    return True
                self.finish_specific = True
                self.finished = True
                self.wanted_resource = deco_recv.resource
                self.wanted_amount = player.get_inventory()[deco_recv.resource] + deco_recv.amount
        return False

    ## PRIVATE ##

    def __send_command(self, player: Player.Player) -> Optional[Command]:
        self.action_status = self.actions[0].update(player)
        if self.action_status == ActionResultType.GIVE_UP:
            raise RuntimeError("I can't do it anymore...")
        self.has_received_post = False
        return self.actions[0].get_cur_command()

    def __reset(self):
        self.ask_drop = False
        self.nb_drops = 0
        self.wait_incant = False


######################################################################################################

class IncantationSharedMaster(ABehavior):
    def __init__(self, player: Player.Player, nb_gather_players: int = 5):
        super().__init__()

        self.wanted_inventories: dict[int, dict[ResourceType, int]] = {
            player.my_drone.pid: player.get_inventory()}
        self.nb_players_incant = nb_gather_players + 1  # + 1 => himself

        self.eveyrone_is_here = True
        self.eveyrone_has_dropped = False
        self.has_asked_inventories = True
        self.eveyrone_has_answered_inventory = False
        self.concerned_dic: dict[int, dict[str, Player.Drone | bool]] = {}
        for id, d in player.other_drones.items():
            self.concerned_dic[id] = {"drone": d,
                                      "ready": True, "dropped": True}

        self.concerned_list = list(self.concerned_dic.keys())
        self.actions: deque[IAction] = deque(
            [Broadcast(CDSendAskInventory(self.concerned_list))])
        self.action_status = ActionResultType.CONTINUE

        self.not_enough_resources = False
        self.has_balanced_food = False
        self.take_diff: Optional[dict] = None
        self.idx = 0

        self.__reset()

        self.finish_abandonned = False

        self.should_wait = True
        self.has_received_post = True

    def update(self, player: Player.Player) -> Optional[Command]:
        if self.finished:
            return None

        if player.get_life() < INCANTATION_ABANDON_THRESHOLD_FOOD:
            print("master abandon")
            self.finish_abandonned = True
            self.finished = True
            return None

        if not self.has_received_post:
            return None

        if self.actions:
            if self.action_status == ActionResultType.CONTINUE:
                if self.wait_incantation:
                    return None
                return self.__send_command(player)
            prev = self.actions.popleft()
            if self.action_status == ActionResultType.DONE:
                if self.nb_has_to_drop > 0:
                    self.nb_has_to_drop -= 1
                    # action is already in list
                    # there might be a broadcast sharing drop demand, sometims no...
                    if len(self.actions) != 0:
                        return self.__send_command(player)
                if self.asked_incante and not self.wait_incantation:
                    self.wait_incantation = True
                    return self.__send_command(player)
                elif self.eveyrone_is_here and self.wait_incantation:
                    if not self.retry:
                        self.wants_to_finish = True
                    else:
                        self.actions.appendleft(
                            Broadcast(CDSendIncantStatus(self.concerned_list, True)))
                        self.__reset()
                    return self.__send_command(player)
                elif self.wants_to_finish:
                    self.finished = True
                    return None
            elif self.action_status == ActionResultType.CHANGE_TO:
                if isinstance(prev, Take) or isinstance(prev, Set):
                    if self.nb_has_to_drop > 0:
                        self.nb_has_to_drop -= 1
                        # action is already in list
                        # there might be a broadcast sharing drop demand, sometims no...
                        if len(self.actions) != 0:
                            return self.__send_command(player)
                # Someone took our resources !!!
                print("MASTER RESET")
                self.__reset()
                self.actions.appendleft(
                    Broadcast(CDSendIncantStatus(self.concerned_list, True)))
                return self.__send_command(player)

        if self.eveyrone_is_here and not self.has_asked_inventories:
            self.has_asked_inventories = True
            self.actions.append(
                Broadcast(CDSendAskInventory(self.concerned_list)))
            return self.__send_command(player)

        if self.eveyrone_is_here and self.eveyrone_has_answered_inventory and not self.ask_drop and not (self.eveyrone_has_dropped and self.nb_has_to_drop == 0):
            reslut, diffs = self.__calculate_inv_drops(player)

            self.retry = reslut is None
            if reslut is not None:
                res, nb = reslut
                self.eveyrone_has_answered_inventory = False
                self.has_asked_inventories = False
                self.ask_drop = False
                self.eveyrone_has_dropped = False
                self.eveyrone_is_here = False

                l = [key for key in self.wanted_inventories.keys(
                ) if key != player.my_drone.pid and self.concerned_dic[key]["ready"]]
                if not l:
                    print("We're dead")
                    return None
                best_food_drone = max(
                    l, key=lambda id: self.wanted_inventories[id][ResourceType.FOOD])
                self.concerned_dic[best_food_drone]["ready"] = False
                print(
                    f"sending not enough {res.name}, {nb}:", player.my_drone.pid)
                self.actions.append(
                    Broadcast(CDSendGatherResources(best_food_drone, res, nb)))
                return self.__send_command(player)

            if not self.has_balanced_food:  # order is important
                self.take_diff = self.__balance_food(
                    player, diffs)  # side effects on diffs
                self.has_balanced_food = True
            has_broadcast_action = self.__send_broadcast(player, diffs)

            if not has_broadcast_action:
                self.eveyrone_has_dropped = True
            else:
                # set the waiting for eveyrone to drop for certain id :
                self.ask_drop = True
            return self.__send_command(player)
        elif self.eveyrone_has_dropped and self.eveyrone_is_here:
            if self.take_diff is not None:
                has_broadcast_action = self.__send_broadcast(
                    player, self.take_diff)

                self.take_diff = None
                if has_broadcast_action:
                    self.ask_drop = True
                    self.eveyrone_has_dropped = False
                    return self.__send_command(player)

            self.eveyrone_has_dropped = False
            self.actions.append(
                Broadcast(CDSendIncantStatus(self.concerned_list, False)))
            self.actions.append(IncantationAction())
            self.asked_incante = True
            return self.__send_command(player)

        # keep the inventory updated, in case
        if len(self.actions) == 0:
            self.actions.appendleft(Inventory(True))
        return self.__send_command(player)

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return
        self.has_received_post = True
        self.action_status = self.actions[0].post(player, callback_result)

    def handle_eject(self, player, direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        super().handle_eject(player, direction)
        # reset everything
        self.__reset(True)

    def wants_to_wait(self) -> bool:
        return self.should_wait and (self.action_status == ActionResultType.CONTINUE)

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        if self.finish_abandonned:
            return (ActionResultType.SUSPEND_FOR, SearchAndFind(ResourceType.FOOD, INCANTATION_MIN_FOOD, -1, should_pick_random=False))
        return (ActionResultType.DONE, None)

    def finish_suspended(self, player: Player.Player):
        self.wait_incantation = False
        self.asked_incante = False
        self.wants_to_finish = False

        self.finish_abandonned = False
        if player.map.player_pos != player.my_drone.base_coords:
            self.action_status = ActionResultType.CONTINUE
            self.actions.append(Move(player.map.player_pos, player.my_drone.base_coords, player.map.player_dir,
                                     player.map.max_x, player.map.max_y))
        return super().finish_suspended(player)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        match recv.type:
            case CommunicationType.SHARE_INVENTORY:
                deco_recv = CDRecvInventory(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack MOVE_TO_ME")
                if not deco_recv.concerned:
                    return False
                self.wanted_inventories[deco_recv.content.drone_id] = deco_recv.inventory
                if len(self.wanted_inventories) == self.nb_players_incant:
                    self.eveyrone_has_answered_inventory = True
                return True
            case CommunicationType.CL_CANCEL_TO_MOVE:
                deco_recv = CDRecvSlaveCancelMove(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack MA_CANCEL_TO_MOVE")
                if not deco_recv.concerned:  # don't care
                    return False
                self.eveyrone_is_here = False
                self.concerned_dic[deco_recv.content.drone_id]["ready"] = False
                return True
            case CommunicationType.DONE_MOVE:
                deco_recv = CDRecvDoneMove(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack DONE_MOVE")
                if not deco_recv.concerned:
                    return False
                self.concerned_dic[deco_recv.content.drone_id]["ready"] = True
                if all([d["ready"] for d in self.concerned_dic.values()]):
                    self.eveyrone_is_here = True
                    # print("askdrop", self.ask_drop, "everyone answered inv",
                    #       self.eveyrone_has_answered_inventory, "every has drop", self.eveyrone_has_dropped)
            case CommunicationType.DONE_DROP:  # when we know the base / when we need to move because we got attacked
                deco_recv = CDRecvDoneDrop(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack DONE_DROP")
                if not deco_recv.concerned:  # don't care
                    return False
                self.concerned_dic[deco_recv.content.drone_id]["dropped"] = True
                if all([d["dropped"] for d in self.concerned_dic.values()]):
                    self.eveyrone_has_dropped = True
                return True
        return False

    ## PRIVATE ##

    def __calculate_inv_drops(self, player: Player.Player) -> tuple[Optional[tuple[ResourceType, int]], dict[int, dict[ResourceType, int]]]:
        ro_lvl_inv = INCANTATION_RESOURCES[player.my_drone.level + 1]
        cur_level_inv = copy(ro_lvl_inv)
        diff_dic: dict[int, dict[ResourceType, int]] = {}
        items: deque[tuple[ResourceType, int]] = deque([(res, nb) for res, nb in cur_level_inv.items()
                                                        if res != ResourceType.PLAYER and nb != 0])
        if not items:
            return (ResourceType.FOOD, 1), diff_dic
        solo_items = [item[0] for item in items]
        pids = [d_id for d_id in self.wanted_inventories.keys()]
        len_pids = len(pids)
        wanted_inv = {}
        for d_id, d_inv in self.wanted_inventories.items():
            wanted_inv[d_id] = {res: nb for res,
                                nb in d_inv.items() if res in solo_items}
        res, nb = items.popleft()
        max_resource = len(items)
        while True:
            was_in = False
            for i in range(len(wanted_inv)):
                # shuffle more the droppers
                self.idx = (self.idx + i) % len_pids
                d_id = pids[self.idx]
                d_inv = wanted_inv[d_id]
                if d_inv[res] > 0:
                    was_in = True
                    if d_id not in diff_dic:
                        diff_dic[d_id] = {res: 0 for res in solo_items}
                    diff_dic[d_id][res] += 1
                    nb -= 1
                    if nb == 0:
                        if max_resource == 0:
                            return None, diff_dic
                        res, nb = items.popleft()
                        max_resource -= 1
                        break
            if not was_in:
                print("ok not done")
                return (res, nb), {}

    def __balance_food(self, player: Player.Player, diffs: dict[int, dict[ResourceType, int]]):
        l = [nb for dic in self.wanted_inventories.values()
             for res, nb in dic.items() if res == ResourceType.FOOD]
        mean = sum(l) / len(l) if len(l) > 0 else 0

        take_diff = {}
        for d_id, d_inv in self.wanted_inventories.items():
            bias = 0  # BALANCE_FOOD_MASTER_BIAS if d_id == player.my_drone.pid else 0
            res = int(d_inv[ResourceType.FOOD] -
                      mean + bias) // FOOD_MULTIPLIER
            if res > 0:
                if diffs.get(d_id) is None:
                    diffs[d_id] = {}
                diffs[d_id][ResourceType.FOOD] = res  # in case
            elif res < 0:
                if take_diff.get(d_id) is None:
                    take_diff[d_id] = {}
                # I have no idea why it doesn't work
                take_diff[d_id][ResourceType.FOOD] = res

        return take_diff

    def __send_broadcast(self, player: Player.Player, diffs: dict[int, dict[ResourceType, int]]):
        has_broadcast_action = False
        for d_id, diff in diffs.items():
            if d_id == player.my_drone.pid:  # the wanted inventory is shallow copy of cur inventory, don't modify it
                actions = get_actions_drop(player, diff)
                self.nb_has_to_drop = len(actions)
                if actions:
                    self.actions.extend(actions)
                continue
            for res, nb in diff.items():
                self.wanted_inventories[d_id][res] -= nb
            self.actions.append(Broadcast(CDSendDrop(d_id, diff)))
            has_broadcast_action = True

        if has_broadcast_action:
            for d_id, diff in diffs.items():
                if d_id == player.my_drone.pid:
                    continue
                self.concerned_dic[d_id]["dropped"] = False
        return has_broadcast_action

    def __send_command(self, player: Player.Player) -> Optional[Command]:
        self.action_status = self.actions[0].update(player)
        if self.action_status == ActionResultType.GIVE_UP:
            raise RuntimeError("I can't do it anymore...")
        self.has_received_post = False
        return self.actions[0].get_cur_command()

    def __reset(self, full: bool = False):
        self.wait_incantation = False
        self.asked_incante = False
        self.wants_to_finish = False
        self.retry = False
        self.nb_has_to_drop = 0
        self.ask_drop = False
        if full:
            self.eveyrone_has_answered_inventory = False
            self.eveyrone_has_dropped = False
            self.eveyrone_is_here = False
            for pid in self.concerned_dic.keys():
                self.concerned_dic[pid]["ready"] = False
                self.concerned_dic[pid]["moving"] = True
