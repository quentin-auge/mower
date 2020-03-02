from mower.structs import Position, Orientation

class Mower:
    """
    A structure that encapsulates a mower's position and orientation.
    """

    def __init__(self, position: Position, orientation: Orientation):
        self._position = position
        self._orientation = orientation

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    @property
    def orientation(self):
        return self._orientation.orientation

    def __str__(self):
        return f'{self._position} {self._orientation}'

def main():
    pass