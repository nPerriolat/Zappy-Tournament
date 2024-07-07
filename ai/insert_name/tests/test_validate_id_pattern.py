from ai.src.utils.messages import validate_id_pattern


class TestValidateIdPattern:

    #  validate strings that exactly match the pattern '[number]'
    def test_valid_pattern(self):
        assert validate_id_pattern('[12345678901234567890]') == True
        assert validate_id_pattern('[01234567890123456789]') == True
        assert validate_id_pattern('[45678901234567890123]') == True

    #  return False for strings without brackets like '123'
    def test_no_brackets(self):
        assert validate_id_pattern('12345678901234567890') == False

    #  return False for empty strings
    def test_empty_string(self):
        assert validate_id_pattern('') == False

    #  return False for strings with only opening or closing bracket like '[' or ']'
    def test_single_bracket(self):
        assert validate_id_pattern('[') == False
        assert validate_id_pattern(']') == False

    #  return False for strings with nested brackets like '[[123]]'
    def test_nested_brackets(self):
        assert validate_id_pattern('[[12345678901234567890]]') == False
