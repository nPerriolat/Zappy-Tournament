import numpy as np
import math


def calc_encryption_key(key: str) -> list[list[int]]:
    """
    Calculate the encryption key matrix from the given key string.

    :param: key: str - The key string used to generate the encryption key matrix.
    :return: list[list[int]] - The encryption key matrix derived from the key string.
    """
    key_len = len(key)
    matrix_size = int(np.ceil(np.sqrt(key_len)))
    # print(matrix_size)
    matrix = [
        [ord(key[count]) if count < key_len else 0 for count in range(i * matrix_size, (i + 1) * matrix_size)]
        for i in range(matrix_size)]

    return matrix


class Cipher(object):
    """
    The Cipher class provides methods for encrypting and decrypting messages using a key matrix derived from a given
    key string. It converts messages into matrices, performs matrix multiplication for encryption, and uses the
    inverse of the key matrix for decryption.
    """

    def __init__(self, encryption_key: str) -> None:
        """
        The __init__ method initializes an instance of the Cipher class by calculating the encryption key matrix from
        the provided encryption key string and then computing its inverse for decryption purposes.

        :param encryption_key: str - encryption key string
        :return: None
        """
        self.key: [[int]] = calc_encryption_key(encryption_key)
        self.key_inv: np.ndarray = np.linalg.inv(self.key)

    def message_matrix(self, message: str) -> list[list[int]]:
        """
        Convert a message into a matrix of ASCII values based on the encryption key matrix size.

        :param message: str - The input message to be converted into a matrix.
        :return list[list[int]]: - A matrix of ASCII values representing the input message.
        """
        matrix_size = len(self.key)
        msg_len = len(message)
        matrix = [
            [ord(message[count]) if count < msg_len else 0 for count in range(i * matrix_size, (i + 1) * matrix_size)]
            for i in range(math.ceil(msg_len / matrix_size))
        ]
        return matrix

    def calc_result_matrix(self, message_matrix: list[list[int]]) -> list[int]:
        """
        Calculate the result matrix by multiplying the message matrix with the encryption key matrix.

        :param message_matrix: list[list[int]] - The matrix representing the message to be encrypted.
        :return: list[int] - The result matrix after the multiplication operation.
        """
        result_matrix = [
            sum(message_matrix[i][k] * self.key[k][j] for k in range(len(self.key)))
            for i in range(len(message_matrix))
            for j in range(len(self.key))
        ]
        return result_matrix

    def encryption(self, message: str, new_uuid: str) -> str:
        """
        Encrypts the input message using the encryption key matrix.

        :param message: str - The message to be encrypted.
        :return: list[int] - The encrypted message as a list of integers.
        """
        matrix_msg: list[[int]] = self.message_matrix(message)
        resulting_matrix: list[int] = self.calc_result_matrix(matrix_msg)
        calc = int(new_uuid[4:], 16)
        resulting_matrix = [x + calc for x in resulting_matrix]
        resulting_msg: str = '#'.join(str(x) for x in resulting_matrix)
        return resulting_msg

    def decryption(self, message: list[int], old_uuid: str) -> str:
        """
        Decrypts an encrypted message using the decryption key matrix.

        :param message: list[int] - The encrypted message to be decrypted as a list of integers.
        :return: str - The decrypted message as a string.
        """
        matrix_size: int = len(self.key)
        calc = int(old_uuid[4:], 16)
        message = [x - calc for x in message]
        reversed_message_matrix = np.array(message).reshape(-1, matrix_size)
        decrypted_matrix = np.dot(reversed_message_matrix, self.key_inv)
        decrypted_matrix = np.round(decrypted_matrix).astype(int)
        decrypted_message = ''.join(chr(num) for row in decrypted_matrix for num in row if 32 <= num <= 126)
        return decrypted_message
