import pytest

from mower.structs import Orientation, Position


def expect_value_or_exception(cls, *args, expected):
    """
    Initialize a given struct of module :module:`mower.structs` with some args.
    Expect either a successful initialization or an exception.
    """

    init_object = lambda: cls(*args)

    if isinstance(expected, Exception):
        # Expect an exception
        with pytest.raises(type(expected), match=str(expected)):
            init_object()
    else:
        # Expect a successful initialization
        assert isinstance(init_object(), expected)


@pytest.mark.parametrize('x, y, expected', [
    pytest.param(-7, 8, complex(-7, 8), id='valid_int'),
    pytest.param('-15', '22', complex(-15, 22), id='valid_string'),
    pytest.param('-22', 15, complex(-22, 15), id='valid_mixed_int_string'),
    pytest.param(9, '', ValueError('Invalid position'), id='invalid_empty_string'),
    pytest.param('19b', 3, ValueError('Invalid position'), id='invalid_string'),
    pytest.param('1.4', '3', ValueError('Invalid position'), id='invalid_float')
])
def test_init_position(x, y, expected):
    if isinstance(expected, Exception):
        # Expect an exception
        with pytest.raises(type(expected), match=str(expected)):
            position = Position(x, y)
            print(position)
    else:
        # Expect a successful initialization with the right attributes
        position = Position(x, y)
        assert position._position == expected
        assert complex(position.x, position.y) == expected


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
        assert orientation_obj._orientation == expected
        assert orientation_obj.orientation == orientation


@pytest.mark.parametrize('orientation', ['N', 'S', 'W', 'E'])
def test_str_orientation(orientation):
    assert str(Orientation(orientation)) == orientation
