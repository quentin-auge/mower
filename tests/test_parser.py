import io
import pytest

from mower import parser
from mower.mower import Mower


def expect_value_or_exception(func, *args, expected):
    """
    Run a given function of module :module:`parser` with some args.
    Expect either a value or an exception.
    """

    run_func = lambda: getattr(parser, func)(*args)

    if isinstance(expected, Exception):
        # Expect an exception
        with pytest.raises(type(expected), match=str(expected)):
            print(run_func())
    else:
        # Expect a value
        assert run_func() == expected


@pytest.mark.parametrize('x, y, expected', [
    pytest.param('-15', '22', (-15, 22), id='valid'),
    pytest.param('9', '', ValueError('Invalid position'), id='invalid_empty_string'),
    pytest.param('19b', '3', ValueError('Invalid position'), id='invalid_string'),
    pytest.param('1.4', '3', ValueError('Invalid position'), id='invalid_float')
])
def test_parse_two_points(x, y, expected):
    expect_value_or_exception('_parse_two_points', x, y, expected=expected)


@pytest.mark.parametrize('token, expected', [
    pytest.param('L', 'L', id='valid_left'),
    pytest.param('R', 'R', id='valid_right'),
    pytest.param('F', 'F', id='valid_forward'),
    pytest.param('X', ValueError('Invalid move'), id='invalid_one_char')
])
def test_parse_move(token, expected):
    expect_value_or_exception('_parse_move', token, expected=expected)


@pytest.mark.parametrize('line, expected', [
    pytest.param('-15 22', (-15, 22), id='valid'),
    pytest.param('1', ValueError('Invalid grid size'), id='invalid_single_value'),
    pytest.param('1 2 3', ValueError('Invalid grid size'), id='invalid_three_values')
])
def test_parse_grid_size_line(line, expected):
    expect_value_or_exception('_parse_grid_size_line', line, expected=expected)


def assert_mower_position_and_orientation(mower, expected_attributes):
    return (mower.x, mower.y, mower.orientation) == expected_attributes


@pytest.mark.parametrize('line, expected', [
    pytest.param('-15 22 W', (-15, 22, 'W'), id='valid'),
    pytest.param('1', ValueError('Invalid initial position or orientation'),
                 id='invalid_two_values'),
    pytest.param('1 2 W 0', ValueError('Invalid initial position or orientation'),
                 id='invalid_four_values')
])
def test_parse_mower_line(line, expected):
    if isinstance(expected, Exception):
        # Expect an exception
        with pytest.raises(type(expected), match=str(expected)):
            print(parser._parse_mower_line(line))
    else:
        # Expect a value
        mower = parser._parse_mower_line(line)
        assert_mower_position_and_orientation(mower, expected)


@pytest.mark.parametrize('line, expected', [
    pytest.param(r'', '', id='valid_empty_string'),
    pytest.param('L', 'L', id='valid_one_char'),
    pytest.param('RFLLRF', 'RFLLRF', id='valid_multiple_chars'),
    pytest.param('RFLXLRF', ValueError('Invalid move'), id='invalid_move')
])
def test_parse_moves_line(line, expected):
    expect_value_or_exception('_parse_moves_line', line, expected=expected)


@pytest.mark.parametrize('under_test', ['grid_size', 'mower', 'moves'])
def test_parse_two_mowers(under_test):
    sample_input = '''5 6
    1 2 N
    LFLFLFLFF
    3 3 E
    FFRFFRFRRF
    '''

    stream = io.StringIO(sample_input)

    # Test grid size
    if under_test == 'grid_size':
        assert parser.parse_grid_size(stream) == (5, 6)
    else:
        # Skip line
        stream.readline()

    # Test first mower initial position and orientation
    if under_test == 'mower':
        mower = parser.parse_mower(stream)
        assert isinstance(mower, Mower)
        assert_mower_position_and_orientation(mower, (1, 2, 'N'))
    else:
        # Skip line
        stream.readline()

    # Test first mower moves
    if under_test == 'moves':
        assert parser.parse_moves(stream) == 'LFLFLFLFF'
    else:
        # Skip line
        stream.readline()

    # Test second mower initial position and orientation
    if under_test == 'mower':
        mower = parser.parse_mower(stream)
        assert isinstance(mower, Mower)
        assert_mower_position_and_orientation(mower, (3, 3, 'E'))
    else:
        # Skip line
        stream.readline()

    # Test second mower moves
    if under_test == 'moves':
        assert parser.parse_moves(stream) == 'FFRFFRFRRF'
    else:
        # Skip line
        stream.readline()

    # Test no mower is left
    if under_test == 'mower':
        mower = parser.parse_mower(stream)
        assert mower is None
    else:
        # Skip line
        stream.readline()

    # Test no moves are left
    if under_test == 'moves':
        moves = parser.parse_moves(stream)
        assert moves == ''
    else:
        # Skip line
        stream.readline()


@pytest.mark.parametrize('under_test', ['grid_size', 'mower', 'moves'])
def test_parse_no_mower(under_test):
    sample_input = '''5 6
    '''

    stream = io.StringIO(sample_input)

    # Test grid size
    if under_test == 'grid_size':
        assert parser.parse_grid_size(stream) == (5, 6)
    else:
        # Skip line
        stream.readline()

    # Test no mower is left
    if under_test == 'mower':
        mower = parser.parse_mower(stream)
        assert mower is None
    else:
        # Skip line
        stream.readline()

    # Test no moves are left
    if under_test == 'moves':
        moves = parser.parse_moves(stream)
        assert moves == ''
    else:
        # Skip line
        stream.readline()


@pytest.mark.parametrize('under_test', ['grid_size', 'mower', 'moves'])
def test_parse_on_mower_without_moves(under_test):
    sample_input = '''5 6
    1 2 N
    '''

    stream = io.StringIO(sample_input)

    # Test grid size
    if under_test == 'grid_size':
        assert parser.parse_grid_size(stream) == (5, 6)
    else:
        # Skip line
        stream.readline()

    # Test first mower initial position and orientation
    if under_test == 'mower':
        mower = parser.parse_mower(stream)
        assert isinstance(mower, Mower)
        assert_mower_position_and_orientation(mower, (1, 2, 'N'))
    else:
        # Skip line
        stream.readline()

    # Test no mower is left
    if under_test == 'mower':
        mower = parser.parse_mower(stream)
        assert mower is None
    else:
        # Skip line
        stream.readline()

    # Test no moves are left
    if under_test == 'moves':
        moves = parser.parse_moves(stream)
        assert moves == ''
    else:
        # Skip line
        stream.readline()
