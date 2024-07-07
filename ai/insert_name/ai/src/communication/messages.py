import uuid
import re

from ai.src.communication.latin import Latin
from ai.src.communication.cipher import Cipher
from ai.src.utils.messages import (validate_look_pattern,
                                   validate_encryption_pattern,
                                   validate_inventory_pattern,
                                   get_infos,
                                   extract_direction,
                                   validate_number_pattern,
                                   validate_elevation,
                                   validate_eject_pattern,
                                   validate_uuid_pattern, correction_overload_server)


class Messages(object):
    """
    This class handles sending and receiving messages using encryption.
    """
    def __init__(self, cipher: Cipher, id_nbr: str, language: Latin, debug: bool = False, parrot: bool = False) -> None:
        """
        Initialize a Messages instance with a cipher and an ID number.

        :param cipher: Cipher - Cipher class
        :param id_nbr: str - id of the receiver
        :param language: Latin - Gaffiot Latin - French
        :param debug: bool - flag for debug prints
        :return: None
        """
        self.uuid_used: list[str] = []
        self.id: str = id_nbr
        self.cipher: Cipher = cipher
        self.language: Latin = language
        self.msg: str = 'Broadcast "'
        self.msg_bis: str = 'Broadcast "'
        self.debug: bool = debug
        self.parrot = parrot
        self.server_fixe: str = ''
        self.last_item: bool = False

    def send_coord(self, message: str, pos: tuple[int, int]) -> str:
        """
        Send a message with coordinates to the specified position.

        :param message: str - The message to be sent.
        :param pos: tuple(int, int) - The coordinates of the message.
        :return: str - A formatted string representing the broadcast message.
        """
        new_uuid: str = ''
        while new_uuid in self.uuid_used:
            new_uuid = uuid.uuid4().__str__()
        if new_uuid not in self.uuid_used:
            self.uuid_used.append(new_uuid)
        message += f'#{pos[0]},{pos[1]}'
        encrypted_msg = self.cipher.encryption(message)
        return f'Broadcast "ACCMST {self.id} {new_uuid} {encrypted_msg}"'

    def send(self, message: str) -> str:
        """
        Send an encrypted message.

        :param message: str - The message to be sent.
        :return :str - A formatted string representing the broadcast message.
        """
        new_uuid: str = ""
        while new_uuid in self.uuid_used:
            new_uuid = uuid.uuid4().__str__()
        if new_uuid not in self.uuid_used:
            self.uuid_used.append(new_uuid)
        encrypted_msg = self.cipher.encryption(message)
        return f'Broadcast "ACCMST {self.id} {new_uuid} {encrypted_msg}"'

    def receive(self,
                message: str,
                actions: list = None,
                incantator: bool = False) -> list[tuple[str, str | list[dict[str, str | int | tuple[int, int]]]]]:
        """
        Receive and process a message.

        :param incantator:
        :param message: str - The message received.
        :param actions: any - Additional actions related to the message.
        :return: list [tuple[str, str | list[dict[str, str | int | tuple[int, int]]]]] - A tuple containing the status
        and processed message details.
        """
        if message == "" or message == "\n":
            return [('broadcast', 'ko')]
        messages = list(filter(None, message.split('\n')))
        result = []
        tmp_msg = []
        for msg in messages:
            if self.last_item is True:
                msg = self.server_fixe + msg
                self.last_item = False
            if correction_overload_server(msg, actions) is False:
                self.server_fixe += msg
                self.last_item = True
            else:
                tmp_msg.append(msg)
                self.server_fixe = ''

        msg_actions = [msg for msg in tmp_msg if 'message' not in msg and 'eject' not in msg and 'level' not in msg and 'Elevaation' not in msg]
        msg_broadcast = [msg for msg in tmp_msg if 'message' in msg or 'eject' in msg or 'level' not in msg or 'Elevation' not in msg]
        if incantator:
            msg_actions = [msg for msg in tmp_msg if 'message' not in msg and 'eject' not in msg]
            msg_broadcast = [msg for msg in tmp_msg if 'message' in msg or 'eject' in msg]
            for msg in tmp_msg:
                if 'eject' in msg:
                    print("ERROR Ejected")

        if actions:
            actions = actions[::-1]
        # print(f'msg_action type {type(msg_actions)}\n{msg_actions}')
        # print(f'msg_broadcast type {type(msg_broadcast)}\n{msg_broadcast}')
        # print(f'fuuuuuuuuuuuuck {self.server_fixe}, {actions}')
        for index, message in enumerate(msg_actions):
            if validate_number_pattern(message):
                result.append(('slots', int(message)))
            if validate_inventory_pattern(message):
                result.append(('inventory', message))
            elif validate_look_pattern(message):
                result.append(('look', message))
            elif validate_elevation(message):
                result.append(('elevation', message))
            elif message == 'ok':
                if self.debug:
                    print(f'ok: {actions[index]}')
                try:
                    result.append(('ok', actions[index]))
                except Exception as e:
                    pass
                    print(f'ok : Error: {e}')
                    print(f'actions: {actions}')
                    print(f'msgs actions: {msg_actions}')
                    print(f'msgs all: {tmp_msg}')
            elif message == 'ko':
                if self.debug:
                    print(f'ko: {actions[index]}')
                try:
                    result.append(('ko', actions[index]))
                except Exception as e:
                    pass
                    print(f'KO : Error: {e}')
                    print(f'actions: {actions}')
                    print(f'msgs actions: {msg_actions}')
                    print(f'msgs all: {tmp_msg}')
            else:
                result.append(self.broadcast_received(message))
        for message in msg_broadcast:
            if validate_eject_pattern(message):
                result.append(('eject', message))
            elif validate_elevation(message):
                result.append(('elevation', message))
            else:
                result.append(self.broadcast_received(message))
        if not result:
            result = [('broadcast', 'ko')]
        return result

    def broadcast_received(self, message: str) -> tuple[str, str | list[dict[str, str | int | tuple[int, int]] | str]]:
        """
        Process the received broadcast message and extract relevant information.

        :param message: str - The received broadcast message.
        :return: tuple[str, str | list[dict[str, str | int | tuple[int, int]] | str]] - A tuple containing the status
        and processed message details.
        """
        save_msg: str = message
        match = re.search(r'\d+, ', message)
        if message == "" or message == "\n":
            return ('broadcast', 'ko')
        result: list[dict[str, str | int]] = []
        if self.parrot is True:
            return 'broadcast', [message[match.end() + 1:-1] if match else 'ko']
        if match and len(message) > 4:
            messages = message[match.end() + 1:-1]
            messages = messages.split('|')
            for msg in messages:
                parts = msg.split()
                if len(parts) != 4:
                    result.append({'msg': 'ko'})
                    continue
                if parts[0] != 'ACCMST' or parts[2] in self.uuid_used or validate_encryption_pattern(parts[3]):
                    return 'broadcast', [{'id': 0, 'msg': 'ko'}]
                self.uuid_used.append(parts[2])
                text = parts[3].split('#')
                text = self.cipher.decryption([int(i) for i in text], parts[2])
                text = text.split('#')
                if text[0] == 'est dominus aquilonis' or text[0] == 'Ego sum dominus tuus':
                    direction = extract_direction(save_msg)
                    result.append({
                        'msg': text[0],
                        'direction': direction
                    })
                elif text[0] in self.language.verbum.values():
                    res = get_infos(text)
                    if len(res) == 1:
                        infos = res[0][0]
                        nbr = None
                    else:
                        infos, nbr = res
                    result.append({
                        'id': int(parts[1]),
                        'msg': text[0],
                        **({'coord': tuple(map(int, text[1].split(',')))} if len(text) > 1 and
                            text[1][0].isnumeric() and validate_uuid_pattern(text[1]) is True else {}),
                        **({'infos': list(infos)} if infos is not None else {}),
                        **({'nbr': list(nbr)} if nbr is not None else {})
                    })
                else:
                    result.append({'id': 0, 'msg': 'ko'})
        if not result:
            result = [{'id': 0, 'msg': 'ko'}]
        return 'broadcast', result

    def buf_messages(self, message: str, coord: tuple[int, int] = None,
                     infos: list[list[str]] = None, my_id: int = -1, bis: bool = False) -> None:
        """
        Append an encrypted message to the buffer for broadcasting.

        :param message: str - The message to be sent.
        :param coord: tuple[int, int] - The coordinates of the message.
        :param infos: list[list[str, str] | any] - Additional information related to the message.
        :param my_id: int - Additional id related to the message
        :param bis: bool - Additional buffer, avoid a broadcast with two messages in conflict
        :return: None
        """
        if coord is not None:
            message += f'#{coord[0]},{coord[1]}'
        if infos is not None:
            message += f'#{"~".join(";".join(info) for info in infos)}'
        if my_id != -1:
            message += f'#{my_id}'
        self.buf_msg_default(message, bis)

    def buf_msg_default(self, message: str, bis: bool) -> None:
        """
        Append an encrypted message to the buffer for broadcasting.

        :param message: str - The message to be sent.
        :param bis: bool - Additional buffer, avoid a broadcast with two messages in conflict
        :return: None
        """
        new_uuid: str = uuid.uuid4().__str__()[:7]
        while new_uuid in self.uuid_used:
            new_uuid = uuid.uuid4().__str__()[:7]
        if new_uuid not in self.uuid_used:
            self.uuid_used.append(new_uuid)
        encrypted_msg = self.cipher.encryption(message, new_uuid)
        if bis is False:
            if self.msg == 'Broadcast "':
                self.msg += f'ACCMST {self.id} {new_uuid} {encrypted_msg}'
            else:
                self.msg += f'|ACCMST {self.id} {new_uuid} {encrypted_msg}'
        else:
            if self.msg_bis == 'Broadcast "':
                self.msg_bis += f'ACCMST {self.id} {new_uuid} {encrypted_msg}'
            else:
                self.msg_bis += f'|ACCMST {self.id} {new_uuid} {encrypted_msg}'

    def send_buf(self) -> str:
        """
        Format and return the buffered messages for broadcasting.

        :return: str - A formatted string representing the buffered messages for broadcasting.
        """
        result = self.msg + '"'
        self.msg = 'Broadcast "'
        return result

    def send_buf_bis(self) -> str:
        """
        Format and return the buffered messages for broadcasting.

        :return: str - A formatted string representing the buffered messages for broadcasting.
        """
        result = self.msg_bis + '"'
        self.msg_bis = 'Broadcast "'
        return result
