import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.src.zappy_ai import display_help, Bot


class TestImport:

    def test_function_compiles(self):
        try:
            result = display_help()
            assert result is None, "Expected return value is None"
        except SyntaxError:
            pytest.fail("Syntax error occurred")

    def test_unexpected_parameters(self):
        with pytest.raises(TypeError):
            display_help(1, 2)

    def test_display_help_output(self, capsys):
        display_help()
        captured = capsys.readouterr()
        assert captured.out == "USAGE: ./zappy_ai.py -p port -n name -h machine\n"
