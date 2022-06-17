import argparse
import random
import sys

from .pitch import Pitch


class Scale:
    class Mode:
        def __init__(self, name, ascending, descending=None, as_intervals=False):
            self.name = name
            if as_intervals:
                cur = 0
                self.ascending = [0]
                for interval in ascending:
                    cur += interval
                    if interval > 0 and cur < 12:
                        self.ascending.append(cur)
            else:
                self.ascending = ascending
            if descending is None:
                self.descending = self.ascending[::-1]
            elif as_intervals:
                cur = 0
                self.descending = [0]
                for interval in descending[::-1]:
                    cur += interval
                    if interval > 0 and cur < 12:
                        self.descending.insert(0, cur)
            else:
                self.descending = descending

        def find_step(self, pos):
            if pos == 0:
                return 0

            step = 0

            if pos > 0:
                # Adjust for octaves
                if pos > len(self.ascending):
                    step = int((pos-1) / len(self.ascending)) * 12
                    pos = ((pos-1) % len(self.ascending))
                else:
                    pos -= 1

                return step + self.ascending[pos]

            else:
                pos = -pos
                # Adjust for octaves
                if pos > len(self.descending):
                    step = int((pos-1) / len(self.descending)) * -12
                    pos = ((pos-1) % len(self.descending))
                else:
                    pos -= 1

                return step + self.descending[pos] - 12

    modes = {
        'Ionian':     Mode('Ionian', [0, 2, 4, 5, 7, 9, 11]),
        'Dorian':     Mode('Dorian', [0, 2, 3, 5, 7, 9, 10]),
        'Phrygian':   Mode('Phrygian', [0, 1, 3, 5, 7, 8, 10]),
        'Lydian':     Mode('Lydian', [0, 2, 4, 6, 7, 9, 11]),
        'Mixolydian': Mode('Mixolydian', [0, 2, 4, 5, 7, 9, 10]),
        'Aeolian':    Mode('Aeolian', [0, 2, 3, 5, 7, 8, 10]),
        'Locrian':    Mode('Locrian', [0, 1, 3, 5, 6, 8, 10]),

        'Major':         Mode('Major', [0, 2, 4, 5, 7, 9, 11]),
        'Minor':         Mode('Minor', [0, 2, 3, 5, 7, 8, 10]),
        'NaturalMinor':  Mode('NaturalMinor', [0, 2, 3, 5, 7, 8, 10]),
        'HarmonicMinor': Mode('HarmonicMinor', [0, 2, 3, 5, 7, 8, 11]),
        'MelodicMinor':  Mode('MelodicMinor', [0, 2, 3, 5, 7, 9, 11], [10, 8, 7, 5, 3, 2, 0]),

        # Foreign scales from www.medianmusic.com/ScaleForeign.html
        'Algerian':  Mode('Algerian', [0, 2, 3, 5, 6, 7, 8, 11]),
        'Arabian':   Mode('Arabian', [0, 2, 4, 5, 6, 8, 10]),
        'Balinese':  Mode('Balinese', [0, 1, 3, 7, 8]),
        'Byzantine': Mode('Byzantine', [0, 1, 4, 5, 7, 8, 11]),
        'Egyptian':  Mode('Egyptian', [0, 2, 5, 7, 10]),
        'Ethiopian': Mode('Ethiopian', [0, 2, 3, 5, 7, 8, 10]),
        'Hungarian': Mode('Hungarian', [0, 3, 4, 6, 7, 9, 10]),
        'Israeli':   Mode('Israeli', [0, 1, 4, 5, 7, 8, 10]),
        'Japanese':  Mode('Japanese', [0, 1, 5, 7, 8]),
        'Javanese':  Mode('Javanese', [0, 1, 3, 5, 7, 9, 10]),
        'Mongolian': Mode('Mongolian', [0, 2, 4, 7, 9]),
        'Persian':   Mode('Persian', [0, 1, 4, 5, 6, 8, 11]),
        'Spanish':   Mode('Spanish', [0, 1, 4, 5, 7, 8, 10]),

        'InSen': Mode('InSen', [0, 1, 5, 7, 10]),
        'Yo':    Mode('Yo', [0, 2, 5, 7, 10], [9, 7, 5, 2, 0]),
        # Naming of Hirajoshi modes from www.shredaholic.com/user48
        'Hirajoshi': Mode('Hirajoshi', [0, 2, 3, 7, 8]),
        'Iwato':     Mode('Iwato', [0, 1, 5, 6, 10]),
        'Kumoi':     Mode('Kumoi', [0, 4, 5, 9, 11]),
        'HonKumoi':  Mode('HonKumoi', [0, 1, 5, 7, 8]),
        'Chinese':   Mode('Chinese', [0, 4, 6, 7, 11]),

        # Bebop scales from www.mattwarnockguitar.com/bebop-scale
        'BebopDominant':        Mode('BebopDominant', [0, 2, 4, 5, 7, 9, 10, 11]),
        'BebopMinor':           Mode('BebopMinor', [0, 2, 3, 5, 7, 9, 10, 11]),
        'BebopMajor':           Mode('BebopMajor', [0, 2, 4, 5, 7, 8, 9, 11]),
        'BebopLydianDominant':  Mode('BebopLydianDominant', [0, 2, 4, 6, 7, 9, 10, 11]),
        'BebopAltered':         Mode('BebopAltered', [0, 1, 4, 5, 7, 8, 10, 11]),
        'BebopiiV':             Mode('BebopiiV', [0, 2, 4, 5, 6, 7, 9, 10, 11]),
        'BebopAllanHoldsworth': Mode('BebopAllanHoldsworth', [0, 2, 3, 4, 5, 7, 9, 10, 11]),
        # Bebop scales from https://en.wikipedia.org/wiki/Bebop_scale
        'BebopDorian':          Mode('BebopDorian', [0, 2, 3, 4, 5, 7, 9, 10]),
        'BebopMelodicMinor':    Mode('BebopMelodicMinor', [0, 2, 3, 5, 7, 8, 9, 11]),
        'BebopHarmonicMinor':   Mode('BebopHarmonicMinor', [0, 2, 3, 5, 7, 8, 10, 11]),
        'BebopNaturalMinor':   Mode('BebopNaturalMinor', [0, 2, 3, 5, 7, 8, 10, 11]),

        'HarmonicMajor':   Mode('HarmonicMajor', [0, 2, 4, 5, 7, 8, 11]),
        'DoubleHarmonic':  Mode('DoubleHarmonic', [0, 1, 4, 5, 7, 8, 11]),
        'Acoustic':        Mode('Acoustic', [0, 2, 4, 6, 7, 9, 10]),
        'LydianDominant':  Mode('LydianDominant', [0, 2, 4, 6, 7, 9, 10]),
        'LydianAugmented': Mode('LydianAugmented', [0, 2, 4, 6, 8, 9, 11]),
        'MajorBlues':      Mode('MajorBlues', [0, 2, 3, 4, 7, 9]),
        'MinorBlues':      Mode('MinorBlues', [0, 3, 5, 6, 7, 10]),
        'Neapolitan':      Mode('Neapolitan', [0, 1, 3, 5, 7, 9, 11]),
        'NeapolitanMinor': Mode('NeapolitanMinor', [0, 1, 3, 5, 7, 8, 11]),

        # Hexatonic from https://en.wikipedia.org/wiki/Hexatonic_scale
        'WholeTone':          Mode('WholeTone', [0, 2, 4, 6, 8, 10]),
        'Augmented':          Mode('Augmented', [0, 3, 4, 7, 8, 11]),
        'Prometheus':         Mode('Prometheus', [0, 2, 4, 6, 9, 10]),
        'Blues':              Mode('Blues', [0, 3, 5, 6, 7, 10]),
        'TriTone':            Mode('TriTone', [0, 1, 4, 6, 7, 10]),
        'TwoSemitoneTriTone': Mode('TwoSemitoneTriTone', [0, 1, 2, 6, 7, 8]),

        'WHDiminished':    Mode('WHDiminished', [0, 2, 3, 5, 6, 8, 9, 11]),
        'HWDiminished':    Mode('HWDiminished', [0, 1, 3, 4, 6, 7, 9, 10]),
        'Pentatonic':      Mode('Pentatonic', [0, 2, 4, 7, 9]),
        'PentatonicMinor': Mode('PentatonicMinor', [0, 2, 3, 7, 8]),
        'Chromatic':       Mode('Chromatic', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    }

    def __init__(self, root, mode):
        if isinstance(root, str):
            self.root = Pitch(root)
        else:
            self.root = root
        if isinstance(mode, str):
            self.mode = self.modes[mode]
        else:
            self.mode = mode

    def __str__(self):
        return (str(self.root)+' ' if self.root else '') + self.mode.name

    def __len__(self):
        return len(self.mode.ascending)

    def show(self):
        if self.root:
            print(str(self), ':', [str(self.root.transpose(interval))
                  for interval in self.mode.ascending+[12]+self.mode.descending])
        else:
            print(str(self), ':', self.mode.ascending+[12]+self.mode.descending)

    def get_pitch(self, num):
        return self.root.transpose(self.mode.find_step(num))


if __name__ == '__main__':

    from musicmaker.sound.staffplayer import StaffPlayer
    from .staff import Staff

    parser = argparse.ArgumentParser(
        description='Find the given scale.')
    parser.add_argument('-r', '--root',
                        help='The root for the scale (e.g. C, Bb, F#).')
    parser.add_argument('-p', '--play', action='store_true',
                        help='Play the given scale.')
    parser.add_argument('-m', '--mode',
                        help='The target mode for the scale (e.g. Major, TriTone, BebopLydianDominant).')
    args = parser.parse_args()

    s = None
    if args.mode:
        if args.mode in Scale.modes:
            mode = args.mode
        else:
            print('Valid modes are', [mode for mode in Scale.modes])
            sys.exit()
    else:
        mode = random.randrange(0, len(Scale.modes))
        mode = list(Scale.modes)[mode]

    if args.root and Pitch.valid(args.root):
        scale = Scale(Pitch(args.root), mode)
    elif args.root:
        print('Valid roots are', [root for root in Pitch.notes()])
        sys.exit()
    else:
        scale = Scale(None, mode)

    scale.show()

    if args.play and args.root:
        staff = Staff()
        for i in range(1, len(scale)+2):
            staff.add([scale.get_pitch(i)], 1)
        for i in range(-1, -len(scale)-1, -1):
            staff.add([scale.get_pitch(i).raise_octave()], 1)

        print('playing..', flush=True)
        player = StaffPlayer(staff)
        player.play()
