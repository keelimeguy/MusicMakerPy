import argparse
import sys

from .string_instrument import StringInstrument
from musicmaker.theory.pitch import Pitch
from musicmaker.theory.chord import Chord, REDUCED_CHORD_REGEX


class Guitar(StringInstrument):
    def __init__(self, frets=22, strings=None):
        StringInstrument.__init__(self, frets, strings if strings else
                                  [Pitch.create('E', 2), Pitch.create('A', 2), Pitch.create('D', 3),
                                   Pitch.create('G', 3), Pitch.create('B', 3), Pitch.create('E', 4)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find the fingerings for ukulele.')
    parser.add_argument('-c', '--chord',
                        help='Find fingerings for the target chord (e.g. Ebdim7, C#sus4, C#sus4#5/A).')
    args = parser.parse_args()

    if args.chord:
        c = Chord.create(args.chord)
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
