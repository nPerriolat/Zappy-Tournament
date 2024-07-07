##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## ia
##

import time
import random
from config import *
from bfs import go_to_friend


class Inventory:
    def __init__(self):
        self.food = 0
        self.linemate = 0
        self.deraumere = 0
        self.sibur = 0
        self.mendiane = 0
        self.phiras = 0
        self.thystame = 0

    def add_item(self, item_type):
        if item_type == FOOD:
            self.food += 1
        elif item_type == LINEMATE:
            self.linemate += 1
        elif item_type == DERAUMERE:
            self.deraumere += 1
        elif item_type == SIBUR:
            self.sibur += 1
        elif item_type == MENDIANE:
            self.mendiane += 1
        elif item_type == PHIRAS:
            self.phiras += 1
        elif item_type == THYSTAME:
            self.thystame += 1

    def remove_item(self, item_type):
        if item_type == 'thystame':
            self.thystame -= 1
        elif item_type == 'linemate':
            self.linemate -= 1
        elif item_type == 'deraumere':
            self.deraumere -= 1
        elif item_type == 'sibur':
            self.sibur -= 1
        elif item_type == 'mendiane':
            self.mendiane -= 1
        elif item_type == 'phiras':
            self.phiras -= 1


class IA:
    def __init__(self, row, col):
        self.LVL = 1
        self.spawn_y = row
        self.spawn_x = col
        self.x = col * CELL_SIZE_X
        self.y = row * CELL_SIZE_Y
        self.look_direction = 'N'
        self.inventory = Inventory()
        self.on = 0
        self.alive = True
        self.list = evolution_list
        self.is_following = False
        self.is_waiting = False


    async def check_broadcast(self, res, server_conn) -> str:
        if 'Current level:' in res:
            elements = res.split('\n')
            for element in elements:
                if element.startswith('Current level:'):
                    tmp2 = element.split(' ')
                    self.LVL = int(tmp2[2])
                    res = res.replace(element, '')
        if 'message' in res:
            self.is_waiting = True
            elements = res.split('\n')
            messages = [element for element in elements if element.startswith('message')]
            instruction = [element for element in elements if not element.startswith('message')]
            for message in messages:
                if 'STOP' in message:
                    return 'STOP'
                elif 'Evolution_LVL_' in message:
                    if self.is_following:
                        await go_to_friend(message, self, server_conn)
                else:
                    rep = message.split(',')
                    rep[1].replace(' ', '')
                    if random.randrange(0,400) == 1:
                        server_conn.send_command(f'Broadcast {rep[1]}\n')
            if len(instruction) - 1 < 0:
                return 'None'
            return instruction[len(instruction) - 1]
        return res

    def update_food(self, res):
        elements = res.strip('[]\n').split(',')
        for elem in elements:
            if 'food' in elem:
                item = elem.split(' ')
                if len(item) >= 3 and item[2].isdigit():
                    self.inventory.food = int(item[2])

    async def check_if_something_is_done(self, response, server_conn):
        if 'dead' in response: self.alive = False
        if not self.alive:
            print('dead')
            return ''

        res = await self.check_broadcast(response, server_conn)
        return res.strip()


async def response_filter(ia, server_conn, response, str_list):
    response = await ia.check_if_something_is_done(response, server_conn)
    elements = response.split('\n')

    max_iterations = 4
    iterations = 0

    while elements and iterations < max_iterations:
        found = False
        for element in elements:
            if any(s in element for s in str_list):
                found = True
                break

        if found:
            response = (await server_conn.get_data()).strip()
            response = await ia.check_if_something_is_done(response, server_conn)
            elements = response.split('\n')
            iterations += 1

            if iterations >= max_iterations:
                break
        else:
            break
    return response


async def switch(value, ia, server_conn) -> None:
    valid_items = {FOOD, LINEMATE, DERAUMERE, SIBUR, MENDIANE, PHIRAS, THYSTAME}
    if value not in valid_items:
        return

    item_name = get_item_name(value)
    count = item_name.count('2')
    count2 = item_name.count('3')
    if count == 0:
        server_conn.send_command(f'Take {item_name}\n')
        response = (await server_conn.get_data()).strip()
        response = await response_filter(ia, server_conn, response, ['None'])

        if response == 'ok':
            ia.inventory.add_item(value)
    elif count2 > 0:
        server_conn.send_command(f'Take food\n')
        response = (await server_conn.get_data()).strip()
        response = await response_filter(ia, server_conn, response, ['None'])

        if response == 'ok':
            ia.inventory.add_item(value)


async def take_item(ia, server_conn) -> None:
    tmp = str(ia.on)
    tmp = tmp.replace('1', '')

    if not (ia.on >= 10 and ia.on > 2):
        await switch(ia.on, ia, server_conn)
    else:
        for char in tmp:
            item = int(char)
            await switch(item, ia, server_conn)


async def evolved_intern_action(ia, server_conn, drop_item):
    element = ia.list[ia.LVL - 1].split(',')
    all_set_ok = True

    if not drop_item:
        for r in element:
            server_conn.send_command(f'Set {r}\n')
            response = (await server_conn.get_data()).strip()
            response = await response_filter(ia, server_conn, response, ['None'])

            if response == 'ko':
                all_set_ok = False
                break
            ia.inventory.remove_item(r)
            drop_item = True

    if not all_set_ok:
        return "ko", drop_item

    server_conn.send_command('Incantation\n')
    response = (await server_conn.get_data()).strip()
    response = await response_filter(ia, server_conn, response, ['ok', 'None'])
    if "ko" in response:
        return "ko", drop_item
    response = (await server_conn.get_data()).strip()
    response = await response_filter(ia, server_conn, response, ['None'])
    if 'ko' in response:
        return 'ko', drop_item
    return 'ok', drop_item


async def broadcasted_evolution(ia, server_conn, nb_player, stat, lvl, players_required):
    drop_item = False

    if random.randrange(0, 20) == 1:
        while nb_player < players_required:
            if ia.inventory.food < 20:
                server_conn.send_command('Broadcast STOP\n')
                break
            test_message = f'Evolution_{lvl}'
            server_conn.send_command(f'Broadcast {test_message}\n')
            server_conn.send_command('Inventory\n')
            inventory_response = (await server_conn.get_data()).strip()
            inventory_response = await response_filter(ia, server_conn, inventory_response, ['ko', 'ok', 'None'])
            ia.update_food(inventory_response)
            stat, drop_item = await evolved_intern_action(ia, server_conn, drop_item)
            if 'ok' in stat:
                break
            time.sleep(0.6)
        return stat
    else:
        stat, drop_item = await evolved_intern_action(ia, server_conn, drop_item)
        return stat


async def evolved(ia, server_conn, start):
    tmp = str(start.value)
    nb_player = tmp.count('2')
    stat = 'ko'

    if ia.LVL == 1 and ia.inventory.linemate >= 1 and ia.inventory.food >= 15 and nb_player >= 1:
        stat, _ = await evolved_intern_action(ia, server_conn, False)
    elif ia.LVL == 2 and ia.inventory.linemate >= 1 and ia.inventory.deraumere >= 1 and ia.inventory.sibur >= 1 and ia.inventory.food >= 20 and nb_player >= 2:
        stat, _ = await evolved_intern_action(ia, server_conn, False)
    elif ia.LVL == 3 and ia.inventory.linemate >= 2 and ia.inventory.sibur >= 1 and ia.inventory.phiras >= 2 and ia.inventory.food >= 20 and nb_player >= 2:
        stat, _ = await evolved_intern_action(ia, server_conn, False)
    elif ia.LVL == 4 and ia.inventory.linemate >= 1 and ia.inventory.deraumere >= 1 and ia.inventory.sibur >= 2 and ia.inventory.phiras >= 1 and ia.inventory.food >= 20:
        stat, _ = await broadcasted_evolution(ia, server_conn, nb_player, stat, 'LVL_4', 4)
    elif ia.LVL == 5 and ia.inventory.linemate >= 1 and ia.inventory.deraumere >= 2 and ia.inventory.sibur >= 1 and ia.inventory.mendiane >= 3 and ia.inventory.food >= 10:
        stat, _ = await broadcasted_evolution(ia, server_conn, nb_player, stat, 'LVL_5', 4)
    elif ia.LVL == 6 and ia.inventory.linemate >= 1 and ia.inventory.deraumere >= 2 and ia.inventory.sibur >= 3 and ia.inventory.phiras >= 1 and ia.inventory.food >= 10:
        stat, _ = await broadcasted_evolution(ia, server_conn, nb_player, stat, 'LVL_6', 6)
    elif ia.LVL == 7 and ia.inventory.linemate >= 2 and ia.inventory.deraumere >= 2 and ia.inventory.sibur >= 2 and ia.inventory.mendiane >= 2 and ia.inventory.phiras >= 2 and ia.inventory.thystame >= 1 and ia.inventory.food >= 10:
        stat, _ = await broadcasted_evolution(ia, server_conn, nb_player, stat, 'LVL_7', 6)

    return stat


def get_item_name(item_value) -> str:
    item_names = {
        FOOD: 'food',
        LINEMATE: 'linemate',
        DERAUMERE: 'deraumere',
        SIBUR: 'sibur',
        MENDIANE: 'mendiane',
        PHIRAS: 'phiras',
        THYSTAME: 'thystame'
    }
    return item_names.get(item_value, 'unknown')
