from ai.src.gameplay.enum_gameplay import Directions


class TestDirections:

    #  adding NORTH and 1 results in EAST
    def test_adding_north_and_1_results_in_east(self):
        assert Directions.NORTH + 1 == Directions.EAST.value

    #  adding EAST and 1 results in SOUTH
    def test_adding_east_and_1_results_in_south(self):
        assert Directions.EAST + 1 == Directions.SOUTH.value

    #  adding SOUTH and 1 results in WEST
    def test_adding_south_and_1_results_in_west(self):
        assert Directions.SOUTH + 1 == Directions.WEST.value

    #  adding NORTH and 4 results in NORTH
    def test_adding_north_and_4_results_in_north(self):
        assert Directions.NORTH + 4 == Directions.NORTH.value

    #  adding EAST and 4 results in EAST
    def test_adding_east_and_4_results_in_east(self):
        assert Directions.EAST + 4 == Directions.EAST.value

    #  adding SOUTH and 4 results in SOUTH
    def test_adding_south_and_4_results_in_south(self):
        assert Directions.SOUTH + 4 == Directions.SOUTH.value
