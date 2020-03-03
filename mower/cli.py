import logging

from mower.parser import parse_grid_size, parse_moves, parse_mower

LOGGER = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    path = './sample_input.txt'

    # Parse input file

    with open(path) as f:
        grid_size = parse_grid_size(f)

        all_mowers, all_moves = [], []

        mower = parse_mower(f, grid_size)
        while mower:
            moves = parse_moves(f)
            all_mowers.append(mower)
            all_moves.append(moves)
            mower = parse_mower(f, grid_size)

    LOGGER.debug(f'Parsed grid size: {grid_size}')
    LOGGER.debug(f'Parsed mowers: {list(map(str, all_mowers))}')
    LOGGER.debug(f'Parsed moves: {all_moves}')


if __name__ == '__main__':
    main()
