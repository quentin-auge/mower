"""
Parse mower moves specification file:
  * grid size on first line (2 space-separated ints)
  * then, an alternance:
    * mower initial position (2 space-separated ints) and initial orientation (N/S/W/E char)
      line
    * mower moves (L/R/F chars) line

Handle parsing errors by raising :exception:`ValueError` with relevant error messages.
"""

import io
from typing import List, Tuple


def parse_grid_size(stream: io.TextIOBase) -> complex:
    """
    Consume first line of stream to get grid size (2 space-separated ints -> complex).

    Args:
        stream: input specification file stream.
    """
    line = _readline(stream)
    grid_size = _parse_grid_size_line(line)
    return grid_size


def parse_mowers(stream: io.TextIOBase) -> List[Tuple[complex, complex, str]]:
    """
    Consume remaining lines of stream to get mowers initial position (2 space-separated ints
    -> complex), initial orientation (N/S/W/E char -> complex) and moves (L/R/F chars).

    Args:
        stream: input specification file stream.
    """

    mowers = []

    line = _readline(stream)

    while line:
        position, orientation = _parse_initial_position_line(line)

        line = _readline(stream)
        moves = _parse_moves_line(line)

        mowers.append((position, orientation, moves))

        line = _readline(stream)

    return mowers


def _readline(stream) -> str:
    """
    Read new line from the stream.

    Args:
        stream: input specification file stream.
    """
    line = stream.readline().strip()
    return line


def _parse_grid_size_line(line) -> complex:
    """
    Parse and validate a grid size specification (2 space-separated ints) to a complex.
    """
    try:
        x, y = line.split(' ')
        grid_size = _parse_position(x, y)
    except ValueError:
        raise ValueError(f'Invalid grid size: "{line}"')

    return grid_size


def _parse_initial_position_line(line: str) -> Tuple[complex, complex]:
    """
    Parse and validate initial position (2 space-separated ints) and orientation (N/S/W/E char)
    to a complex position and complex orientation.
    """
    try:
        x, y, orientation = line.split(' ')
        position = _parse_position(x, y)
        orientation = _parse_orientation(orientation)
    except ValueError:
        raise ValueError(f'Invalid initial position: "{line}"')

    return position, orientation


def _parse_position(x: str, y: str) -> complex:
    """
    Parse and validate a position (two strings interepretable as ints) to a complex.
    """
    try:
        x, y = int(x), int(y)
    except ValueError:
        msg = f'Invalid position: "{(x, y)}", must be integers'
        raise ValueError(msg)

    return complex(x, y)


def _parse_orientation(token: str) -> complex:
    """
    Parse and validate an orientation (N/S/W/E char) to a complex.
    """

    orientation_mapping = {
        'W': complex(-1, 0),
        'E': complex(1, 0),
        'N': complex(0, 1),
        'S': complex(0, -1)
    }

    try:
        orientation = orientation_mapping[token]
    except KeyError:
        valid_orientation_tokens = list(orientation_mapping.keys())
        msg = f'Invalid orientation token: "{token}"; not one of {valid_orientation_tokens}'
        raise ValueError(msg)

    return orientation


def _parse_moves_line(line: str) -> str:
    """
    Validate and return moves specification (concatenated one-char moves).
    """
    try:
        moves = ''.join(_parse_move(move) for move in line)
    except ValueError:
        raise ValueError(f'Invalid moves: {line}')

    return moves


def _parse_move(token: str) -> str:
    """
    Validate and return a move (L/R/F char).
    """

    valid_move_tokens = 'LRF'

    if token not in valid_move_tokens:
        msg = f'Invalid move token: {token}; not one of {list(valid_move_tokens)}'
        raise ValueError(msg)

    return token
