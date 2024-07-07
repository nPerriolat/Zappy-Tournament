from ai.src.gameplay.evolution import evolution


class TestEvolution:

    #  returns correct dictionary for level 1
    def test_returns_correct_dict_for_level_1(self):
        assert evolution(1) == {"player": 1, "linemate": 1}

    #  returns correct dictionary for level 2
    def test_returns_correct_dict_for_level_2(self):
        assert evolution(2) == {"player": 2, "linemate": 1, "sibur": 1, "phiras": 2}

    #  returns correct dictionary for level 3
    def test_returns_correct_dict_for_level_3(self):
        assert evolution(3) == {"player": 2, "linemate": 2, "deraumere": 1, "sibur": 1, "mendiane": 3}

    #  handles negative level input gracefully
    def test_handles_negative_level_input_gracefully(self):
        assert evolution(-1) is None

    #  handles zero level input gracefully
    def test_handles_zero_level_input_gracefully(self):
        assert evolution(0) is None

    #  handles level input greater than 7 gracefully
    def test_handles_level_input_greater_than_7_gracefully(self):
        assert evolution(8) is None
