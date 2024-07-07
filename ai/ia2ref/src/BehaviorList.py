##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# BehaviorList.py
##

"""
@file BehaviorList.py
"""
from __future__ import annotations

from . import Player

from .Behaviors.Master import Master
from .Behaviors.Slave import Slave
from .Behavior import ABehavior


def calculate_behavior(player: Player.Player) -> ABehavior:
    """
    @brief Calculate the behavior based on the role
    @param role: Player role
    """
    match player.role:
        case Player.PlayerRole.MASTER:
            return Master(player, player.max_connects)
        case _: # Player.PlayerRole.SLAVE:
            return Slave(player.my_drone.jefe_pid, player.should_preload_broadcast)
