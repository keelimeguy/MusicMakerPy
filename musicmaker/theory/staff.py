class Staff:
    class Line:
        def __init__(self):
            self.note_groups = [] # array of ([pitch], length) pairs
            self.total_beats = 0
            self.cur_index = 0
            self.cur_beat = 0

        def add(self, notes, length):
            self.total_beats += length
            self.note_groups.append((notes, length))

        def restart(self):
            self.cur_index = 0
            self.cur_beat = 0

        def check_cur(self, beat):
            if self.cur_index < len(self.note_groups) and self.cur_beat <= beat:
                return self.note_groups[self.cur_index][1]

            return None

        def get_cur(self):
            self.cur_index += 1
            self.cur_beat += self.note_groups[self.cur_index-1][1]
            return self.note_groups[self.cur_index-1][0]


    def __init__(self, loop=False, tempo=120, meter_beats=0, meter_base=0):
        self.loop = loop
        self.tempo = tempo
        self.meter_beats = meter_beats
        self.meter_base = meter_base
        self.lines = {}
        self.total_beats = 0

    # length in number of beats
    def add(self, notes, length=1, line=1):
        if length <= 0:
            return

        if line not in self.lines:
            self.lines[line] = self.Line()

        self.lines[line].add(notes, length)

        if self.lines[line].total_beats > self.total_beats:
            self.total_beats = self.lines[line].total_beats

    def __iter__(self):
        self.cur_beat = 0
        for key in self.lines:
            self.lines[key].restart()
        return self

    def __next__(self):
        if self.cur_beat < self.total_beats:
            note_lines = {}
            min_length = None

            for key in self.lines:
                line = self.lines[key]
                cur =  line.check_cur(self.cur_beat)
                if cur == None:
                    continue

                note_lines[key] = line.get_cur()
                if min_length:
                    if cur < min_length:
                        min_length = cur
                else:
                    min_length = cur

            if min_length:
                self.cur_beat += min_length
                return (min_length, note_lines)
            else:
                raise StopIteration
        else:
            raise StopIteration

    def show(self):
        beat = 0
        for note_group in self:
            notes = []
            for line in note_group[1]:
                notes += [str(note) for note in note_group[1][line]]
            print(beat, notes)
            beat += note_group[0]
        print(beat, 'END')
