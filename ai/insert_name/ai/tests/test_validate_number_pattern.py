from ai.src.utils.messages import validate_number_pattern


class TestValidateNumberPattern:

    #  input is a string of digits only
    def test_digits_only(self):
        assert validate_number_pattern("1234567890") == True

    #  input is an empty string
    def test_empty_string(self):
        assert validate_number_pattern("") == False

    #  input is a string with leading zeros
    def test_leading_zeros(self):
        assert validate_number_pattern("001234") == True

    #  input contains alphabetic characters
    def test_alphabetic_characters(self):
        assert validate_number_pattern("123abc") == False

    #  input contains special characters
    def test_special_characters(self):
        assert validate_number_pattern("123!@#") == False

    #  input contains whitespace characters
    def test_whitespace_characters(self):
        assert validate_number_pattern("123 456") == False
