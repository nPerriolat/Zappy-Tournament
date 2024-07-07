##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## FastAES.py
##

"""
@file FastAES.py
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from typing import Optional

"""
We use ECB encryption for fastest encryption.
"""

class AES128:
    def __init__(self, key) -> None:
        """
        :param key: The encryption key (bytes), must be 16 bytes for AES-128.
        """
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes long for AES-128.")
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, plain_text: str) -> bytes:
        """
        Encrypts the plaintext using AES-128 in ECB mode.

        :param plaintext: The plaintext to encrypt (bytes).
        :return: The ciphertext (bytes)
        """
        padded_plaintext = pad(plain_text.encode(), AES.block_size)
        return self.cipher.encrypt(padded_plaintext)

    def decrypt(self, ciphertext) -> Optional[str]:
        """
        Decrypts the ciphertext using AES-128 in ECB mode.

        :param ciphertext: The ciphertext to decrypt (bytes).
        :return: The plaintext (bytes) OR None if the cyphertext is invalid.
        """
        try:
            decrypted_padded_plaintext = self.cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted_padded_plaintext, AES.block_size)
            return plaintext.decode()
        except ValueError:
            return None


def detect_aes_ecb(ciphertext, block_size=16) -> bool:
    """
    Detect if the ciphertext is likely encrypted using AES-128-ECB.

    :param ciphertext: The ciphertext to analyze (bytes).
    :param block_size: The block size for AES (default is 16 bytes for AES).
    :return: True if ECB mode is detected, False otherwise.
    """
    # Split the ciphertext into blocks of the specified block size
    blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
    unique_blocks = set(blocks)

    # If the number of unique blocks is less than the total number of blocks, ECB mode is likely used
    return len(unique_blocks) < len(blocks)
