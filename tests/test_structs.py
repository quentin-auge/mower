import pytest

from mower.structs import Orientation, Position


def test_init_position():
    position = Position(-7, 8)
    assert position.cplx_position == complex(-7, 8)
    assert (position.x, position.y) == (-7, 8)


def test_str_position():
    assert str(Position(1, -2)) == '1 -2'


@pytest.mark.parametrize('orientation, expected', [
    pytest.param('N', complex(0, 1), id='valid_north'),
    pytest.param('S', complex(0, -1), id='valid_south'),
    pytest.param('W', complex(-1, 0), id='valid_west'),
    pytest.param('E', complex(1, 0), id='valid_east'),
    pytest.param('', ValueError('Invalid orientation'), id='invalid_empty'),
    pytest.param('X', ValueError('Invalid orientation'), id='invalid_non_existing')
])
def test_init_orientation(orientation, expected):
    if isinstance(expected, Exception):
        # Expect an exception
        with pytest.raises(type(expected), match=str(expected)):
            orientation_obj = Orientation(orientation)
            print(orientation_obj)
    else:
        # Expect a successful initialization with the right attribute
        orientation_obj = Orientation(orientation)
        assert orientation_obj.cplx_orientation == expected
        assert orientation_obj.orientation == orientation


@pytest.mark.parametrize('orientation', ['N', 'S', 'W', 'E'])
def test_str_orientation(orientation):
    assert str(Orientation(orientation)) == orientation
