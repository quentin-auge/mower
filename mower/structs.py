"""
A set of helper structs.
"""

from typing import Union

class Position:
    """
    A pretty-printable structure that encapsulates a cartesian-coordinates position.
    """

    def __init__(self, x: Union[str, int], y: Union[str, int]):

        try:
            x, y = int(x), int(y)
        except ValueError:
            msg = f'Invalid position: "{(x, y)}", must be integers'
            raise ValueError(msg)

        self._position = complex(x, y)

    @property
    def x(self):
        return int(self._position.real)

    @property
    def y(self):
        return int(self._position.imag)

    def __str__(self):
        return f'{self.x} {self.y}'


class Orientation:
    """
    A pretty-printable structure that encapsulates a N/S/W/E orientation.
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
            self._orientation = self.orientation_to_complex[orientation]
        except KeyError:
            valid_orientations = list(self.orientation_to_complex.keys())
            msg = f'Invalid orientation: "{orientation}"; not one of {valid_orientations}'
            raise ValueError(msg)

    @property
    def orientation(self):
        return self.complex_to_orientation[self._orientation]

    def __str__(self):
        return self.orientation
