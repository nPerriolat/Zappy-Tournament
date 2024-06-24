#!/usr/bin/env python3

import subprocess
import threading
import re
import signal
import os
import psutil
import time

from src.settings import Settings
from src.result import Result

def launch_server(teamA : str, teamB : str, settings : Settings):
    command = ["./server/zappy_server", "-p", str(settings.port), "-x", str(settings.x), "-y", str(settings.y), "-n", teamA, teamB, "-c", str(settings.starting_eggs), "-f", str(settings.frequence)]
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def launch_ai(team : str, settings : Settings):
    command = [f"./ai/{team}/zappy_ai", "-p", str(settings.port), "-n", team]
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# TO FIX
def monitor_output(process, stop_event, output_storage):
    print(f"Monitoring output for process with PID {process.pid}")
    while not stop_event.is_set():
        output = process.stdout.readline()
        if output:
            print(output.strip())
            if re.search(r'Team .* as won', output):
                output_storage.append(output.strip())
                stop_event.set()
                print("Stop event has been set")
        if process.poll() is not None:
            print(f"Process with PID {process.pid} has terminated")
            break

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
        server_process = launch_server(teamA, teamB, settings)
        if server_process.poll() is not None:
            print(f"Failed to start server process. Return code: {server_process.poll()}")
            return

        output_storage = []
        stop_event = threading.Event()

        server_thread = threading.Thread(target=monitor_output, args=(server_process, stop_event, output_storage))
        server_thread.start()

        client_processes = [launch_ai(teamA, settings), launch_ai(teamB, settings)]

        for client_process in client_processes:
            if client_process.poll() is not None:
                print(f"Failed to start client process. Return code: {client_process.poll()}")
                return

        # TO FIX
        while not stop_event.is_set():
            if all(process.poll() is not None for process in client_processes):
                print("all(process.poll() is not None for process in client_processes)")
                break
            if server_process.poll() is not None:
                print("server_process.poll() is not None")
                break

        if server_process.poll() is None:
            terminate_process_and_children(server_process.pid)
        for client_process in client_processes:
            if client_process.poll() is None:
                terminate_process_and_children(client_process.pid)

        server_thread.join()

        if output_storage:
            print(f"Found message: {output_storage[0]}")
        else:
            print("Processus terminated without winner")
