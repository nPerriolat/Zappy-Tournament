from socket import socket, AF_INET, SOCK_STREAM


def connect(port: str, team_name: str, host: str) -> tuple[list[int], socket]:
    """
    The connect function establishes a TCP connection to a specified host and port, sends a team name, and processes the received data into a list of integers, returning this list along with the socket object.

    :param port: The port number to connect to.
    :param team_name: A string representing the name of the team.
    :param host: The hostname or IP address to connect to.
    :return: A tuple containing a list of integers and the socket object used for the connection.
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, int(port)))
    welcome_message = client_socket.recv(10_000).decode().strip()
    client_socket.send(f"{team_name}\n".encode())
    cli_number = client_socket.recv(100_000).decode()
    new_ntq = cli_number.split()
    result = []
    if new_ntq != ['ko']:
        result = list(map(int, filter(None, new_ntq[:3])))
    else:
        print(f"Error\n for: {cli_number} or {welcome_message}")
        client_socket.close()
        client_socket = None
        result = None
    return result, client_socket
