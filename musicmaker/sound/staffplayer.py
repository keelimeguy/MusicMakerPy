import argparse
import sys

from musicmaker.theory.staff import Staff
from .wav import Wav

class StaffPlayer(Wav):
    def __init__(self, staff, sample_rate=44100):
        Wav.__init__(self, sample_rate)
        self.staff = staff
        self.sounds = {}
        self.ready = False

    def add_sound(self, key, sound):
        self.sounds[key] = sound

    def prepare(self):
        for note_lines in self.staff:

            notes = []
            length = note_lines[0]*60.0*1000.0/self.staff.tempo

            for key in note_lines[1]:
                if key in self.sounds:
                    sound = self.sounds[key]
                else:
                    sound = lambda f,d,v: self.synth.clean_ends(self.synth.sine_tone(f,d,v))
                for note in note_lines[1][key]:
                    if hasattr(note, 'freq'):
                        notes.append(note.freq())

            if len(notes) > 0:
                self.append_sound(self.synth.chord(notes, sound, length))
            else:
                self.add_rest(length)

        self.ready = True

    def play(self):
        if not self.ready:
            self.prepare()
        Wav.play(self, self.staff.loop)


if __name__ == '__main__':

    from musicmaker.theory.scale import Scale
    from musicmaker.theory.pitch import Pitch

    parser = argparse.ArgumentParser(
        description='Find the given scale.')
    parser.add_argument('-r', '--root', default='A',
        help='The root for the song (e.g. A, Cb, F#).')
    parser.add_argument('-m', '--mode', default='HarmonicMinor',
        help='The target mode for the song (e.g. HarmonicMinor, Major, Mixolydian).')
    parser.add_argument('-t', '--tempo', default=60,
        help='The tempo for the song in beats per minute (e.g. 60).')
    args = parser.parse_args()

    if args.mode in Scale.modes:
        if args.root and Pitch.valid(args.root):
            scale = Scale(Pitch(args.root, 2), args.mode)
        else:
            print('Valid roots are', [root for root in Pitch.notes()])
            sys.exit()
    elif args.mode not in Scale.modes or len(scale.mode.ascending) != 7:
        modes = []
        for mode in Scale.modes:
            if len(Scale.modes[mode].ascending) == 7:
                modes.append(mode)
        print('Valid modes are', modes)
        sys.exit()

    staff = Staff(tempo=int(args.tempo))
    for n in [8, 6, 5, 7, 8, 9, 7, 8]:
        pitch = scale.get_pitch(n)
        staff.add([pitch, scale.get_pitch(n+2), scale.get_pitch(n+4)], 2, line=1)
        staff.add([], 2, line=2)

    for n in [8, 6, 5, 7, 8, 9, 7, 8]:
        pitch = scale.get_pitch(n)
        staff.add([pitch, scale.get_pitch(n+2), scale.get_pitch(n+4)], 2, line=1)
    for n in [25, 24, 20, 19, 18, 19, 16, 15]:
        pitch = scale.get_pitch(n)
        staff.add([pitch], 2, line=2)

    player = StaffPlayer(staff)
    player.add_sound(1, player.synth.chime)
    player.add_sound(2, player.synth.chime_soft)
    player.play()
