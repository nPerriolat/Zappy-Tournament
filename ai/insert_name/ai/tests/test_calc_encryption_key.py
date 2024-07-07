import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.src.communication.cipher import calc_encryption_key



class TestCalcEncryptionKey:

    #  Converts a string key into a square matrix of ASCII values
    def test_converts_string_key_to_square_matrix(self):
        key = "testkey"
        expected_matrix = [
            [116, 101, 115],
            [116, 107, 101],
            [121, 0, 0]
        ]
        result = calc_encryption_key(key)
        assert result == expected_matrix

    #  Handles keys with length equal to a perfect square
    def test_key_length_perfect_square(self):
        key = "perfectsq"
        expected_matrix = [
            [112, 101, 114],
            [102, 101, 99],
            [116, 115, 113]
        ]
        result = calc_encryption_key(key)
        assert result == expected_matrix

    #  Handles keys with length less than a perfect square by padding with zeros
    def test_key_length_less_than_perfect_square(self):
        key = "short"
        expected_matrix = [
            [115, 104, 111],
            [114, 116, 0],
            [0, 0, 0]
        ]
        result = calc_encryption_key(key)
        assert result == expected_matrix

    #  Empty string as key
    def test_empty_string_key(self):
        key = ""
        expected_matrix = []
        result = calc_encryption_key(key)
        assert result == expected_matrix

    #  Single character key
    def test_single_character_key(self):
        key = "a"
        expected_matrix = [
            [97]
        ]
        result = calc_encryption_key(key)
        assert result == expected_matrix

    #  Key with length just below a perfect square
    def test_key_length_just_below_perfect_square(self):
        key = "almostperfect"
        expected_matrix = [
            [97, 108, 109, 111],
            [115, 116, 112, 101],
            [114, 102, 101, 99],
            [116, 0, 0, 0]
        ]
        result = calc_encryption_key(key)
        assert result == expected_matrix
