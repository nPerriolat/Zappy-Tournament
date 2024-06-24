#!/usr/bin/env python3

import subprocess
import threading
import re
import signal
import os
import psutil

def launch_server():
    command = ["./server/zappy_server", "-p", "8080", "-x", "10", "-y", "10", "-n", "team1", "team2", "-c", "3", "-f", "100"]
    print(f"Lauch {command}")
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def launch_client1():
    command = ["./ai/team1/zappy_ai", "-p", "8080", "-n", "team1"]
    print(f"Lauch {command}")
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def launch_client2():
    command = ["./ai/team1/zappy_ai", "-p", "8080", "-n", "team2"]
    print(f"Lauch {command}")
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def monitor_output(process, stop_event, output_storage):
    # Lire les sorties du processus
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
    print(f"Terminating pid={proc_pid}")
    try:
        # Terminer les processus enfants d'abord
        parent = psutil.Process(proc_pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
    except psutil.NoSuchProcess:
        pass

def main():
    # Lancer le serveur
    server_process = launch_server()

    if server_process.poll() is not None:
        print(f"Failed to start server process. Return code: {server_process.poll()}")
        return

    # Stocker les phrases trouvées
    output_storage = []

    # Utiliser un événement pour arrêter les threads
    stop_event = threading.Event()

    # Créer et démarrer un thread pour surveiller la sortie du serveur
    server_thread = threading.Thread(target=monitor_output, args=(server_process, stop_event, output_storage))
    server_thread.start()

    # Lancer les clients
    client_processes = [launch_client1(), launch_client2()]

    for client_process in client_processes:
        if client_process.poll() is not None:
            print(f"Failed to start client process. Return code: {client_process.poll()}")
            # Afficher les erreurs des clients
            stderr = client_process.stderr.read()
            print(f"Client process stderr: {stderr}")
            return
    
    client_threads = []
    for client_process in client_processes:
        client_thread = threading.Thread(target=monitor_output, args=(client_process, stop_event, output_storage))
        client_thread.start()
        client_threads.append(client_thread)

    print("All process has been lauched")
    # Attendre que le thread du serveur trouve la phrase ou que tous les processus se terminent
    while not stop_event.is_set():
        if all(process.poll() is not None for process in client_processes):
            print("all(process.poll() is not None for process in client_processes)")
            break
        if server_process.poll() is not None:
            print("server_process.poll() is not None")
            break
    # Arrêter tous les processus
    if server_process.poll() is None:
        terminate_process_and_children(server_process.pid)
    for client_process in client_processes:
        if client_process.poll() is None:
            terminate_process_and_children(client_process.pid)

    # Attendre que le thread du serveur termine
    server_thread.join()

    # Afficher le message trouvé
    if output_storage:
        print(f"Found message: {output_storage[0]}")
    else:
        print("Processus terminated without winner")

if __name__ == "__main__":
    main()