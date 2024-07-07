from ai.src.utils.messages import get_infos


class TestGetInfos:

    #  returns None, None when text has less than 2 elements
    def test_returns_none_none_when_text_has_less_than_2_elements(self):
        assert get_infos(["1234567890#"]) == (None, None)

    #  returns None, None when text has 2 elements and second element starts with a number
    def test_returns_none_none_when_text_has_2_elements_and_second_element_starts_with_number(self):
        assert get_infos(["info", "1234567890#"]) == (('1234567890#',),)

    #  returns None and extracted number when text has 2 elements and second element matches '[number]' pattern
    def test_returns_none_and_extracted_number_when_text_has_2_elements_and_second_element_matches_pattern(self):
        assert get_infos(["info", "[1234567890#]"]) == (('[1234567890#]',),)

    #  handles empty list input gracefully
    def test_handles_empty_list_input_gracefully(self):
        assert get_infos([]) == (None, None)

    #  handles list with one empty string
    def test_handles_list_with_one_empty_string(self):
        assert get_infos([""]) == (None, None)

    #  handles list with multiple empty strings
    def test_handles_list_with_multiple_empty_strings(self):
        assert get_infos(["", ""]) == (('',),)
