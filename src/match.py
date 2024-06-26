#!/usr/bin/env python3

import subprocess
import threading
import re
import signal
import os
import psutil
import time
import sys
import socket

from src.settings import Settings
from src.result import Result

class RunFailed(Exception):
    pass

def launch_server(teamA : str, teamB : str, settings : Settings):
    command = ["./server/zappy_server", "-p", str(settings.port), "-x", str(settings.x), "-y", str(settings.y), "-n", teamA, teamB, "-c", str(settings.starting_eggs), "-f", str(settings.frequence)]
    return subprocess.Popen(command, bufsize=-1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)

def launch_ai(team : str, settings : Settings):
    command = [f"./ai/{team}/zappy_ai", "-p", str(settings.port), "-n", team]
    return subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)

def monitor_output(process, stop_event, error_event, output_storage, settings):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((settings.hostname, settings.port))
    except:
        error_event.set()
        return
    print(f"Match connected at {settings.hostname}:{settings.port}")
    received = sock.recv(1024).decode()
    if received == "ko\n":
        sock.close()
        return
    sock.send("GRAPHIC\n".encode())
    while not stop_event.is_set():
        try:
            listen = sock.recv(1024).decode()
        except UnicodeDecodeError:
            break
        if listen:
            if re.search("seg .*\n", listen):
                output_storage.append(listen.strip())
                stop_event.set()
        if process.poll() is not None:
            break
    sock.close()

def terminate_process_and_children(proc_pid):
    try:
        parent = psutil.Process(proc_pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
    except psutil.NoSuchProcess:
        pass

class Match:
    def __init__(self, teamA : str, teamB : str, settings : Settings):
        self.teamA = teamA
        self.teamB = teamB
        self.settings = settings
        self.result = None

    def run(self):
        server_process = launch_server(self.teamA, self.teamB, self.settings)
        if server_process.poll() is not None:
            raise ConnectionRefusedError

        output_storage = []
        stop_event = threading.Event()
        error_event = threading.Event()

        server_thread = threading.Thread(target=monitor_output, args=(server_process, stop_event, error_event, output_storage, self.settings))
        server_thread.start()

        client_processes = [launch_ai(self.teamA, self.settings), launch_ai(self.teamB, self.settings)]

        for client_process in client_processes:
            if client_process.poll() is not None:
                if server_process.poll() is None:
                    terminate_process_and_children(server_process.pid)
                for client_process in client_processes:
                    if client_process.poll() is None:
                        terminate_process_and_children(client_process.pid)
                stop_event.set()
                server_thread.join()
                raise ConnectionRefusedError

        start = time.time()
        elapsed = time.time() - start
        while not stop_event.is_set():
            if all(process.poll() is not None for process in client_processes):
                break
            if server_process.poll() is not None:
                break
            if elapsed > self.settings.timeout * 60:
                break
            if error_event.is_set():
                break
            elapsed = time.time() - start

        if server_process.poll() is None:
            terminate_process_and_children(server_process.pid)
        for client_process in client_processes:
            if client_process.poll() is None:
                terminate_process_and_children(client_process.pid)

        server_thread.join()

        if error_event.is_set():
            raise ConnectionRefusedError

        winner = "Equality"
        if output_storage:
            winner = output_storage[0].split(" ")[1]
        return Result(self.teamA, self.teamB, winner, elapsed)

    def safe_run(self):
        i = 1
        while self.settings.port < 65535:
            try:
                while i % 60 != 0:
                    try:
                        return self.run()
                    except ConnectionRefusedError:
                        self.settings.port += 1
                        time.sleep(1)
                    i += 1
                raise RunFailed
            except RunFailed:
                os.system("killall zappy_server > /dev/null 2>&1")
                time.sleep(10)
            i += 1
        raise RunFailed
