import re


def extract_direction(message: str) -> int:
    match = re.search(r'\b\d+', message)
    return int(match.group())


def get_infos(text: list[str]) -> tuple | None:
    """
    Get information from the input text.

    Parameters:
    - text: a list of strings containing information.

    Returns:
    - A tuple of lists containing parsed information.
    """
    if (len(text) == 2 and text[1][0:1].isnumeric() and validate_uuid_pattern(text[1]) is True) or len(text) < 2:
        return None, None
    if len(text) == 2 and validate_id_pattern(text[1]):
        return None, re.match(r'^\[(\d+)\]$', text[1]).group(1)
    if len(text) > 2:
        return tuple(zip(*(infos.split(";") for infos in text[2].split('~'))))
    return tuple(zip(*(infos.split(";") for infos in text[1].split('~'))))


def validate_id_pattern(s) -> bool:
    """
    Validate if the input string matches the pattern '[number]'.

    :param s: Input string to be validated.
    :return: True if the input string matches the pattern, False otherwise.
    """
    return bool(re.match(r'^\[\d+\]$', s))


def validate_look_pattern(s) -> bool:
    """
    Check if the input string matches a specific pattern.

    Parameters:
    s (str): The input string to be validated.

    Returns:
    int: 1 if the string matches the pattern, 0 otherwise.
    """
    pattern = r'^\[ player.*\]$'
    return True if re.match(pattern, s) else False


def validate_encryption_pattern(s) -> bool:
    """
    Validate if the input string follows a specific encryption pattern.

    Args:
        s (str): The input string to be validated.

    Returns:
        int: 0 if the pattern is valid, 1 if not.
    """
    pattern = r'^(?:\d+#){9}\d+(?:#(?:\d+#){9}\d+)*$'
    return False if re.fullmatch(pattern, s) else True


def validate_inventory_pattern(s) -> bool:
    """
    Validate if the input string matches a specific inventory pattern.

    Args:
        s (str): The input string to be validated.

    Returns:
        int: 1 if the input string matches the pattern, 0 otherwise.
    """
    pattern = r'^\[\s*food\s+\d+,\s+linemate\s+\d+,\s+deraumere\s+\d+,\s+sibur\s+\d+,\s+mendiane\s+\d+,\s+phiras\s+\d+,\s+thystame\s+\d+\s*\]$'
    return True if re.fullmatch(pattern, s) else False


def validate_number_pattern(s) -> bool:
    """
    Validate if the input string `s` consists only of digits.

    :param s: input string to be validated
    :return: True if `s` consists only of digits, False otherwise
    """
    return bool(re.match(r'^\d+$', s))


def validate_elevation(s) -> bool:
    """
    Validate if the input string represents a valid elevation level.

    :param s: Input string to be validated.
    :return: True if the input string represents a valid elevation level, False otherwise.
    """
    if s == 'Elevation underway' or re.fullmatch(r'^Current level: (\d+)$', s):
        return True
    return False


def validate_eject_pattern(s) -> bool:
    """

    :param s:
    :return:
    """
    return bool(re.fullmatch(r'eject: [7135]', s))


def validate_uuid_pattern(s) -> bool:
    """

    :param s:
    :return:
    """
    return bool(re.fullmatch(r'^([a-f0-9]{7})(;0~[a-f0-9]{7})*$', s))


def extract_inventory(s) -> dict:
    pattern = r'\[\s*food\s+(\d+),\s+linemate\s+(\d+),\s+deraumere\s+(\d+),\s+sibur\s+(\d+),\s+mendiane\s+(\d+),\s+phiras\s+(\d+),\s+thystame\s+(\d+)\s*\]'

    match = re.search(pattern, s)
    food, linemate, deraumere, sibur, mendiane, phiras, thystame = map(int, match.groups())
    return {
        'food': food,
        'linemate': linemate,
        'deraumere': deraumere,
        'sibur': sibur,
        'mendiane': mendiane,
        'phiras': phiras,
        'thystame': thystame
    }


def get_id_testudo(ids: list) -> int:
    id_concat = ''
    for single_id in ids:
        id_concat += single_id
    return int(id_concat)


def correction_overload_server(s: str, actions) -> bool:
    if s == 'ok':
        return True
    if s == 'ko':
        return True
    if s.startswith('['):
        return counter_of_delim(s)
    if s.startswith('message'):
        return counter_of_quotations_marks(s)
    # print(f'slot valide ? {validate_number_pattern(s)}')
    # print(f'is in {'Slots' in actions}')
    if validate_number_pattern(s) and 'Slots' in actions:
        return True
    if s.startswith('Elevation') or s.startswith('Current'):
        return validate_elevation(s)
    if s.startswith('eject'):
        return validate_eject_pattern(s)
    return False


def counter_of_quotations_marks(s) -> bool:
    if s.count('"') == 2:
        return True
    return False


def counter_of_delim(s) -> bool:
    if s.count('[') - s.count(']') == 0:
        return True
    return False
