##
# EPITECH PROJECT, 2024
# B-YEP-400-LYN-4-1-zappy-alexandre.douard
# File description:
# OSUtils.py
##

import os
import sys
import ctypes


def check_pid(pid: int) -> bool:
    """ Check For the existence of a pid. """
    if sys.platform == 'win32':
        kernel32 = ctypes.windll.kernel32
        SYNCHRONIZE = 0x100000

        process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
        if process != 0:
            kernel32.CloseHandle(process)
            return True
        else:
            return False
    else:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True


def get_pid() -> int:
    return os.getpid()


def fork() -> bool:
    """ False if the current process is the parent, True the child."""
    p = os.fork()
    if p == -1:
        raise Exception("Fork failed")
    return p == 0
