##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## server
##

import socket
import asyncio

class Server:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None


    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_ip, self.server_port))
            print(f'Connected to {self.server_ip} on port {self.server_port}')
        except socket.error as e:
            print(f'Failed to connect to the server: {e}')
            self.sock = None


    def disconnect(self):
        if self.sock:
            try:
                self.sock.close()
            except socket.error as e:
                print(f'Failed to close the socket: {e}')
            finally:
                self.sock = None


    async def get_data(self):
        if not self.sock:
            print('No socket connection.')
            return ''

        try:
            response = b''
            while True:
                chunk = await asyncio.to_thread(self.sock.recv, 1024)
                if not chunk:
                    print('Socket connection closed by the server.')
                    break
                response += chunk
                if response.endswith(b'\n'):
                    break
            return response.decode('utf-8').strip()
        except socket.error as e:
            print(f'Socket error: {e}')
            self.disconnect()
            return ''


    def send_command(self, command):
        if self.sock:
            try:
                print(f'send command: {command}')
                self.sock.sendall(command.encode('utf-8'))
            except socket.error as e:
                print(f'Failed to send command: {e}')
                self.disconnect()
        else:
            print('Not connected to the server.2')


    def send_team(self, team):
        if self.sock:
            try:
                print(f'Sending team name: {team}')
                self.sock.sendall((team + '\n').encode('utf-8'))
                print('Sent team name')
            except socket.error as e:
                print(f'Failed to send team name: {e}')
                self.disconnect()
        else:
            print('Not connected to the server.3')
