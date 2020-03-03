import logging
from argparse import ArgumentParser

from mower.parser import parse_grid_size, parse_moves, parse_mower

LOGGER = logging.getLogger(__name__)


def main():


    # Parse command line

    parser = ArgumentParser(description='Move a mower on a lawn')
    parser.add_argument('path', help='instructions file for moving the mower')
    parser.add_argument('--verbose', '-v', action='store_true', help='debug_mode')
    args = parser.parse_args()

    # Setup logging

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    # Parse input file

    with open(args.path) as f:
        grid_size = parse_grid_size(f)

        all_mowers, all_moves = [], []

        mower = parse_mower(f, grid_size)
        while mower:
            moves = parse_moves(f)
            all_mowers.append(mower)
            all_moves.append(moves)
            mower = parse_mower(f, grid_size)

    LOGGER.debug(f' Parsed grid size: {grid_size}')
    LOGGER.debug(f' Parsed mowers: {list(map(str, all_mowers))}')
    LOGGER.debug(f' Parsed moves: {all_moves}')
    LOGGER.debug('')

    # Execute moves

    for i, (mower, moves) in enumerate(zip(all_mowers, all_moves), 1):
        LOGGER.debug(f' Mower {i}')
        LOGGER.debug(f'   {mower}')

        for move in moves:
            mower.step(move)
            LOGGER.debug(f' {move} {mower}')

        LOGGER.debug('')

    # Print result

    for mower in all_mowers:
        print(mower)

if __name__ == '__main__':
    main()
