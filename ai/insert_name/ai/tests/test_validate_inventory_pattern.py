from ai.src.utils.messages import validate_inventory_pattern


class TestValidateInventoryPattern:

    #  returns 1 for a valid formatted string with all required elements
    def test_valid_formatted_string(self):
        valid_string = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6, thystame 7 ]"
        assert validate_inventory_pattern(valid_string) == 1

    #  returns 1 for a string with correct spacing and formatting
    def test_correct_spacing_and_formatting(self):
        valid_string = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6, thystame 7 ]"
        assert validate_inventory_pattern(valid_string) == 1

    #  returns 0 for a string missing one or more required elements
    def test_missing_elements(self):
        invalid_string = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6 ]"
        assert validate_inventory_pattern(invalid_string) == 0

    #  returns 0 for a string with elements in incorrect order
    def test_incorrect_order(self):
        invalid_string = "[ food 1, linemate 2, deraumere 3, mendiane 5, sibur 4, phiras 6, thystame 7 ]"
        assert validate_inventory_pattern(invalid_string) == 0

    #  returns 0 for an empty string
    def test_empty_string(self):
        invalid_string = ""
        assert validate_inventory_pattern(invalid_string) == 0

    #  returns 0 for a string with extra elements not specified in the pattern
    def test_extra_elements(self):
        invalid_string = "[ food 1, linemate 2, deraumere 3, sibur 4, mendiane 5, phiras 6, thystame 7, extra 8 ]"
        assert validate_inventory_pattern(invalid_string) == 0
