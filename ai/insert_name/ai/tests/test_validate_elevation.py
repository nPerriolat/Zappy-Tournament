from ai.src.utils.messages import validate_elevation


class TestValidateElevation:

    #  input is 'Elevation underway' returns True
    def test_elevation_underway_returns_true(self):
        assert validate_elevation('Elevation underway') == True

    #  input is 'Current level: 100' returns True
    def test_current_level_100_returns_true(self):
        assert validate_elevation('Current level: 100') == True

    #  input is 'Current level: 0' returns True
    def test_current_level_0_returns_true(self):
        assert validate_elevation('Current level: 0') == True

    #  input is 'Current level: ' returns False
    def test_current_level_empty_returns_false(self):
        assert validate_elevation('Current level: ') == False

    #  input is 'Current level: -1' returns False
    def test_current_level_negative_returns_false(self):
        assert validate_elevation('Current level: -1') == False

    #  input is 'Current level: abc' returns False
    def test_current_level_non_numeric_returns_false(self):
        assert validate_elevation('Current level: abc') == False
