##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-antonin.leprest
## File description:
## main
##

import asyncio
import argparse
from server import Server
from start_ia import connect_server


def args_handling():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--help',
        help='show this help message and exit',
        action='help',
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        '-p',
        metavar='Port',
        help='The port of the server',
        required=False,
        default='8080',
        type=str,
    )
    parser.add_argument(
        '-n',
        metavar='Team_Name',
        help='The AI team\'s name',
        required=True,
        type=str,
    )
    parser.add_argument(
        '-h',
        metavar='IP_Adresse',
        help='The IP of the server',
        required=False,
        default='localhost',
        type=str,
    )
    args = parser.parse_args()
    return args


def main() -> None:
    args = args_handling()

    try:
        server_port = int(args.p)
    except ValueError:
        print('Invalid port number')
        return

    team_name = args.n
    server_ip = args.h

    server_conn = Server(server_ip, server_port)
    asyncio.run(connect_server(server_conn, server_port, server_ip, team_name))

if __name__ == '__main__':
    main()
