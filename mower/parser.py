import io

class Parser:
    """
    Parse mower moves specification file.
    """

    def __init__(self, stream: io.TextIOBase):
        """
        Initialize parser.

        Arguments:
            stream: the specification file as an input stream that implements ``.readline()``.
        """
        self.stream = stream

    def parse_grid_size(self) -> complex:
        line = self._readline()
        grid_size = self._parse_grid_size_line(line)
        return grid_size

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

    def _parse_position(self, x: str, y: str) -> complex:
        """
        Parse and validate a position (two strings interepretable as ints) to a complex.
        """
        try:
            x, y = int(x), int(y)
        except ValueError:
            msg = f'Invalid position: {(x, y)}, must be integers'
            raise ValueError(msg)

        return complex(x, y)

    def _readline(self) -> str:
        """
        Read new line from the stream.
        """
        line = self.stream.readline().strip()
        return line