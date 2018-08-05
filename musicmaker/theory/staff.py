class Staff:
    def __init__(self, loop=False, tempo=120, meter_beats=4, meter_base=4):
        self.loop = loop
        self.tempo = tempo
        self.meter_beats = meter_beats
        self.meter_base = meter_base
        self.note_groups = [] # Array of (note[], length) pairs
        self.num_beats = 0

    def add(self, notes, length=1):
        self.num_beats += length
        self.note_groups.append((notes, length))

    def show(self):
        beat = 0
        for note_group in self.note_groups:
            print(beat, [str(note) for note in note_group[0]])
            beat += note_group[1]
        print(beat, 'END')
