import pytest

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from src.Map import Map, ResourceType, Tile, Position

@pytest.fixture
def map():
    return Map(10, 10, False)


def test_add_resource_to_map_x_axis_decrease(map):
    map.player_pos = Position(y=4, x=4)
    resources = [
        [ResourceType.FOOD], [ResourceType.LINEMATE], [ResourceType.DERAUMERE],
        [ResourceType.SIBUR], [ResourceType.MENDIANE, ResourceType.PLAYER], [ResourceType.PHIRAS],
        [ResourceType.THYSTAME], [ResourceType.PLAYER], [ResourceType.FOOD, ResourceType.FOOD]
    ]
    map._Map__add_resource_to_map(True, True, resources)
    assert map.map[4][4].types == [ResourceType.FOOD]
    assert map.map[5][3].types == [ResourceType.LINEMATE]
    assert map.map[4][3].types == [ResourceType.DERAUMERE]
    assert map.map[3][3].types == [ResourceType.SIBUR]
    assert map.map[6][2].types == [ResourceType.MENDIANE, ResourceType.PLAYER]
    assert map.map[5][2].types == [ResourceType.PHIRAS]
    assert map.map[4][2].types == [ResourceType.THYSTAME]
    assert map.map[3][2].types == [ResourceType.PLAYER]
    assert map.map[2][2].types == [ResourceType.FOOD, ResourceType.FOOD]
    assert map.map[1][2] is None

def test_add_resource_to_map_x_axis_increase_modulo(map):
    map.player_pos = Position(y=8, x=8)
    resources = [
        [ResourceType.FOOD], [ResourceType.LINEMATE], [ResourceType.DERAUMERE],
        [ResourceType.SIBUR], [ResourceType.MENDIANE, ResourceType.PLAYER], [ResourceType.PHIRAS],
        [ResourceType.THYSTAME], [ResourceType.PLAYER], [ResourceType.FOOD, ResourceType.FOOD]
    ]
    map._Map__add_resource_to_map(True, False, resources)
    assert map.map[(4 + 4) % 10][(4 + 4) % 10].types == [ResourceType.FOOD]
    assert map.map[(3 + 4) % 10][(5 + 4) % 10].types == [ResourceType.LINEMATE]
    assert map.map[(4 + 4) % 10][(5 + 4) % 10].types == [ResourceType.DERAUMERE]
    assert map.map[(5 + 4) % 10][(5 + 4) % 10].types == [ResourceType.SIBUR]
    assert map.map[(2 + 4) % 10][(6 + 4) % 10].types == [ResourceType.MENDIANE, ResourceType.PLAYER]
    assert map.map[(3 + 4) % 10][(6 + 4) % 10].types == [ResourceType.PHIRAS]
    assert map.map[(4 + 4) % 10][(6 + 4) % 10].types == [ResourceType.THYSTAME]
    assert map.map[(5 + 4) % 10][(6 + 4) % 10].types == [ResourceType.PLAYER]
    assert map.map[(6 + 4) % 10][(6 + 4) % 10].types == [ResourceType.FOOD, ResourceType.FOOD]
    assert map.map[(6 + 4) % 10][(7 + 4) % 10] is None

def test_add_resource_to_map_x_axis_increase(map):
    map.player_pos = Position(y=4, x=4)
    resources = [
        [ResourceType.FOOD], [ResourceType.LINEMATE], [ResourceType.DERAUMERE],
        [ResourceType.SIBUR], [ResourceType.MENDIANE, ResourceType.PLAYER], [ResourceType.PHIRAS],
        [ResourceType.THYSTAME], [ResourceType.PLAYER], [ResourceType.FOOD, ResourceType.FOOD]
    ]
    map._Map__add_resource_to_map(True, False, resources)
    assert map.map[4][4].types == [ResourceType.FOOD]
    assert map.map[3][5].types == [ResourceType.LINEMATE]
    assert map.map[4][5].types == [ResourceType.DERAUMERE]
    assert map.map[5][5].types == [ResourceType.SIBUR]
    assert map.map[2][6].types == [ResourceType.MENDIANE, ResourceType.PLAYER]
    assert map.map[3][6].types == [ResourceType.PHIRAS]
    assert map.map[4][6].types == [ResourceType.THYSTAME]
    assert map.map[5][6].types == [ResourceType.PLAYER]
    assert map.map[6][6].types == [ResourceType.FOOD, ResourceType.FOOD]
    assert map.map[6][7] is None

def test_add_resource_to_map_y_axis_increase(map):
    map.player_pos = Position(y=4, x=4)
    resources = [
        [ResourceType.FOOD], [ResourceType.LINEMATE], [ResourceType.DERAUMERE],
        [ResourceType.SIBUR], [ResourceType.MENDIANE, ResourceType.PLAYER], [ResourceType.PHIRAS],
        [ResourceType.THYSTAME], [ResourceType.PLAYER], [ResourceType.FOOD, ResourceType.FOOD]
    ]
    map._Map__add_resource_to_map(False, False, resources)
    assert map.map[4][4].types == [ResourceType.FOOD]
    assert map.map[5][3].types == [ResourceType.SIBUR]
    assert map.map[5][4].types == [ResourceType.DERAUMERE]
    assert map.map[5][5].types == [ResourceType.LINEMATE]
    assert map.map[6][2].types == [ResourceType.FOOD, ResourceType.FOOD]
    assert map.map[6][3].types == [ResourceType.PLAYER]
    assert map.map[6][4].types == [ResourceType.THYSTAME]
    assert map.map[6][5].types == [ResourceType.PHIRAS]
    assert map.map[6][6].types == [ResourceType.MENDIANE, ResourceType.PLAYER]
    assert map.map[6][7] is None

def test_add_resource_to_map_y_axis_decrease(map):
    map.player_pos = Position(y=4, x=4)
    resources = [
        [ResourceType.FOOD], [ResourceType.LINEMATE], [ResourceType.DERAUMERE],
        [ResourceType.SIBUR], [ResourceType.MENDIANE, ResourceType.PLAYER], [ResourceType.PHIRAS],
        [ResourceType.THYSTAME], [ResourceType.PLAYER], [ResourceType.FOOD, ResourceType.FOOD]
    ]
    map._Map__add_resource_to_map(False, True, resources)
    assert map.map[4][4].types == [ResourceType.FOOD]
    assert map.map[3][3].types == [ResourceType.LINEMATE]
    assert map.map[3][4].types == [ResourceType.DERAUMERE]
    assert map.map[3][5].types == [ResourceType.SIBUR]
    assert map.map[2][2].types == [ResourceType.MENDIANE, ResourceType.PLAYER]
    assert map.map[2][3].types == [ResourceType.PHIRAS]
    assert map.map[2][4].types == [ResourceType.THYSTAME]
    assert map.map[2][5].types == [ResourceType.PLAYER]
    assert map.map[2][6].types == [ResourceType.FOOD, ResourceType.FOOD]
    assert map.map[2][7] is None

# TODO : tests on overlapping vision. Make sure they don't unececessarily overwrite the map
def test_add_resource_to_map_empty_resources(map):
    map.player_pos = Position(y=4, x=4)
    resources = []
    map._Map__add_resource_to_map(True, True, resources)
    assert map.map[4][4] is None
    assert map.map[5][3] is None
    assert map.map[4][3] is None
    assert map.map[3][3] is None
    assert map.map[6][2] is None
    assert map.map[5][2] is None
    assert map.map[4][2] is None
    assert map.map[3][2] is None
    assert map.map[2][2] is None
    assert map.map[1][2] is None
    assert map.map[(4 + 4) % 10][(4 + 4) % 10] is None
    assert map.map[(3 + 4) % 10][(5 + 4) % 10] is None
    assert map.map[(4 + 4) % 10][(5 + 4) % 10] is None
    assert map.map[(5 + 4) % 10][(5 + 4) % 10] is None
    assert map.map[(2 + 4) % 10][(6 + 4) % 10] is None
    assert map.map[(3 + 4) % 10][(6 + 4) % 10] is None
    assert map.map[(4 + 4) % 10][(6 + 4) % 10] is None
    assert map.map[(5 + 4) % 10][(6 + 4) % 10] is None
    assert map.map[(6 + 4) % 10][(6 + 4) % 10] is None
    assert map.map[(6 + 4) % 10][(7 + 4) % 10] is None
    assert map.map[4][4] is None
    assert map.map[3][5] is None
    assert map.map[4][5] is None
    assert map.map[5][5] is None
    assert map.map[2][6] is None
    assert map.map[3][6] is None
    assert map.map[4][6] is None
    assert map.map[5][6] is None
    assert map.map[6][6] is None
    assert map.map[6][7] is None
    assert map.map[4][4] is None
    assert map.map[5][3] is None
    assert map.map[5][4] is None
    assert map.map[5][5] is None
    assert map.map[6][2] is None
    assert map.map[6][3] is None
    assert map.map[6][4] is None
    assert map.map[6][5] is None
    assert map.map[6][6] is None
    assert map.map[6][7] is None
    assert map.map[4][4] is None
    assert map.map[3][3] is None
    assert map.map[3][4] is None
    assert map.map[3][5] is None
    assert map.map[2][2] is None
    assert map.map[2][3] is None
    assert map.map[2][4] is None
    assert map.map[2][5] is None
    assert map.map[2][6] is None
    assert map.map[2][7] is None