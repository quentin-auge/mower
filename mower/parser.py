import io
from typing import List, Tuple


class Parser:
    """
    Parse mower moves specification file:
      * grid size on first line (2 space-separated ints)
      * then, an alternance:
        * mower initial position (2 space-separated ints) and initial orientation (N/S/W/E char)
          line
        * mower moves (L/R/F chars) line

    Handle parsing errors by raising :exception:`ValueError` with relevant error messages.
    """

    def __init__(self, stream: io.TextIOBase):
        """
        Initialize parser.

        Arguments:
            stream: the specification file as an input stream that implements ``.readline()``.
        """
        self.stream = stream

    def parse_grid_size(self) -> complex:
        """
        Consume first line of stream to get grid size (2 space-separated ints -> complex).
        """
        line = self._readline()
        grid_size = self._parse_grid_size_line(line)
        return grid_size

    def parse_mowers(self) -> List[Tuple[complex, complex, str]]:
        """
        Consume remaining lines of stream to get mowers initial position (2 space-separated ints
        -> complex), initial orientation (N/S/W/E char -> complex) and moves (L/R/F chars).
        """

        mowers = []

        line = self._readline()

        while line:
            position, orientation = self._parse_initial_position_line(line)

            line = self._readline()
            moves = self._parse_moves_line(line)

            mowers.append((position, orientation, moves))

            line = self._readline()

        return mowers

    def _readline(self) -> str:
        """
        Read new line from the stream.
        """
        line = self.stream.readline().strip()
        return line

    def _parse_grid_size_line(self, line) -> complex:
        """
        Parse and validate a grid size specification (2 space-separated ints) to a complex.
        """
        try:
            x, y = line.split(' ')
            grid_size = self._parse_position(x, y)
        except ValueError:
            raise ValueError(f'Invalid grid size: "{line}"')

        return grid_size

    def _parse_initial_position_line(self, line: str) -> Tuple[complex, complex]:
        """
        Parse and validate initial position (2 space-separated ints) and orientation (N/S/W/E char)
        to a complex position and complex orientation.
        """
        try:
            x, y, orientation = line.split(' ')
            position = self._parse_position(x, y)
            orientation = self._parse_orientation(orientation)
        except ValueError:
            raise ValueError(f'Invalid initial position: "{line}"')

        return position, orientation

    def _parse_position(self, x: str, y: str) -> complex:
        """
        Parse and validate a position (two strings interepretable as ints) to a complex.
        """
        try:
            x, y = int(x), int(y)
        except ValueError:
            msg = f'Invalid position: "{(x, y)}", must be integers'
            raise ValueError(msg)

        return complex(x, y)

    def _parse_orientation(self, token: str) -> complex:
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

    def _parse_moves_line(self, line: str) -> str:
        """
        Validate and return moves specification (concatenated one-char moves).
        """
        try:
            moves = ''.join(self._parse_move(move) for move in line)
        except ValueError:
            raise ValueError(f'Invalid moves: {line}')

        return moves

    def _parse_move(self, token: str) -> str:
        """
        Validate and return a move (L/R/F char).
        """

        valid_move_tokens = 'LRF'

        if token not in valid_move_tokens:
            msg = f'Invalid move token: {token}; not one of {list(valid_move_tokens)}'
            raise ValueError(msg)

        return token
