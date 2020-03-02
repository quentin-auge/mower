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


@pytest.mark.parametrize('line, expected', [
    pytest.param('-15 22', complex(-15, 22), id='valid'),
    pytest.param('1', ValueError('Invalid grid size'), id='invalid_single_value'),
    pytest.param('1 2 3', ValueError('Invalid grid size'), id='invalid_three_values')
])
def test_parse_grid_size_line(line, expected):
    expect_value_or_exception('_parse_grid_size_line', line, expected=expected)

