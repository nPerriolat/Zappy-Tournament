from ai.src.communication.cipher import Cipher
from ai.src.communication.latin import Latin
from ai.src.communication.messages import Messages
from ai.src.utils.messages import validate_inventory_pattern


class TestValidateLookPattern:

    #  returns 1 for valid formatted string with all required elements
    def test_valid_formatted_string(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        valid_string = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6, thystame 7 ]"
        assert validate_inventory_pattern(valid_string) == 1

    #  returns 0 for string missing one or more required elements
    def test_missing_elements(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        invalid_string = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6 ]"
        assert validate_inventory_pattern(invalid_string) == 0

    #  returns 0 for string with elements in incorrect order
    def test_incorrect_order(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        invalid_string = "[ food 1, linemate 2, deraumere 3, mendiane 5, sibur 4, phiras 6, thystame 7 ]"
        assert validate_inventory_pattern(invalid_string) == 0

    #  returns 0 for empty string
    def test_empty_string(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        invalid_string = ""
        assert validate_inventory_pattern(invalid_string) == 0

    #  returns 0 for string with extra elements not specified in pattern
    def test_extra_elements(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        invalid_string = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6, thystame 7, extra 8 ]"
        assert validate_inventory_pattern(invalid_string) == 0

    #  returns 0 for string with negative quantities
    def test_negative_quantities(self):
        cipher = Cipher("testkey")
        language = Latin()
        messages = Messages(cipher, "123", language)
        invalid_string = "[ food -1, linemate -2, deraumere -3, sibur -4, mendiane -5, phiras -6, thystame -7 ]"
        assert validate_inventory_pattern(invalid_string) == 0
