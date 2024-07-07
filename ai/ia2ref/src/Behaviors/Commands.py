##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## Commands.py
##

"""
@file Commands.py
"""

from .Action import Command, IncantationStatus

def parse_default(payload: str) -> bool:
    return payload == "ok"

def parse_lists(payload: str) -> list[str]:
    try:
        return payload.strip("[]").split(",")
    except:
        raise RuntimeError("Server is sending badly formatted data")

def parse_int(payload: str) -> int:
    try:
        return int(payload)
    except:
        raise RuntimeError("Server is sending badly formatted data")

def parse_incantation(payload: str) -> int:
    """
    I know we give an int, it's to avoid updating all the typings
    """
    match payload:
        case "Elevation underway":
            return IncantationStatus.WAIT.value
        case "ko":
            return IncantationStatus.BAD.value
        case _:
            return IncantationStatus.FINISH.value

def parse_none(payload: str) -> str:
    return payload

##################

class Com_Forward(Command):
    def __init__(self):
        super().__init__("Forward", 7, parse_default)

class Com_Right(Command):
    def __init__(self):
        super().__init__("Right", 7, parse_default)

class Com_Left(Command):
    def __init__(self):
        super().__init__("Left", 7, parse_default)

class Com_Look(Command):
    def __init__(self):
        super().__init__("Look", 7, parse_lists)

class Com_Inventory(Command):
    def __init__(self, should_parse: bool = True):
        super().__init__("Inventory", 1, parse_lists if should_parse else parse_none) # type: ignore

class Com_Connect_nbr(Command):
    def __init__(self):
        super().__init__("Connect_nbr", 0, parse_int)

class Com_Broadcast(Command):
    def __init__(self, payload: str):
        super().__init__(f"Broadcast {payload}", 7, parse_default)

class Com_Fork(Command):
    def __init__(self):
        super().__init__("Fork", 42, parse_default)

class Com_Eject(Command):
    def __init__(self):
        super().__init__("Eject", 7, parse_default)

class Com_Take(Command):
    def __init__(self, object: str):
        super().__init__(f"Take {object}", 7, parse_default)

class Com_Set(Command):
    def __init__(self, object: str):
        super().__init__(f"Set {object}", 7, parse_default)

class Com_Incant(Command):
    def __init__(self):
        super().__init__("Incantation", 300, parse_incantation)
