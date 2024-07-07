##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## CircularArray.py
##

class CircularArray:
    def __init__(self, array: list, size: int):
        self.array = array
        self.size = size
        self.current_index: int = 0

    def get_current(self):
        return self.array[self.current_index]

    def get_previous(self):
        index = (self.current_index - 1) % self.size
        return self.array[index]

    def set_index(self, index):
        self.current_index = index

    def insert_element(self, element):
        self.array.insert(self.current_index, element)
        self.size += 1

    def remove_current_element(self):
        self.array.pop(self.current_index)
        self.size -= 1

    def advance(self):
        self.current_index = (self.current_index + 1) % self.size
