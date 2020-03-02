from mower.mower import Mower
from mower.structs import Orientation, Position


def test_mower_initialization():
    mower = Mower(Position(1, 2), Orientation('W'))
    assert mower.x == 1
    assert mower.y == 2
    assert mower.orientation == 'W'


def test_str_mower():
    mower = Mower(Position(1, 2), Orientation('W'))
    assert str(mower) == '1 2 W'
