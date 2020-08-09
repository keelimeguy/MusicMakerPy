import argparse
import logging
import sys

from .language.hiragana import Hiragana
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
        language = Hiragana
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
    _border_str = '-' * len(sys.version)
    print(f"{_border_str}\n{sys.version}\n{_border_str}", end='\n\n', flush=True)

    sys.stdout.reconfigure(encoding='utf-8')

    _parser = argparse.ArgumentParser(description='')
    _parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    _parser.add_argument('--log_file', default='logfile.log')
    _parser.add_argument('input')
    _parser.add_argument('-V', '--voice', default=None, help='voice, givin as name of folder within voice directory')
    _parser.add_argument('-T', '--voice_type', default=None, help='voice type of the given voice, e.g. CV, VCV, CVVC, VCCV')
    _parser.add_argument('-o', '--ust_output', default='sample.ust')
    _parser.add_argument('-w', '--wav_filename', default='sample.wav')
    _parser.add_argument('-t', '--tempo', type=float, default=100.0)
    _parser.add_argument('-f', '--flags', default='')
    _parser.add_argument('-E', '--english', action='store_true', help='parse lyrics as english')
    _args = _parser.parse_args()

    _format = '%(message)s'
    _verbose_format = '%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s'

    _fh = logging.FileHandler(_args.log_file, 'w', 'utf-8')
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(logging.Formatter(_verbose_format))

    _sh = logging.StreamHandler(sys.stdout)
    if _args.verbose:
        _sh.setLevel(logging.DEBUG)
        _sh.setFormatter(logging.Formatter(_verbose_format))
    else:
        _sh.setLevel(logging.INFO)
        _sh.setFormatter(logging.Formatter(_format))

    _log = logging.getLogger()
    _log.setLevel(level=logging.DEBUG)

    _log.addHandler(_fh)
    _log.addHandler(_sh)

    main(_args)
