from ai.src.utils.info_look import look_resources


class TestLookResources:

    #  correctly extracts and splits resources from the input string
    def test_correctly_extracts_and_splits_resources(self):
        around = "[ player wood stone, iron gold, water ]"
        focus = ["wood", "stone", "iron", "gold", "water"]
        expected = [["wood", "stone"], ["iron", "gold"], ["water"]]
        result = look_resources(around, focus)
        assert result == expected, f'is {result} must be {expected}'

    #  filters resources based on the focus list
    def test_filters_resources_based_on_focus_list(self):
        around = "[ player wood stone,iron gold,water ]"
        focus = ["wood", "gold"]
        expected = [["wood"], ["gold"], []]
        assert look_resources(around, focus) == expected

    #  handles multiple resources in a single tile correctly
    def test_handles_multiple_resources_in_single_tile(self):
        around = "[ player wood stone iron,water gold ]"
        focus = ["wood", "stone", "iron", "gold"]
        expected = [["wood", "stone", "iron"], ["gold"]]
        assert look_resources(around, focus) == expected

    #  returns an empty list if the input string is shorter than 8 characters
    def test_returns_empty_list_if_input_string_shorter_than_8(self):
        around = "1234567"
        focus = ["wood", "stone"]
        expected = []
        assert look_resources(around, focus) == expected

    #  handles input strings with no commas correctly
    def test_handles_input_strings_with_no_commas_correctly(self):
        around = "[ player wood stone iron gold ]"
        focus = ["wood", "stone", "iron", "gold"]
        expected = [["wood", "stone", "iron", "gold"]]
        assert look_resources(around, focus) == expected

    #  processes input strings with no matching resources in the focus list
    def test_processes_input_strings_with_no_matching_resources(self):
        around = "[ player wood stone,iron gold,water ]"
        focus = ["diamond", "silver"]
        expected = [[], [], []]
        assert look_resources(around, focus) == expected
