import pytest

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.Utils.CircularArray import CircularArray

@pytest.fixture
def circular_array():
    array = [1, 2, 3, 4, 5]
    return CircularArray(array, len(array))

def test_set_index(circular_array):
    circular_array.set_index(2)
    assert circular_array.get_current() == 3

def test_insert_element_at_index(circular_array):
    circular_array.set_index(2)
    circular_array.insert_element(6)
    assert circular_array.size == 6
    assert circular_array.get_current() == 6

def test_remove_element_at_index(circular_array):
    circular_array.set_index(2)
    circular_array.remove_current_element()
    assert circular_array.size == 4
    assert circular_array.get_current() == 4

def test_advance_multiple_times(circular_array):
    circular_array.advance()
    circular_array.advance()
    assert circular_array.get_current() == 3
