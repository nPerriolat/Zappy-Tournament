##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# MoveToBroadcaster.py
##

"""
@file MoveToBroadcaster.py
"""
from __future__ import annotations

from typing import Optional
from collections import deque

from ... import Player
from ...Behavior import ABehavior
from ..Action import Command, IAction, ActionResultType
from ..Actions.Move import Move
from ..Actions.Broadcast import Broadcast
from ..Actions.Inventory import Inventory
from ...Map import ResourceType, Position
from ...Locomotion import LocomotionDirection, Direction
from ...Constants import FOOD_MULTIPLIER, MOVE_TO_ME_CLOCK_FOLLOW, INCANTATION_MIN_FOOD

from ...Communications.Broadcasts.MasterMoveToMe import CDSendMoveToMe, CDRecvMoveToMe, CDRecvMoveToCoords, CDRecvMasterCancelMove, CDSendMasterCancelMove, CDSendMoveToCoords
from ...Communications.Broadcasts.SlaveMoveToMe import CDRecvOKToMove, CDSendOKToMove, CDRecvDoneMove, CDSendDoneMove, CDRecvSlaveCancelMove, CDSendSlaveCancelMove
from ...Communications.Communication import CommunicationRecv
from ...Communications.CommunicationType import CommunicationType

from .SearchAndFind import SearchAndFind


class MoveToBroadcaster(ABehavior):
    def __init__(self, player: Player.Player, moving_demand: Optional[CDRecvMoveToMe], min_food: int = FOOD_MULTIPLIER):
        super().__init__()

        self.min_food_threshold = min_food
        # if concerned and receive MOVE_TO_COORDS, then it's the saved base coordinates
        self.knows_base = False

        self.actions: deque[IAction] = deque()
        self.action_status = ActionResultType.NONE

        self.wants_to_said_to_move = False
        self.has_said_to_move = False
        self.should_move = False
        self.is_in_destination = False

        self.is_moving = False

        # the slave behavior will reintantiate the behavior anyways
        self.finished_waiting = False
        self.finish_abandonned = False

        self.should_wait = True
        self.must_wait = True

        self.has_received_post = True

        if moving_demand is not None:
            self.__handle_move_to_me(player, moving_demand)

    def update(self, player: Player.Player) -> Optional[Command]:
        if not self.has_received_post:  # broadcst updates, but may distrub some actions that doesn't expect to be updated without post
            return None  # watchout, because errors in them like empty commands breaks the cycle and infinite loop occurs

        if player.get_life() <= self.min_food_threshold:
            self.actions.clear()
            self.actions.appendleft(
                Broadcast(CDSendSlaveCancelMove(player.my_drone.jefe_pid, False)))
            self.action_status = ActionResultType.CONTINUE
            self.finish_abandonned = True
            return self.__send_command(player)

        if self.actions:
            if self.action_status == ActionResultType.CONTINUE or self.action_status == ActionResultType.NONE:
                return self.__send_command(player)
            self.actions.popleft()

        if self.action_status == ActionResultType.DONE:
            if len(self.actions) > 0:
                self.action_status = ActionResultType.CONTINUE
            if self.is_in_destination:
                # normally, the first time you encounter a base
                player.my_drone.knows_base = True
                player.set_first_base(player.map.player_pos) # no diff == player.map.player_pos
                self.finished = True
            elif self.wants_to_said_to_move and not self.has_said_to_move:
                self.has_said_to_move = True
            elif self.has_said_to_move and self.is_moving:
                self.is_moving = False
            elif self.has_said_to_move and self.knows_base:
                self.finished = True

        return None

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return
        self.has_received_post = True
        self.action_status = self.actions[0].post(player, callback_result)

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        if self.finish_abandonned:
            return (ActionResultType.SUSPEND_FOR, SearchAndFind(ResourceType.FOOD, INCANTATION_MIN_FOOD, -1, should_pick_random=False))
        if self.finished_waiting:
            return (ActionResultType.DONE, None)
        return (ActionResultType.DONE, None)

    def finish_suspended(self, player: Player.Player):
        self.finish_abandonned = False
        return super().finish_suspended(player)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        match recv.type:
            case CommunicationType.MOVE_TO_ME:
                deco_recv = CDRecvMoveToMe(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack MOVE_TO_ME")
                if deco_recv.concerned:
                    if self.is_moving:  # don't overwrite cur action
                        return True
                    self.__handle_move_to_me(player, deco_recv)
                    return True
                return False
            case CommunicationType.MA_CANCEL_TO_MOVE:
                deco_recv = CDRecvMasterCancelMove(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack MA_CANCEL_TO_MOVE")
                if not deco_recv.concerned:  # don't care
                    return False
                # unpack and chekc if conercened
                self.finish_incant = True
                self.finished = True
                return True
            case CommunicationType.MOVE_TO_COORDS:  # when we know the base / when we need to move because we got attacked
                # SLAVE BEHAVIOR ALREADY UPDATED THE COORDS, THIS IS DONE TO NEVER FORGET WHERE THE BASE IS
                deco_recv = CDRecvMoveToCoords(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack MOVE_TO_COORDS")
                if not deco_recv.concerned:  # don't care
                    return False
                self.wants_to_said_to_move = True
                self.actions.append(
                    Broadcast(CDSendOKToMove(player.my_drone.jefe_pid)))
                self.actions.append(Move(player.map.player_pos, deco_recv.coords, player.map.player_dir,
                                         player.map.max_x, player.map.max_y))
                self.action_status = ActionResultType.CONTINUE
                return True
        return False

    def handle_eject(self, player: Player.Player, direction: Direction):
        super().handle_eject(player, direction)
        if self.finish_abandonned:  # don't care
            return

        self.actions.append(
            Broadcast(CDSendSlaveCancelMove(player.my_drone.jefe_pid, True)))
        self.action_status = ActionResultType.CONTINUE
        self.is_in_destination = False

    def wants_to_wait(self) -> bool:
        return self.should_wait and self.action_status == ActionResultType.CONTINUE

    ## Private ##

    def __send_command(self, player: Player.Player) -> Optional[Command]:
        self.action_status = self.actions[0].update(player)
        if self.action_status == ActionResultType.GIVE_UP:
            raise RuntimeError("I can't do it anymore...")
        self.has_received_post = False
        return self.actions[0].get_cur_command()

    def __handle_move_to_me(self, player: Player.Player, deco_recv: CDRecvMoveToMe):
        coords = self.__direction_to_coords(player, deco_recv.content.dir)
        if coords is None:
            self.is_in_destination = True
            self.actions.append(
                Broadcast(CDSendDoneMove(player.my_drone.jefe_pid)))
            self.action_status = ActionResultType.CONTINUE
            return True
        elif not self.wants_to_said_to_move:
            self.is_moving = True
            self.wants_to_said_to_move = True
            self.action_status = ActionResultType.CONTINUE
            self.actions.append(
                Broadcast(CDSendOKToMove(player.my_drone.jefe_pid)))
            if self.knows_base:
                self.actions.append(Move(player.map.player_pos, player.my_drone.base_coords, player.map.player_dir,
                                         player.map.max_x, player.map.max_y))
            else:
                self.actions.append(Move(player.map.player_pos, coords, player.map.player_dir,
                                         player.map.max_x, player.map.max_y))
        elif self.has_said_to_move:
            self.is_moving = True
            self.action_status = ActionResultType.CONTINUE
            move = Move(player.map.player_pos, coords, player.map.player_dir,
                        player.map.max_x, player.map.max_y)
            self.actions.append(move)

    def __direction_to_coords(self, player: Player.Player, direction: Direction) -> Optional[Position]:
        pos = player.map.player_pos
        if direction == Direction.SAME_TILE:
            return None  # done

        match player.map.player_dir:
            case LocomotionDirection.UP:
                match direction:
                    case Direction.NORTH:
                        return Position(pos.x, pos.y + 1)
                    case Direction.NORTH_WEST:
                        return Position(pos.x + 1, pos.y + 1)
                    case Direction.WEST:
                        return Position(pos.x + 1, pos.y)
                    case Direction.SOUTH_WEST:
                        return Position(pos.x + 1, pos.y - 1)
                    case Direction.SOUTH:
                        return Position(pos.x, pos.y - 1)
                    case Direction.SOUTH_EAST:
                        return Position(pos.x - 1, pos.y - 1)
                    case Direction.EAST:
                        return Position(pos.x - 1, pos.y)
                    case Direction.NORTH_EAST:
                        return Position(pos.x - 1, pos.y + 1)
            case LocomotionDirection.DOWN:
                match direction:
                    case Direction.NORTH:
                        return Position(pos.x, pos.y - 1)
                    case Direction.NORTH_WEST:
                        return Position(pos.x - 1, pos.y - 1)
                    case Direction.WEST:
                        return Position(pos.x - 1, pos.y)
                    case Direction.SOUTH_WEST:
                        return Position(pos.x - 1, pos.y + 1)
                    case Direction.SOUTH:
                        return Position(pos.x, pos.y + 1)
                    case Direction.SOUTH_EAST:
                        return Position(pos.x + 1, pos.y + 1)
                    case Direction.EAST:
                        return Position(pos.x + 1, pos.y)
                    case Direction.NORTH_EAST:
                        return Position(pos.x + 1, pos.y - 1)
            case LocomotionDirection.RIGHT:
                match direction:
                    case Direction.NORTH:
                        return Position(pos.x + 1, pos.y)
                    case Direction.NORTH_WEST:
                        return Position(pos.x + 1, pos.y - 1)
                    case Direction.WEST:
                        return Position(pos.x, pos.y - 1)
                    case Direction.SOUTH_WEST:
                        return Position(pos.x - 1, pos.y - 1)
                    case Direction.SOUTH:
                        return Position(pos.x - 1, pos.y)
                    case Direction.SOUTH_EAST:
                        return Position(pos.x - 1, pos.y + 1)
                    case Direction.EAST:
                        return Position(pos.x, pos.y + 1)
                    case Direction.NORTH_EAST:
                        return Position(pos.x + 1, pos.y + 1)
            case LocomotionDirection.LEFT:
                match direction:
                    case Direction.NORTH:
                        return Position(pos.x - 1, pos.y)
                    case Direction.NORTH_WEST:
                        return Position(pos.x - 1, pos.y + 1)
                    case Direction.WEST:
                        return Position(pos.x, pos.y + 1)
                    case Direction.SOUTH_WEST:
                        return Position(pos.x + 1, pos.y + 1)
                    case Direction.SOUTH:
                        return Position(pos.x + 1, pos.y)
                    case Direction.SOUTH_EAST:
                        return Position(pos.x + 1, pos.y - 1)
                    case Direction.EAST:
                        return Position(pos.x, pos.y - 1)
                    case Direction.NORTH_EAST:
                        return Position(pos.x - 1, pos.y - 1)


####################################################################################################


class MoveToMe(ABehavior):
    def __init__(self, player: Player.Player, base_coords: Optional[Position] = None, min_food: int = 250):
        super().__init__()

        self.min_food_threshold = min_food
        self.base_coords = base_coords

        self.concerned = self.__get_concerned(player)
        if self.base_coords is not None:
            self.unique_action = Broadcast(
                CDSendMoveToCoords(self.concerned, self.base_coords))
        else:
            self.unique_action = Broadcast(CDSendMoveToMe(self.concerned))
        self.action_status = ActionResultType.CONTINUE

        self.finish_abandonned = False
        self.should_wait = True

        self.cur_clock_loop = 0
        self.concerned_dic = {}
        items = [(pid, d) for pid, d in player.other_drones.items()
                 if d.jefe_pid == player.my_drone.pid]
        for pid, d in items:
            self.concerned_dic[pid] = {
                "drone": d, "ready": False, "moving": False}

    def update(self, player: Player.Player) -> Optional[Command]:
        if not self.finish_abandonned and player.get_life() <= self.min_food_threshold:
            self.unique_action = Broadcast(
                CDSendMasterCancelMove(self.concerned))
            self.action_status = ActionResultType.CONTINUE
            self.finish_abandonned = True
            self.action_status = self.unique_action.update(player)
            return self.unique_action.get_cur_command()

        if self.action_status == ActionResultType.DONE:
            if self.finish_abandonned:
                self.finished = True

        if self.finished:
            return None

        if self.action_status != ActionResultType.CONTINUE:
            if self.base_coords is None and self.cur_clock_loop >= MOVE_TO_ME_CLOCK_FOLLOW:
                self.cur_clock_loop = 0
                self.unique_action = Broadcast(CDSendMoveToMe(self.concerned))
            else:
                self.cur_clock_loop += 1
                self.unique_action = Inventory(True)

        self.action_status = self.unique_action.update(player)
        return self.unique_action.get_cur_command()

    def post(self, player: Player.Player, callback_result: Optional[bool | list[str] | int]):
        if callback_result is None:
            return
        self.action_status = self.unique_action.post(
            player, callback_result)

    def wants_to_wait(self) -> bool:
        return self.should_wait and self.action_status == ActionResultType.CONTINUE

    def finish(self, player: Player.Player) -> tuple[ActionResultType, ABehavior | None]:
        if self.finish_abandonned:
            return (ActionResultType.SUSPEND_FOR, SearchAndFind(ResourceType.FOOD, self.min_food_threshold + 126 * 4, -1, should_pick_random=False))
        return (ActionResultType.DONE, None)

    def handle_eject(self, player, direction):
        """
        Eject may corrupt what the player is doing, so the behavior should acknowledge this
        """
        super().handle_eject(player, direction)

    def handle_broadcast(self, player: Player.Player, recv: CommunicationRecv) -> bool:
        match recv.type:
            case CommunicationType.OK_TO_MOVE:
                # unpack and chekc if conercened
                deco_recv = CDRecvOKToMove(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack OK_TO_MOVE")
                if not deco_recv.concerned:
                    return False
                self.concerned_dic[recv.drone_id]["moving"] = True
                return True
            case CommunicationType.CL_CANCEL_TO_MOVE:
                deco_recv = CDRecvSlaveCancelMove(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack CL_CANCEL_TO_MOVE")
                if not deco_recv.concerned:
                    return False
                self.concerned_dic[recv.drone_id]["ready"] = False
                self.concerned_dic[recv.drone_id]["moving"] = False
                self.finished = False
                return True
            case CommunicationType.DONE_MOVE:
                deco_recv = CDRecvDoneMove(recv)
                if not deco_recv.unpack(player):
                    raise RuntimeError("Failed to unpack DONE_MOVE")
                if not deco_recv.concerned:
                    return False
                self.concerned_dic[recv.drone_id]["ready"] = True
                if all([d["ready"] for d in self.concerned_dic.values()]):
                    self.finished = True
                    if not player.my_drone.knows_base:
                        player.my_drone.knows_base = True
                        player.set_first_base(player.map.player_pos)
                    else:
                        player.map.update_db_base(
                            player.map.player_pos, player.my_drone.base_coords)
                return True
        return False

    ## Private ##

    def __get_concerned(self, player: Player.Player) -> list[int]:
        return [id for id, d in player.other_drones.items() if d.jefe_pid == player.my_drone.pid]
