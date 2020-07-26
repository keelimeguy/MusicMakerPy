import argparse
import logging
import sys

from .language.katakana import Katakana
from .language.english import English
from .lyric import Lyric, parse_lyrics
from .voice import Voice
from .ust import UST

logger = logging.getLogger(__name__)


def main(args):
    if args.english:
        language = English
        args_voice = args.voice or 'Yami VCCV ENGLISH'
        args_voice_type = args.voice_type or 'CV'
    else:
        language = Katakana
        args_voice = args.voice or '桃音モモCute'
        args_voice_type = args.voice_type or 'VCV'

    voice = Voice(args_voice, voice_type=args_voice_type)

    project_name = ''.join(args.input.split('.')[:-1])
    ust = UST(project_name, args.wav_filename, voice, tempo=args.tempo, flags=args.flags)

    with open(args.input, 'r', encoding='utf-8') as f:
        lyrics = parse_lyrics(f, language=language)

    with open(args.ust_output, 'wb') as f:
        ust.write(f, lyrics, language=language)


if __name__ == '__main__':
    border_str = '-' * len(sys.version)
    print(f"{border_str}\n{sys.version}\n{border_str}", end='\n\n', flush=True)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    parser.add_argument('input')
    parser.add_argument('-V', '--voice', default=None, help='voice, givin as name of folder within voice directory')
    parser.add_argument('-T', '--voice_type', default=None, help='voice type of the given voice, e.g. CV, VCV, CVVC, VCCV')
    parser.add_argument('-o', '--ust_output', default='sample.ust')
    parser.add_argument('-w', '--wav_filename', default='sample.wav')
    parser.add_argument('-t', '--tempo', type=float, default=100.0)
    parser.add_argument('-f', '--flags', default='')
    parser.add_argument('-E', '--english', action='store_true', help='parse lyrics as english')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    main(args)
