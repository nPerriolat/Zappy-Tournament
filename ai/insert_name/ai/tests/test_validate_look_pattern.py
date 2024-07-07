from ai.src.utils.messages import validate_look_pattern


class TestValidateLookPattern:

    #  input string exactly matches '[ player]'
    def test_exact_match_player(self):
        assert validate_look_pattern('[ player]') == True

    #  input string matches '[ player123]'
    def test_match_player123(self):
        assert validate_look_pattern('[ player123]') == True

    #  input string matches '[ player_name]'
    def test_match_player_name(self):
        assert validate_look_pattern('[ player_name]') == True

    #  input string is empty
    def test_empty_string(self):
        assert validate_look_pattern('') == False

    #  input string does not start with '['
    def test_no_start_bracket(self):
        assert validate_look_pattern(' player]') == False

    #  input string does not end with ']'
    def test_no_end_bracket(self):
        assert validate_look_pattern('[ player') == False
