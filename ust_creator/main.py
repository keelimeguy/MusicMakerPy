import argparse
import logging
import sys

from .lyric import Lyric, parse_lyrics
from .voice import Voice
from .ust import UST

logger = logging.getLogger(__name__)


def main(args):
    voice = Voice(args.voice, voice_type=args.voice_type)

    project_name = ''.join(args.input.split('.')[:-1])
    ust = UST(project_name, args.wav_filename, voice, tempo=args.tempo, flags=args.flags)

    with open(args.input, 'r', encoding='utf-8') as f:
        lyrics = parse_lyrics(f)

    with open(args.ust_output, 'wb') as f:
        ust.write(f, lyrics)


if __name__ == '__main__':
    border_str = '-' * len(sys.version)
    print(f"{border_str}\n{sys.version}\n{border_str}", end='\n\n', flush=True)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    parser.add_argument('input')
    parser.add_argument('-V', '--voice', default='桃音モモCute', help='voice, givin as name of folder within voice directory')
    parser.add_argument('-T', '--voice_type', default='VCV', help='voice type of the given voice, e.g. CV, VCV, CVVC, VCCV')
    parser.add_argument('-o', '--ust_output', default='sample.ust')
    parser.add_argument('-w', '--wav_filename', default='sample.wav')
    parser.add_argument('-t', '--tempo', type=float, default=100.0)
    parser.add_argument('-f', '--flags', default='')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    main(args)
