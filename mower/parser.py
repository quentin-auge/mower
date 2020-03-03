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
from typing import Tuple

from mower.structs import Mower, Orientation, Position


def parse_grid_size(stream: io.TextIOBase) -> Tuple[int, int]:
    """
    Consume grid size (2 space-separated ints) from stream.

    Args:
        stream: input specification file stream.
    """
    line = _readline(stream)
    grid_size = _parse_grid_size_line(line)
    return grid_size


def parse_mower(stream: io.TextIOBase, grid_size: Tuple[int, int]) -> Mower:
    """
    Consume mower initial state (initial position as 2 space-separated ints and initial
    orientation as N/S/W/E char) from stream.

    Args:
        stream: input specification file stream.
    """

    line = _readline(stream)
    if line:
        mower = _parse_mower_line(line, grid_size)
        return mower


def parse_moves(stream: io.TextIOBase) -> str:
    """
    Consume mower moves (L/R/F chars) from stream.

    Args:
        stream: input specification file stream.
    """

    line = _readline(stream)
    moves = _parse_moves_line(line)

    return moves


def _readline(stream) -> str:
    """
    Read new line from the stream.

    Args:
        stream: input specification file stream.
    """
    line = stream.readline().strip()
    return line


def _parse_grid_size_line(line) -> Tuple[int, int]:
    """
    Parse and validate a grid size specification (2 space-separated ints).

    Notes:
        Both coordinates must be > 0.
    """
    try:
        x, y = line.split(' ')
        grid_size = _parse_point(x, y)
        if grid_size[0] <= 0 or grid_size[1] <= 0:
            raise ValueError(f'Invalid grid size: {(x, y)}, must be integers > 0')
    except ValueError:
        raise ValueError(f'Invalid grid size: "{line}"')

    return grid_size


def _parse_mower_line(line: str, grid_size: Tuple[int, int]) -> Mower:
    """
    Parse and validate initial position (2 space-separated ints) and orientation (N/S/W/E char)
    of mower.
    """
    try:
        x, y, orientation = line.split(' ')
        x, y = _parse_point(x, y)
        position = Position(x, y)
        orientation = Orientation(orientation)
    except ValueError:
        raise ValueError(f'Invalid initial position and orientation: "{line}"')
    else:
        mower = Mower(position, orientation, grid_size)
        return mower


def _parse_point(x: str, y: str) -> Tuple[int, int]:
    """
    Parse and validate a position (two strings interpretable as ints).

    Notes:
        Both coordinates must be >= 0.
    """
    try:
        x, y = int(x), int(y)
        if x < 0 or y < 0:
            raise ValueError(f'Invalid position: {(x, y)}, must be integers >= 0')
    except ValueError:
        msg = f'Invalid position: {(x, y)}, must be integers >= 0'
        raise ValueError(msg)

    return x, y


def _parse_moves_line(line: str) -> str:
    """
    Validate and return moves specification (concatenated one-char moves).
    """
    try:
        moves = ''.join(_parse_move(move) for move in line)
    except ValueError:
        raise ValueError(f'Invalid moves: "{line}"')

    return moves


def _parse_move(token: str) -> str:
    """
    Validate and return a move (L/R/F char).
    """

    valid_move_tokens = 'LRF'

    if token not in valid_move_tokens:
        msg = f'Invalid move token: "{token}"; not one of {list(valid_move_tokens)}'
        raise ValueError(msg)

    return token
