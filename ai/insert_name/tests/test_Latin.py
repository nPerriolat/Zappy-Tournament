import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.src.communication.latin import Latin


class TestLatin:

    #  accessing a valid key in the verbum dictionary returns the correct Latin translation
    def test_access_valid_key_returns_correct_translation(self):
        latin = Latin()
        assert latin.verbum['point de ralliment'] == 'collectio militum : '

    #  adding a new key-value pair to the verbum dictionary works as expected
    def test_adding_new_key_value_pair(self):
        latin = Latin()
        latin.verbum['nouveau mot'] = 'novum verbum'
        assert latin.verbum['nouveau mot'] == 'novum verbum'

