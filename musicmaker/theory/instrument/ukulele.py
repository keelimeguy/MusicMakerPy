import argparse
import sys

from .string_instrument import StringInstrument
from musicmaker.theory.pitch import Pitch
from musicmaker.theory.chord import Chord, REDUCED_CHORD_REGEX


class Ukulele(StringInstrument):
    def __init__(self, frets=12, strings=None):
        StringInstrument.__init__(self, frets, strings if strings else
                                  [Pitch.create('G', 4), Pitch.create('C', 4), Pitch.create('E', 4), Pitch.create('A', 4)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find the fingerings for ukulele.')
    parser.add_argument('-c', '--chord',
                        help='Find fingerings for the target chord (e.g. Ebdim7, C#sus4, C#sus4#5/A).')
    args = parser.parse_args()

    if args.chord:
        c = Chord.create(args.chord)
        if c.valid:
            uke = Ukulele()
            frets = uke.find_frets_for_notes(c.get_notes())
            for i in range(len(frets)):
                print(uke.get_pitch_on_string(i+1), ':', end='')
                for fret in frets[i]:
                    print(' ', fret, end='')
                print()

        else:
            print("Chord must match regex:", REDUCED_CHORD_REGEX)
            sys.exit()

    else:
        uke = Ukulele()
        for i in range(uke.num_strings()):
            print(uke.get_pitch_on_string(i+1), ':', end='')
            for fret in range(uke.num_frets+1):
                print(' ', fret, end='')
            print()
