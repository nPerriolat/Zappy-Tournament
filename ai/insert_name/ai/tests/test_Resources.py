from ai.src.gameplay.enum_gameplay import Resources


class TestResources:

    #  Enum members can be accessed by name
    def test_enum_members_access_by_name(self):
        assert Resources.NONE.name == 'NONE'
        assert Resources.LINEMATE.name == 'LINEMATE'
        assert Resources.DERAUMERE.name == 'DERAUMERE'
        assert Resources.SIBUR.name == 'SIBUR'
        assert Resources.MENDIANE.name == 'MENDIANE'
        assert Resources.PHIRAS.name == 'PHIRAS'
        assert Resources.THYSTAME.name == 'THYSTAME'
        assert Resources.FOOD.name == 'FOOD'
        assert Resources.PLAYER.name == 'PLAYER'

    #  Enum members can be accessed by value
    def test_enum_members_access_by_value(self):
        assert Resources(0) == Resources.NONE
        assert Resources(1) == Resources.LINEMATE
        assert Resources(2) == Resources.DERAUMERE
        assert Resources(3) == Resources.SIBUR
        assert Resources(4) == Resources.MENDIANE
        assert Resources(5) == Resources.PHIRAS
        assert Resources(6) == Resources.THYSTAME
        assert Resources(7) == Resources.FOOD
        assert Resources(8) == Resources.PLAYER

    #  Enum members have correct integer values
    def test_enum_members_correct_values(self):
        assert Resources.NONE.value == 0
        assert Resources.LINEMATE.value == 1
        assert Resources.DERAUMERE.value == 2
        assert Resources.SIBUR.value == 3
        assert Resources.MENDIANE.value == 4
        assert Resources.PHIRAS.value == 5
        assert Resources.THYSTAME.value == 6
        assert Resources.FOOD.value == 7
        assert Resources.PLAYER.value == 8
