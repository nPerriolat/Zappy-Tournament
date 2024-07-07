import socket

from ai.src.player.player import Player


class Hansel(Player):

    def __init__(self, serv_info: list[int], cli_socket: socket, debug_mode: bool = False):
        super().__init__(serv_info, cli_socket, debug_mode)
        self.give_all_food()

    def give_all_food(self) -> None:
        """
        Give all the food items in the player's inventory.

        This method adds 'Set' action for each food item in the player's inventory to the action queue.
        :return: None
        """
        for _ in range(self.inventory['food'] - 1):
            self.queue.append(('Set', 'food'))

    def make_action(self) -> None:
        if len(self.actions) >= 1:
            return
        if len(self.queue) > 0:
            self.apply_action()
