import pytest

from ai.src.utils.messages import extract_direction


class TestExtractDirection:

    #  extracts first integer from a string with multiple integers
    def test_extracts_first_integer_from_multiple(self):
        assert extract_direction("Turn 45 degrees then 90 degrees") == 45

    #  extracts integer from a string with leading and trailing spaces
    def test_extracts_integer_with_spaces(self):
        assert extract_direction("   123   ") == 123

    #  extracts integer from a string with special characters
    def test_extracts_integer_with_special_characters(self):
        assert extract_direction("Move @#$%^&*() 789!") == 789

    #  raises an error when no integers are present in the string
    def test_raises_error_when_no_integers(self):
        with pytest.raises(AttributeError):
            extract_direction("No numbers here!")

    #  handles very large integers correctly
    def test_handles_very_large_integers(self):
        assert extract_direction("The number is 12345678901234567890") == 12345678901234567890

    #  handles negative numbers correctly
    def test_not_handles_neg_numbers(self):
        assert extract_direction("Temperature is -20 degrees") != -20

    #  extracts integer from a message string
    def test_extracts_integer_in_message_string(self):
        assert extract_direction("message 7, 'Hello world'") == 7

    #  extracts integer from a broadcast string
    def test_extracts_integer_in_broadcast_string(self):
        assert extract_direction("Broadcast 7, 'Hello world'") == 7
