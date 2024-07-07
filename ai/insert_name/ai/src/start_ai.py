import sys

from ai.src.server import connexion
from ai.src.player.parent_ai import ParentAI
from ai.src.player.pusher import Pusher
from ai.src.player.collector import Collector
from ai.src.player.pnj import Pnj
from ai.src.player.incantator import Incantator
from ai.src.player.north_guard import NorthGuard
from ai.src.player.first_born import First_born
from ai.src.player.progenitor import Progenitor
from ai.src.zappy_ai import display_help, connection


def start_ai():
    """
    The main function is the entry point of the program.

    :return: sys.exit 0 or 84(error)
    """
    # try:
    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        return display_help()
    name = ""
    port = ""
    machine = ""
    debug = False
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-p':
            port = sys.argv[i + 1]
        elif sys.argv[i] == '-n':
            name = sys.argv[i + 1]
        elif sys.argv[i] == '-h':
            machine = sys.argv[i + 1]
        elif sys.argv[i] == '-d':
            debug = True
        elif sys.argv[i - 1] != '-p' and sys.argv[i - 1] != '-n' and sys.argv[i - 1] != '-h':
            raise ValueError("Invalid argument")
    server_info, cli_socket = connection(port, name, machine)
    mybot = ParentAI(server_info, cli_socket, debug, machine, port, name)
    # mybot = Pnj(server_info, cli_socket, debug)
    # mybot = Pusher(server_info, cli_socket, debug)
    # mybot = Collector(server_info, cli_socket, debug)
    # mybot = NorthGuard(server_info, cli_socket, debug)
    # mybot = Incantator(server_info, cli_socket, debug)
    # mybot = Depot(server_info, cli_socket, debug)
    mybot.run()
    # except (ValueError, AssertionError, ConnectionError, ConnectionRefusedError, Exception) as e:
    #     print(f"NOP: {e}")
    #     return 84
    return 0
