
resources = {'linemate': 0,
             'deraumere': 0,
             'sibur': 0,
             'mendiane': 0,
             'phiras': 0,
             'thystame': 0,
             'food': 0,
             'player': 0}


def look_resources(around: str, focus: list[str]) -> list[list[str]]:
    """
    Look for resources in the given `around` area based on the `focus` items.

    Parameters:
    - around: str, representing the area to search for resources.
    - focus: list[str], containing the items to focus on.

    Returns:
    - list[list[str]]: A list of lists containing the resources found in the `around` area based on the `focus` items.
    """
    if len(around) < 8:
        return []
    my_list = around[8:-2].split(',')
    world_resources = [tile.split() for tile in my_list]
    focus_resources = []
    for tile in world_resources:
        new_tile = []
        for items in tile:
            if items in focus:
                new_tile.append(items)
        focus_resources.append(new_tile)
    return focus_resources


def only_forward_resources(tiles: list[list[str]]) -> list[list[str]]:
    """
    Extracts only the forward resources from the given tiles.

    Parameters:
    - tiles: a list of lists containing strings representing resources

    Returns:
    - a list of lists containing only the forward resources
    """
    new_tiles: list[list[str]] = []
    if len(tiles) >= 4:
        new_tiles.append(tiles[0])
        new_tiles.append(tiles[2])
    if len(tiles) >= 9:
        new_tiles.append(tiles[6])
    if len(tiles) >= 16:
        new_tiles.append(tiles[12])
    if len(tiles) >= 25:
        new_tiles.append(tiles[20])
    if len(tiles) >= 36:
        new_tiles.append(tiles[30])
    if len(tiles) >= 49:
        new_tiles.append(tiles[42])
    if len(tiles) >= 64:
        new_tiles.append(tiles[56])
    if len(tiles) >= 81:
        new_tiles.append(tiles[72])
    return new_tiles
