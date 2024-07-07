##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## start_ia
##

import asyncio
from config import VIEW
from cell import create_grid, check_point_cell
from bfs import bfs
from ia import IA, take_item, response_filter
from itemsPriority import calculate_priority
from server import Server
from multiprocessing import Process


def sync_connect_server(server_port: int, server_ip: str,
                        team_name: str) -> None:
    server_conn = Server(server_ip, server_port)
    asyncio.run(connect_server(server_conn, server_port, server_ip, team_name))


async def connect_server(server_conn: Server, server_port: int,
                         server_ip: str, team_name: str) -> None:
    try:
        server_conn.connect()
        if server_conn.sock:
            response = server_conn.sock.recv(1024)
            if response and response.decode('utf-8') == 'WELCOME\n':
                server_conn.send_team(team_name)
                response = server_conn.sock.recv(1024)
                if 'ko' in response.decode('utf-8'):
                    print('Server did not accept the team name.')
                    server_conn.disconnect()
                    return
                print('Connected to the server.')
                await start_ia(server_conn, server_port, server_ip,
                               team_name)
            else:
                server_conn.disconnect()
        else:
            print('Could not connect to the server.')
    except Exception as e:
        print(f'An error occurred during connection: {e}')
        server_conn.disconnect()


async def fork_command(server_port, server_ip, team_name) -> None:
    child = Process(
        target=sync_connect_server,
        args=(server_port, server_ip, team_name)
    )
    child.start()


async def start_ia(server_conn: Server, server_port: int, server_ip: str,
                   team_name: str) -> None:
    try:
        global VIEW
        ia = IA(1, 1)
        max_baby_count = 0
        child = None

        while ia.alive:
            try:
                if ia.is_following:
                    if ia.inventory.food < 20:
                        ia.is_following = False
                    else:
                        server_conn.send_command('Inventory\n')
                        inventory_response = (await server_conn.get_data()).strip()
                        if 'STOP' in inventory_response:
                            ia.is_following = False
                            inventory_response = (await server_conn.get_data()).strip()
                        inventory_response = await response_filter(
                            ia, server_conn, inventory_response,
                            ['ko', 'ok', 'None']
                        )
                        ia.update_food(inventory_response)
                    continue
                ia.is_waiting = False

                server_conn.send_command('Connect_nbr\n')
                connect_response = await server_conn.get_data()
                connect_response = await response_filter(
                    ia, server_conn, connect_response, [
                        'ko', 'ok', 'None', 'STOP'
                    ]
                )
                if int(connect_response) > 0:
                    await fork_command(server_port, server_ip, team_name)

                server_conn.send_command('Look\n')
                look_response = (await server_conn.get_data()).strip()
                look_response = await response_filter(
                    ia, server_conn, look_response, [
                        'ko', 'ok', 'None', 'Elevation underway', 'STOP'
                    ]
                )
                if '[' not in look_response:
                    continue
                VIEW = look_response

                server_conn.send_command('Inventory\n')
                inventory_response = (await server_conn.get_data()).strip()
                inventory_response = await response_filter(
                    ia, server_conn, inventory_response,
                    ['ko', 'ok', 'None', 'STOP']
                )
                ia.update_food(inventory_response)

                if max_baby_count < 5 and ia.inventory.food > 20:
                    server_conn.send_command('Fork\n')
                    fork_response = (await server_conn.get_data()).strip()
                    fork_response = await response_filter(
                        ia, server_conn, fork_response, ['None'])
                    if 'ok' in fork_response:
                        max_baby_count += 1
                        await fork_command(server_port, server_ip, team_name)

                grid = create_grid(ia.LVL, VIEW)
                for row in grid:
                    for cell in row:
                        cell.add_neighbors(grid)

                start = grid[ia.LVL][ia.LVL]
                checkpoints = check_point_cell(grid, ia.LVL)
                dest = calculate_priority(checkpoints, ia)

                if not await bfs(start, dest, grid, ia, server_conn):
                    break

                ia.on = dest.value
                await take_item(ia, server_conn)
                if ia.is_waiting:
                    ia.is_following = True
            except Exception as err:
                print(f'Error during IA operation: {err}')
                if child:
                    child.join()
                break
    except Exception as e:
        print(f'An error occurred: {e}')
        if child:
            child.join()
    except KeyboardInterrupt:
        print('Interrupted by user.')
        if child:
            child.join()
