import pytest
from src.Algorithms.PathFinding import calculate_shortest_path, LocomotionDirection, LocomotionAction, Position

def test_calculate_shortest_path():
    start = Position(0, 0)
    dest = Position(3, 4)
    max_x = 5
    max_y = 5
    current_direction = LocomotionDirection.UP

    expected_actions = [
        LocomotionAction.TURN_LEFT,
        LocomotionAction.TURN_LEFT,
        LocomotionAction.FORWARD,
        LocomotionAction.TURN_LEFT,
        LocomotionAction.FORWARD,
        LocomotionAction.FORWARD,
    ]

    actions = calculate_shortest_path(current_direction, start, dest, max_x, max_y)

    assert actions == expected_actions

def test_calculate_shortest_path_same_position():
    start = Position(2, 2)
    dest = Position(2, 2)
    max_x = 5
    max_y = 5
    current_direction = LocomotionDirection.RIGHT
    expected_actions = []
    actions = calculate_shortest_path(current_direction, start, dest, max_x, max_y)
    assert actions == expected_actions

# def test_calculate_shortest_path_diagonal_movement():
#     start = Position(0, 0)
#     dest = Position(3, 3)
#     max_x = 5
#     max_y = 5
#     current_direction = LocomotionDirection.UP
#     expected_actions = [
#         LocomotionAction.FORWARD,
#         LocomotionAction.TURN_RIGHT,
#         LocomotionAction.FORWARD,
#         LocomotionAction.TURN_RIGHT,
#         LocomotionAction.FORWARD,
#     ]
#     actions = calculate_shortest_path(current_direction, start, dest, max_x, max_y)
#     assert actions == expected_actions

def test_calculate_shortest_path_reaching_boundary_reverse():
    start = Position(0, 0)
    dest = Position(4, 0)
    max_x = 5
    max_y = 5
    current_direction = LocomotionDirection.RIGHT
    expected_actions = [
        LocomotionAction.TURN_LEFT,
        LocomotionAction.TURN_LEFT,
        LocomotionAction.FORWARD,
    ]
    actions = calculate_shortest_path(current_direction, start, dest, max_x, max_y)
    assert actions == expected_actions

def test_calculate_shortest_path_forward():
    start = Position(0, 0)
    dest = Position(4, 0)
    max_x = 10
    max_y = 10
    current_direction = LocomotionDirection.RIGHT
    expected_actions = [
        LocomotionAction.FORWARD,
        LocomotionAction.FORWARD,
        LocomotionAction.FORWARD,
        LocomotionAction.FORWARD,
    ]
    actions = calculate_shortest_path(current_direction, start, dest, max_x, max_y)
    assert actions == expected_actions

if __name__ == '__main__':
    pytest.main()