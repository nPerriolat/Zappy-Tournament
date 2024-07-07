from ai.src.gameplay.utils import is_all_val0


class TestIsAllVal0:

    #  returns True when all values in arg_dict are 0
    def test_all_values_zero(self):
        arg_dict = {'a': 0, 'b': 0, 'c': 0}
        assert is_all_val0(arg_dict) is True

    #  returns True when arg_dict is empty
    def test_empty_dict(self):
        arg_dict = {}
        assert is_all_val0(arg_dict) is True

    #  returns True when all non-zero values are in not_contains
    def test_non_zero_values_in_not_contains(self):
        arg_dict = {'a': 0, 'b': 1, 'c': 2}
        not_contains = [1, 2]
        assert is_all_val0(arg_dict, not_contains) is True

    #  returns True when arg_dict contains only one key-value pair with value 0
    def test_single_key_value_pair_zero(self):
        arg_dict = {'a': 0}
        assert is_all_val0(arg_dict) is True

    #  returns False when arg_dict contains only one key-value pair with non-zero value not in not_contains
    def test_single_key_value_pair_non_zero_not_in_not_contains(self):
        arg_dict = {'a': 1}
        assert is_all_val0(arg_dict) is False

    #  handles large dictionaries efficiently
    def test_large_dictionary(self):
        arg_dict = {f'key{i}': 0 for i in range(100000)}
        assert is_all_val0(arg_dict) is True
