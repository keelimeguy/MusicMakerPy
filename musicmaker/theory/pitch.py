import functools
import math

NOTE_MAP = {
    'C':    12,       'B#':   12,       'Dbb':  12,
    'Db':   13,       'C#':   13,       'B##':  13,
    'D':    14,       'Ebb':  14,       'C##':  14,
    'Eb':   15,       'D#':   15,       'Fbb':  15,
    'E':    16,       'Fb':   16,       'D##':  16,
    'F':    17,       'E#':   17,       'Gbb':  17,
    'Gb':   18,       'F#':   18,       'E##':  18,
    'G':    19,       'Abb':  19,       'F##':  19,
    'Ab':   20,       'G#':   20,
    'A':    21,       'Bbb':  21,       'G##':  21,
    'Bb':   22,       'A#':   22,       'Cbb':  22,
    'B':    23,       'Cb':   23,       'A##':  23
}
REV_NOTE_MAP = {0: 'C', 1: 'Db', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F', 6: 'Gb', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'}
SHARP_NOTE_MAP = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}


@functools.lru_cache(128)
def freq_equal_temperament(n, base_freq):
    return base_freq * 2.0**((n-69)/12.0)


class Pitch:
    @functools.lru_cache(256)
    def create(name='C', octave=4, tuning=440, midi=None):
        return Pitch(name, octave, tuning, midi)

    def __init__(self, name='C', octave=4, tuning=440, midi=None):
        if midi is None:
            self.name = name
            self.octave = octave
            self.tuning = tuning
            self.value = NOTE_MAP[name]+12*octave
        else:
            self.value = midi
            self.tuning = tuning
            self.octave = math.floor(midi / 12) - 1
            self.name = REV_NOTE_MAP[midi % 12]

    def __str__(self):
        return self.name + str(self.octave)
    __repr__ = __str__

    def __eq__(self, other):
        return self.value == other.value

    def note_kind_equals(self, other):
        return self.value % 12 == other.value % 12

    def transpose(self, steps=1):
        return Pitch.create(tuning=self.tuning, midi=self.value + steps)

    def flat(self):
        return Pitch.create(tuning=self.tuning, midi=self.value - 1)

    def sharp(self):
        return Pitch.create(tuning=self.tuning, midi=self.value + 1)

    # Used to convert note name to one in REV_NOTE_MAP (flat-based)
    def normal(self):
        return Pitch.create(REV_NOTE_MAP[self.value % 12], self.octave, self.tuning)

    # Used to convert note name to one in SHARP_NOTE_MAP (sharp-based)
    def sharp_normal(self):
        return Pitch.create(SHARP_NOTE_MAP[self.value % 12], self.octave, self.tuning)

    def freq(self):
        return freq_equal_temperament(self.value, self.tuning)

    def raise_octave(self, steps=1):
        value = self.value + 12*steps
        return Pitch.create(tuning=self.tuning, midi=value)

    def set_octave(self, octave):
        return Pitch.create(REV_NOTE_MAP[self.value % 12], octave, self.tuning)

    @staticmethod
    def valid(name):
        return name in NOTE_MAP

    @staticmethod
    def notes():
        return [note for note in NOTE_MAP]
