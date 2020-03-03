import io

import pytest

import mower.parser


def expect_value_or_exception(func, *args, expected):
    """
    Run a given function of module :module:`mower.parser` with some args.
    Expect either a value or an exception.
    """

    run_func = lambda: getattr(mower.parser, func)(*args)

    if isinstance(expected, Exception):
        # Expect an exception
        with pytest.raises(type(expected), match=str(expected)):
            run_func()
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
    pytest.param('N', complex(0, 1), id='valid_north'),
    pytest.param('S', complex(0, -1), id='valid_south'),
    pytest.param('W', complex(-1, 0), id='valid_west'),
    pytest.param('E', complex(1, 0), id='valid_east'),
    pytest.param('', ValueError('Invalid orientation'), id='invalid_empty_string'),
    pytest.param('X', ValueError('Invalid orientation'), id='invalid_one_char'),
    pytest.param('NS', ValueError('Invalid orientation'), id='invalid_multiple_chars')
])
def test_parse_orientation(token, expected):
    expect_value_or_exception('_parse_orientation', token, expected=expected)


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


@pytest.mark.parametrize('line, expected', [
    pytest.param('-15 22 W', (complex(-15, 22), complex(-1, 0)), id='valid'),
    pytest.param('1', ValueError('Invalid initial position'), id='invalid_two_values'),
    pytest.param('1 2 W 0', ValueError('Invalid initial position'), id='invalid_four_values')
])
def test_parse_initial_position_line(line, expected):
    expect_value_or_exception('_parse_initial_position_line', line, expected=expected)


@pytest.mark.parametrize('line, expected', [
    pytest.param(r'', '', id='valid_empty_string'),
    pytest.param('L', 'L', id='valid_one_char'),
    pytest.param('RFLLRF', 'RFLLRF', id='valid_multiple_chars'),
    pytest.param('RFLXLRF', ValueError('Invalid move'), id='invalid_move')
])
def test_parse_moves_line(line, expected):
    expect_value_or_exception('_parse_moves_line', line, expected=expected)


def test_parse_grid_size_from_stream():
    sample_input = '''5 6
    1 2 N
    LFLFLFLFF
    '''
    stream = io.StringIO(sample_input)
    assert mower.parser.parse_grid_size(stream) == (5, 6)


def test_parse_zero_mower_from_stream():
    stream = io.StringIO()

    actual_mowers = mower.parser.parse_mowers(stream)
    expected_mowers = []

    assert actual_mowers == expected_mowers


def test_parse_all_mower_from_stream():
    sample_input = '''1 2 N
    LFLFLFLFF
    3 3 E
    FFRFFRFRRF
    '''

    stream = io.StringIO(sample_input)

    actual_mowers = mower.parser.parse_mowers(stream)
    expected_mowers = [
        (complex(1, 2), complex(0, 1), 'LFLFLFLFF'),
        (complex(3, 3), complex(1, 0), 'FFRFFRFRRF')
    ]

    assert actual_mowers == expected_mowers


def test_parse_one_mower_from_stream():
    sample_input = '''1 2 N
    LFLFLFLFF
    '''

    stream = io.StringIO(sample_input)

    actual_mowers = mower.parser.parse_mowers(stream)
    expected_mowers = [
        (complex(1, 2), complex(0, 1), 'LFLFLFLFF')
    ]

    assert actual_mowers == expected_mowers


def test_parse_incomplete_mower_from_stream():
    sample_input = '''1 2 N
    LFLFLFLFF
    3 3 E
    '''

    stream = io.StringIO(sample_input)

    actual_mowers = mower.parser.parse_mowers(stream)
    expected_mowers = [
        (complex(1, 2), complex(0, 1), 'LFLFLFLFF'),
        (complex(3, 3), complex(1, 0), '')
    ]

    assert actual_mowers == expected_mowers
