import sys
import os
import socket

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.src.zappy_ai import Bot


class Test__Init__:

    def test_cli_num_assignment(self, mocker):
        mocker.patch('socket.socket')
        serv_info = [42, 10, 10]
        cli_socket = socket.socket()
        bot = Bot(serv_info, cli_socket)
        assert bot.cli_num == 42, "cli_num should be assigned the first element of serv_info"

    def test_empty_serv_info_handling(self, mocker):
        mocker.patch('socket.socket')
        serv_info = []
        cli_socket = socket.socket()
        with pytest.raises(IndexError):
            bot = Bot(serv_info, cli_socket)


class TestSend:

    def test_send_valid_encoded_action(self, mocker):
        mock_socket = mocker.Mock()
        bot = Bot([1, 5, 5], mock_socket)
        bot.send_action("Forward\n")
        mock_socket.send.assert_called_once_with("Forward\n".encode())

    def test_send_empty_string_input(self, mocker):
        mock_socket = mocker.Mock()
        bot = Bot([1, 5, 5], mock_socket)
        bot.send_action("")
        mock_socket.send.assert_called_once_with("".encode())


class TestLookAround:

    def test_look_around_sends_correct_command(self, mocker):
        mock_socket = mocker.MagicMock()
        serv_info = [1, 10, 10]
        bot = Bot(serv_info, mock_socket)
        bot.look_around()
        mock_socket.send.assert_called_once_with("Look\n".encode())

    def test_look_around_handles_socket_errors(self, mocker):
        mock_socket = mocker.MagicMock()
        mock_socket.send.side_effect = Exception("Socket error")
        serv_info = [1, 10, 10]
        bot = Bot(serv_info, mock_socket)
        with pytest.raises(Exception) as exc_info:
            bot.look_around()
        assert str(exc_info.value) == "Socket error"
        mock_socket.send.assert_called_once_with("Look\n".encode())


class TestForward:

    def test_forward_sends_correct_command(self, mocker):
        mock_socket = mocker.MagicMock()
        bot = Bot([1, 10, 10], mock_socket)
        bot.forward()
        mock_socket.send.assert_called_once_with("Forward\n".encode())

    def test_forward_called_with_closed_socket(self, mocker):
        mock_socket = mocker.MagicMock()
        mock_socket.send.side_effect = socket.error("Socket is closed")
        bot = Bot([1, 10, 10], mock_socket)
        with pytest.raises(socket.error) as excinfo:
            bot.forward()
        assert str(excinfo.value) == "Socket is closed"


class TestRight:

    def test_right_command_sent_correctly(self, mocker):
        mock_socket = mocker.MagicMock()
        serv_info = [1, 5, 5]
        bot = Bot(serv_info, mock_socket)
        bot.right()
        mock_socket.send.assert_called_once_with("Right\n".encode())

    def test_right_with_non_responsive_server(self, mocker):
        mock_socket = mocker.MagicMock()
        mock_socket.send.side_effect = socket.timeout
        serv_info = [1, 5, 5]
        bot = Bot(serv_info, mock_socket)
        with pytest.raises(socket.timeout):
            bot.right()


class TestLeft:

    def test_left_command_sent_correctly(self, mocker):
        mock_socket = mocker.MagicMock()
        bot = Bot([1, 10, 10], mock_socket)
        bot.left()
        mock_socket.send.assert_called_once_with("Left\n".encode())

    def test_socket_connection_broken(self, mocker):
        mock_socket = mocker.MagicMock()
        mock_socket.send.side_effect = Exception("Connection broken")
        bot = Bot([1, 10, 10], mock_socket)
        with pytest.raises(Exception) as exc_info:
            bot.left()
        assert str(exc_info.value) == "Connection broken"


class TestNbrOfSlot:
    def test_sends_connect_nbr_command(self, mocker):
        mock_socket = mocker.MagicMock()
        bot = Bot([1, 5, 5], mock_socket)
        bot.nbr_of_slot()
        mock_socket.send.assert_called_once_with("Connect_nbr\n".encode())

    def test_socket_connection_broken_during_send(self, mocker):
        mock_socket = mocker.MagicMock()
        mock_socket.send.side_effect = Exception("Connection error")
        bot = Bot([1, 5, 5], mock_socket)
        with pytest.raises(Exception) as exc_info:
            bot.nbr_of_slot()
        assert "Connection error" in str(exc_info.value)


class TestInventory:

    def test_inventory_command_sent(self, mocker):
        mock_socket = mocker.MagicMock()
        serv_info = [1, 10, 20, 30]
        bot = Bot(serv_info, mock_socket)
        bot.check_inventory()
        mock_socket.send.assert_called_once_with("Inventory\n".encode())

    def test_inventory_socket_broken(self, mocker):
        mock_socket = mocker.MagicMock()
        mock_socket.send.side_effect = socket.error("Broken connection")
        serv_info = [1, 10, 20, 30]
        bot = Bot(serv_info, mock_socket)
        with pytest.raises(socket.error):
            bot.check_inventory()


class TestIncantation:

    def test_incantation_sends_correct_command(self, mocker):
        mock_socket = mocker.MagicMock()
        serv_info = [1, 5, 5]
        bot = Bot(serv_info, mock_socket)
        bot.incantation()
        mock_socket.send.assert_called_once_with("Incantation\n".encode())

    def test_incantation_with_closed_socket(self, mocker):
        mock_socket = mocker.MagicMock()
        mock_socket.send.side_effect = socket.error("Socket is closed")
        serv_info = [1, 5, 5]
        bot = Bot(serv_info, mock_socket)
        with pytest.raises(socket.error):
            bot.incantation()
