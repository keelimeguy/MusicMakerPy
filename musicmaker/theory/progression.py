from .staff import Staff

class Progression(Staff):
    def __init__(self, loop=False, tempo=120, meter_beats=4, meter_base=4):
        Staff.__init__(self, loop, tempo, meter_beats, meter_base)

    def add(self, chord, length=1):
        self.num_beats += length
        if hasattr(chord, 'get_notes'):
            self.note_groups.append((chord.get_notes(), length, chord.name))
        else:
            self.note_groups.append((chord[1], length, chord[0]))

    def show(self):
        beat = 0
        for note_group in self.note_groups:
            print(beat, ': (', note_group[2], ')', '\t' if len(note_group[2])<=5 else '', '\t', [str(note) for note in note_group[0]])
            beat += note_group[1]
        print(beat, 'END')
