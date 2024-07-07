from ai.src.utils.info_look import only_forward_resources


class TestOnlyForwardResources:

    #  returns correct sublist when input list has 4 elements
    def test_returns_correct_sublist_for_4_elements(self):
        tiles = [["1"], ["2"], ["3"], ["4"]]
        result = only_forward_resources(tiles)
        assert result == [["1"], ["3"]]

    #  returns correct sublist when input list has 9 elements
    def test_returns_correct_sublist_for_9_elements(self):
        tiles = [["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"]]
        result = only_forward_resources(tiles)
        assert result == [["1"], ["3"], ["7"]]

    #  returns correct sublist when input list has 16 elements
    def test_returns_correct_sublist_for_16_elements(self):
        tiles = [["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"], ["10"], ["11"], ["12"], ["13"], ["14"], ["15"], ["16"]]
        result = only_forward_resources(tiles)
        assert result == [["1"], ["3"], ["7"], ["13"]]

    #  returns empty list when input list is empty
    def test_returns_empty_list_for_empty_input(self):
        tiles = []
        result = only_forward_resources(tiles)
        assert result == []

    #  returns empty list when input list has less than 4 elements
    def test_returns_empty_list_for_less_than_4_elements(self):
        tiles = [["1"], ["2"], ["3"]]
        result = only_forward_resources(tiles)
        assert result == []

    #  handles lists with non-string elements gracefully
    def test_handles_non_string_elements_gracefully(self):
        tiles = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
        result = only_forward_resources(tiles)
        assert result == [[1], [3], [7]]
