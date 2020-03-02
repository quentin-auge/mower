import pytest

from mower.parser import Parser


def expect_value_or_exception(method, *args, expected):
    """
    Run a given method of class :class:`Parser` with some args.
    Expect either a value or an exception.
    """

    run_method = lambda: getattr(Parser(None), method)(*args)

    if isinstance(expected, Exception):
        # Expect an exception
        with pytest.raises(type(expected), match=str(expected)):
            run_method()
    else:
        # Expect a value
        assert run_method()


@pytest.mark.parametrize('x, y, expected', [
    pytest.param('-15', '22', complex(-15, 22), id='valid'),
    pytest.param('9', '', ValueError('Invalid position'), id='invalid_empty_string'),
    pytest.param('19b', '3', ValueError('Invalid position'), id='invalid_string'),
    pytest.param('1.4', '3', ValueError('Invalid position'), id='invalid_float')
])
def test_parse_position(x, y, expected):
    expect_value_or_exception('_parse_position', x, y, expected=expected)


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


@pytest.mark.parametrize('line, expected', [
    pytest.param('-15 22', complex(-15, 22), id='valid'),
    pytest.param('1', ValueError('Invalid grid size'), id='invalid_single_value'),
    pytest.param('1 2 3', ValueError('Invalid grid size'), id='invalid_three_values')
])
def test_parse_grid_size_line(line, expected):
    expect_value_or_exception('_parse_grid_size_line', line, expected=expected)


@pytest.mark.parametrize('line, expected', [
    pytest.param('-15 22 W', complex(-15, 22), id='valid'),
    pytest.param('1', ValueError('Invalid initial position'), id='invalid_two_values'),
    pytest.param('1 2 W 0', ValueError('Invalid initial position'), id='invalid_four_values')
])
def test_parse_initial_position_line(line, expected):
    expect_value_or_exception('_parse_initial_position_line', line, expected=expected)
