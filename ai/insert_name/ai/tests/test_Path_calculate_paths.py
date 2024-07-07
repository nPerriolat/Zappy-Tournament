from ai.src.mvt.path import Path


class TestCalculatePaths:

    #  correctly calculates westward and eastward distances when end is to the right of start
    def test_calculates_westward_eastward_right(self):
        limit = [10, 10]
        start = [2, 2]
        end = [5, 2]
        path = Path(limit, start, end)
        result = path.calculate_paths()
        assert result == (True, False, 10, 7, 0, 3)

    #  correctly calculates westward and eastward distances when end is to the left of start
    def test_calculates_westward_eastward_left(self):
        limit = [10, 10]
        start = [5, 2]
        end = [2, 2]
        path = Path(limit, start, end)
        result = path.calculate_paths()
        assert result == (False, False, 10, 3, 0, 7)

    #  correctly calculates northward and southward distances when end is above start
    def test_calculates_northward_southward_above(self):
        limit = [10, 10]
        start = [2, 2]
        end = [2, 5]
        path = Path(limit, start, end)
        result = path.calculate_paths()
        assert result == (True, True, 3, 10, 7, 0)

    #  handles case when start and end points are the same
    def test_start_end_same(self):
        limit = [10, 10]
        start = [2, 2]
        end = [2, 2]
        path = Path(limit, start, end)
        result = path.calculate_paths()
        assert result == (True, False, 10, 10, 0, 0)

    #  handles case when start or end points are at the boundary limits
    def test_start_end_boundary_limits(self):
        limit = [10, 10]
        start = [0, 0]
        end = [9, 9]
        path = Path(limit, start, end)
        result = path.calculate_paths()
        assert result == (False, False, 9, 1, 1, 9)

    #  handles case when start and end points are diagonally opposite
    def test_start_end_diagonally_opposite(self):
        limit = [10, 10]
        start = [0, 0]
        end = [9, 9]
        path = Path(limit, start, end)
        result = path.calculate_paths()
        assert result == (False, False, 9, 1, 1, 9)
