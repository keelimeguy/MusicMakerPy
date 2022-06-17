import argparse
import sys

from .string_instrument import StringInstrument
from musicmaker.theory.pitch import Pitch
from musicmaker.theory.chord import Chord, REDUCED_CHORD_REGEX


class Guitar(StringInstrument):
    def __init__(self, frets=22, strings=None):
        StringInstrument.__init__(self, frets, strings if strings else
                                  [Pitch('E', 2), Pitch('A', 2), Pitch('D', 3), Pitch('G', 3), Pitch('B', 3), Pitch('E', 4)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find the fingerings for ukulele.')
    parser.add_argument('-c', '--chord',
                        help='Find fingerings for the target chord (e.g. Ebdim7, C#sus4, C#sus4#5/A).')
    args = parser.parse_args()

    if args.chord:
        c = Chord(args.chord)
        if c.valid:
            g = Guitar()
            frets = g.find_frets_for_notes(c.get_notes())
            for i in range(len(frets)):
                print(g.get_pitch_on_string(i+1), ':', end='')
                for fret in frets[i]:
                    print(' ', fret, end='')
                print()

        else:
            print("Chord must match regex:", REDUCED_CHORD_REGEX)
            sys.exit()

    else:
        g = Guitar()
        for i in range(g.num_strings()):
            print(g.get_pitch_on_string(i+1), ':', end='')
            for fret in range(g.num_frets+1):
                print(' ', fret, end='')
            print()
