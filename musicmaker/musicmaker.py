import argparse
import logging
import sys
import io

logger = logging.getLogger(__name__)


class MusicMaker:
    def __init__(self):
        pass


def main(args):
    MusicMaker()


if __name__ == '__main__':
    _border_str = '-' * len(sys.version)
    print(f"{_border_str}\n{sys.version}\n{_border_str}", end='\n\n', flush=True)

    _parser = argparse.ArgumentParser(description='A program to make, generate, and play: '
                                                  'chord progressions, phrases, and other such musical things.')
    _parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    _args = _parser.parse_args()

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if _args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    main(_args)
