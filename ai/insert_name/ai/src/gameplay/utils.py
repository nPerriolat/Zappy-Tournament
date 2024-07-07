

def is_all_val0(arg_dict, not_contains=None):
    """
    Check if all values in the dictionary are 0, excluding those specified in `not_contains`.

    :param arg_dict: Dictionary to check values.
    :param not_contains: List of values to exclude from the check.
    :return: True if all values are 0 or in `not_contains`, False otherwise.
    """
    if not_contains is None:
        not_contains = []
    values = arg_dict.values()
    for val in values:
        if val != 0 and val not in not_contains:
            return False
    return True

