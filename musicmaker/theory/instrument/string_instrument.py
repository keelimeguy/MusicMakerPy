from musicmaker.theory.pitch import Pitch


class StringInstrument:
    def __init__(self, num_frets, strings):
        self.num_frets = num_frets  # num_frets = # notes per string
        self.strings = strings[::-1]  # array of Pitches, from highest string down
        # i.e [G4,C4,E4,A4] are strings 4, 3, 2, 1 (this makes sense don't worry)

    def num_strings(self):
        return len(self.strings)

    def get_pitch_on_string(self, string_num):
        return self.strings[string_num-1]

    def pluck(self, string_num, fret=0):
        return self.strings[string_num-1].transpose(fret)

    def strum(self, frets=None):
        if not frets:
            frets = [0]*self.num_frets
        notes = []
        for i, string in enumerate(self.strings):
            if frets[i] >= 0:
                notes.append(string.transpose(frets[i]))
        return notes

    def find_frets_for_note_on_string(self, note, string_num):
        if isinstance(note, str):
            note = Pitch.create(note)
        note_diff = note.value % 12 - self.strings[string_num-1].value % 12 + 12
        if note_diff >= 12:
            note_diff -= 12
        return list(range(note_diff, self.num_frets+1, 12))

    def find_frets_for_notes(self, notes):
        frets = []
        for i in range(self.num_strings()):
            frets.append([])
            for note in notes:
                frets[i] += self.find_frets_for_note_on_string(note, i+1)
            frets[i] = sorted(frets[i])
        return frets
