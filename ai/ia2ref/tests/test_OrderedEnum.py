import pytest
from src.Utils.OrderedEnum import OrderedEnum

class TestOrderedEnum:
    def test_ordered_enum_comparison(self):
        class MyEnum(OrderedEnum):
            VALUE1 = 1
            VALUE2 = 2
            VALUE3 = 3

        assert MyEnum.VALUE1 < MyEnum.VALUE2
        assert MyEnum.VALUE2 > MyEnum.VALUE1
        assert MyEnum.VALUE1 <= MyEnum.VALUE2
        assert MyEnum.VALUE2 >= MyEnum.VALUE1
        assert MyEnum.VALUE1 != MyEnum.VALUE3
        assert MyEnum.VALUE3 == MyEnum.VALUE3

    def test_ordered_enum_not_implemented(self):
        class MyEnum(OrderedEnum):
            VALUE1 = 1
            VALUE2 = 2

        with pytest.raises(TypeError):
            MyEnum.VALUE1 < 42

        with pytest.raises(TypeError):
            MyEnum.VALUE2 > "abc"
