"""
A set of helper structs.
"""
from typing import Tuple


class Orientation:
    """
    A pretty-printable structure that encapsulates a N/S/W/E orientation and operates upon it.
    """

    orientation_to_complex = {
        'W': complex(-1, 0),
        'E': complex(1, 0),
        'N': complex(0, 1),
        'S': complex(0, -1)
    }

    complex_to_orientation = {c: orientation for orientation, c
                              in orientation_to_complex.items()}

    def __init__(self, orientation: str):
        try:
            self.cplx_orientation = self.orientation_to_complex[orientation]
        except KeyError:
            valid_orientations = list(self.orientation_to_complex.keys())
            msg = f'Invalid orientation: "{orientation}"; not one of {valid_orientations}'
            raise ValueError(msg)

    @property
    def orientation(self) -> str:
        return self.complex_to_orientation[self.cplx_orientation]

    def rotate_left(self):
        """
        Perform 1/4 counter-clockwise rotation of orientation.
        """
        # Multiply the orientation by j = exp(j * pi / 2) in the complex plane
        self.cplx_orientation *= complex(0, 1)

    def rotate_right(self):
        """
        Perform 1/4 clockwise rotation of orientation.
        """
        # Multiply the orientation by -j = exp(-j * pi / 2) in the complex plane
        self.cplx_orientation *= complex(0, -1)

    def __str__(self):
        return self.orientation


class Position:
    """
    A pretty-printable structure that encapsulates a cartesian-coordinates position and operates
    upon it.
    """

    def __init__(self, x: int, y: int):
        self.cplx_position = complex(x, y)

    @property
    def x(self) -> int:
        return int(self.cplx_position.real)

    @property
    def y(self) -> int:
        return int(self.cplx_position.imag)

    def forward(self, orientation: Orientation, grid_size: Tuple[int, int]):
        """
        Move position 1 unit along a given orientation.
        """
        self.cplx_position += orientation.cplx_orientation
        self.restrict_to_grid(grid_size)

    def restrict_to_grid(self, grid_size: Tuple[int, int]):
        """
        Bring back position inside of grid, if needed.
        """
        max_x, max_y = grid_size
        x = max(0, min(self.x, max_x - 1))
        y = max(0, min(self.y, max_y - 1))
        self.cplx_position = complex(x, y)

    def __str__(self):
        return f'{self.x} {self.y}'


class Mower:
    """
    A structure that encapsulates a mower's position and orientation.
    """

    def __init__(self, position: Position, orientation: Orientation, grid_size: Tuple[int, int]):
        self._position = position
        self._orientation = orientation
        self._grid_size = grid_size

        # Force initial position inside grid
        self._position.restrict_to_grid(self._grid_size)

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    @property
    def orientation(self):
        return self._orientation.orientation

    def step(self, move: str):
        """
        Apply move (L/R/F char) to mower.
        """
        if move == 'L':
            self._orientation.rotate_left()
        elif move == 'R':
            self._orientation.rotate_right()
        elif move == 'F':
            self._position.forward(self._orientation, self._grid_size)
        else:
            raise NotImplementedError(f'Invalid move: "{move}"')

    def __str__(self):
        return f'{self._position} {self._orientation}'
