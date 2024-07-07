##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# OrderedEnum.py
##

"""
@file OrderedEnum.py
"""

from enum import Enum


class OrderedEnum(Enum):

    def __init__(self, value, *args, **kwds):
        super().__init__(*args, **kwds)
        self.__order = len(self.__class__)

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.__order >= other.__order
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.__order > other.__order
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.__order <= other.__order
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.__order < other.__order
        return NotImplemented
