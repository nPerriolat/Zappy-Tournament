##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## CommunicationType.py
##

"""
@file CommunicationType.py
"""

from enum import Enum

class CommunicationType(Enum):
    NONE = -1

    ACKNOWLEDGE = 0 # Acknowledge the message

    BORN_NEW = 1 # Call whenever a new client is connected, index master should respond. The other clients acknowledge
    BORN_SET = 2 # The index master got the message, the client got every indexes necessary to receive, it tells to resume everything

    MOVE_TO_ME = 3 # Move to tile where the broadcast is comming from
    OK_TO_MOVE = 4 # The client is ready to move to the tile
    CL_CANCEL_TO_MOVE = 5 # The client is not ready to move to the tile
    MA_CANCEL_TO_MOVE = 6 # The master needs food, BRB !!
    DONE_MOVE = 7 # The client is done moving to the tile, redy to incante
    MOVE_TO_COORDS = 8 # Move to the base coordinates diff given

    ASK_INVENTORY = 9 # Master to demand to give inventory
    SHARE_INVENTORY = 10 # Share inventory with the master
    DROP_RESOURCES = 11 # Master to demand to give these resources
    DONE_DROP = 12 # Master to demand to give these resources
    INCANT_STATUS = 13 # Master to demand to incante now
    GATHER_RESOURCES = 14 # Master to demand to find resources, not enough available

    READY = 15 # The client is ready to begin the incant process
    UPDATE_BASE_COORDS = 16 # Move the base from what you think it is.
