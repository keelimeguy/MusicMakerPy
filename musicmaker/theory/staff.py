class Staff:
    class Line:
        def __init__(self):
            self.note_groups = [] # array of ([pitch], length) pairs
            self.total_beats = 0
            self.cur_index = 0
            self.cur_beat = 0

        def __str__(self):
            return str(self.note_groups)

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
            return self.note_groups[self.cur_index-1]

        def catch_up(self, target_beats):
            if target_beats > self.total_beats:
                length = target_beats - self.total_beats
                self.total_beats += length
                self.note_groups.append((['z'], length))


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

    # When adding notes that are of different lengths but start at the same time
    def add_multi_length(self, note_groups, line=1):
        note_lines = []
        cur_line = 0
        for note_group in sorted(note_groups, key=lambda el:el[1]):
            note = note_group[0]
            length = note_group[1]
            if not note_lines:
                note_lines.append(([],length))
            if note_lines[cur_line][1] == length:
                note_lines[cur_line][0].append(note)
            else:
                cur_line += 1
                note_lines.append(([],length))
                note_lines[cur_line][0].append(note)

        if line not in self.lines:
            self.lines[line] = self.Line()

        for i, note_group in enumerate(note_lines[1:]):
            line_key = 'multi_length'+str(line)+'.'+str(i)
            while line_key in self.lines and self.lines[line_key].total_beats > self.lines[line].total_beats:
                line_key += 'x'

            if line_key not in self.lines:
                self.lines[line_key] = self.Line()
            self.lines[line_key].catch_up(self.lines[line].total_beats)

            notes = note_group[0]
            length = note_group[1]
            self.lines[line_key].add(notes, length)

        notes = note_lines[0][0]
        length = note_lines[0][1]
        self.lines[line].add(notes, length)

        if self.lines[line].total_beats > self.total_beats:
            self.total_beats = self.lines[line].total_beats




    def __iter__(self):
        self.cur_beat = 0
        for key in self.lines:
            if self.lines[key].total_beats > self.total_beats:
                self.total_beats = self.lines[key].total_beats
        for key in self.lines:
            self.lines[key].catch_up(self.total_beats)
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
                return note_lines
            else:
                print('oops')
                raise StopIteration
        else:
            raise StopIteration

    def show(self):
        beat = 0
        for note_group in self:
            notes = []
            min_beat = None
            for line in note_group:
                notes += [str(note_group) for note_group in note_group[line]]
                if not min_beat or note_group[line][1] < min_beat:
                    min_beat = note_group[line][1]
            print(beat, notes)
            beat += min_beat
        print(beat, 'END')
