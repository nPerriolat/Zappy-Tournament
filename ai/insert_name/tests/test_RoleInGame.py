import pytest

from ai.src.gameplay.enum_gameplay import RoleInGame


class TestRoleInGame:

    #  Enum members can be accessed by name
    def test_enum_members_access_by_name(self):
        assert RoleInGame.PROGENITOR.name == "PROGENITOR"
        assert RoleInGame.MASTERMIND.name == "MASTERMIND"

    #  Enum members can be accessed by value
    def test_enum_members_access_by_value(self):
        assert RoleInGame(0) == RoleInGame.PROGENITOR
        assert RoleInGame(1) == RoleInGame.INCANTATOR

    #  Enum members have correct names
    def test_enum_members_have_correct_names(self):
        assert RoleInGame.PROGENITOR.name == "PROGENITOR"
        assert RoleInGame.PUSHER.name == "PUSHER"

    #  Accessing an undefined enum member raises AttributeError
    def test_accessing_undefined_enum_member_raises_attribute_error(self):
        with pytest.raises(AttributeError):
            _ = RoleInGame.UNDEFINED

    #  Accessing an enum member with an invalid value raises ValueError
    def test_accessing_enum_member_with_invalid_value_raises_value_error(self):
        with pytest.raises(ValueError):
            _ = RoleInGame(99)

    #  Enum member names are case-sensitive
    def test_enum_member_names_are_case_sensitive(self):
        with pytest.raises(AttributeError):
            _ = RoleInGame.progenitor
