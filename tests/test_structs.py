import mock
import pytest

from mower.structs import Mower, Orientation, Position


def test_init_position():
    position = Position(-7, 8)
    assert position.cplx_position == complex(-7, 8)
    assert (position.x, position.y) == (-7, 8)


def test_str_position():
    assert str(Position(1, -2)) == '1 -2'


@pytest.mark.parametrize('orientation, dst_position', [
    pytest.param('N', (1, 3), id='N'),
    pytest.param('S', (1, 1), id='S'),
    pytest.param('W', (0, 2), id='W'),
    pytest.param('E', (2, 2), id='E')
])
def test_forward_position(orientation, dst_position):
    position = Position(1, 2)
    orientation = Orientation(orientation)

    with mock.patch.object(position, 'restrict_to_grid') as restrict_to_grid:
        position.forward(orientation, grid_size=(100, 100))
        restrict_to_grid.assert_called_once()

    assert (position.x, position.y) == dst_position


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


@pytest.mark.parametrize('src_orientation, rotate_method, dst_orientation', [
    pytest.param('N', 'rotate_left', 'W', id='rotate_left_N'),
    pytest.param('S', 'rotate_left', 'E', id='rotate_left_S'),
    pytest.param('W', 'rotate_left', 'S', id='rotate_left_W'),
    pytest.param('E', 'rotate_left', 'N', id='rotate_left_E'),
    pytest.param('N', 'rotate_right', 'E', id='rotate_right_N'),
    pytest.param('S', 'rotate_right', 'W', id='rotate_right_S'),
    pytest.param('W', 'rotate_right', 'N', id='rotate_right_W'),
    pytest.param('E', 'rotate_right', 'S', id='rotate_right_E'),
])
def test_rotate_orientation(src_orientation, rotate_method, dst_orientation):
    orientation = Orientation(src_orientation)

    # Check base orientation
    assert orientation.orientation == src_orientation

    # Rotate left or right
    rotate_method = getattr(orientation, rotate_method)
    rotate_method()

    # Check orientation after rotation
    assert orientation.orientation == dst_orientation


def test_mower_initialization():
    position = Position(8, 9)

    with mock.patch.object(position, 'restrict_to_grid') as restrict_to_grid:
        mower = Mower(position, Orientation('W'), grid_size=(10, 10))
        restrict_to_grid.assert_called_once()

    assert (mower.x, mower.y) == (8, 9)
    assert mower.orientation == 'W'


def test_str_mower():
    mower = Mower(Position(8, 9), Orientation('W'), grid_size=(10, 10))
    assert str(mower) == '8 9 W'


@pytest.mark.parametrize('src_position, grid_size, dst_position', [
    pytest.param((0, 0), (10, 5), (0, 0), id='valid_bottom_left_corner'),
    pytest.param((0, 4), (10, 5), (0, 4), id='valid_top_left_corner'),
    pytest.param((9, 4), (10, 5), (9, 4), id='valid_top_right_corner'),
    pytest.param((9, 0), (10, 5), (9, 0), id='valid_bottom_right_corner'),
    pytest.param((0, -1), (10, 5), (0, 0), id='invalid_bottom'),
    pytest.param((-1, 4), (10, 5), (0, 4), id='invalid_left'),
    pytest.param((9, 5), (10, 5), (9, 4), id='invalid_top'),
    pytest.param((10, 0), (10, 5), (9, 0), id='invalid_right')
])
def test_restrict_position_to_grid(src_position, grid_size, dst_position):
    position = Position(*src_position)
    position.restrict_to_grid(grid_size)
    assert (position.x, position.y) == dst_position
