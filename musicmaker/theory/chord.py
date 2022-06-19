import functools
import argparse
import re

from musicmaker.sound.staffplayer import StaffPlayer
from .staff import Staff
from .scale import Scale
from .pitch import Pitch

CHORD_REGEX = (
    r'(?P<key>[A-G](##?|bb?)?)'
    r'(?P<kind>(maj|mM|m|M|dim|aug)?)'
    r'(?P<add>([0-9]*)?)'
    r'(?P<adjust>((((##?|bb?)|(add|no)(##?|bb?)?)[0-9]+)|sus[24])*)'
    r'(?P<bass>((/([A-G](##?|bb?)?|(##?|bb?)?[0-9]+))?))'
    r'(?P<adjust2>((((##?|bb?)|(add|no)(##?|bb?)?)[0-9]+)|sus[24])*)'
)

REDUCED_CHORD_REGEX = (
    '[A-G](##?|bb?)?'
    '(maj|mM|m|M|dim|aug)?'
    '([0-9]*)?'
    '((((##?|bb?)|(add|no)(##?|bb?)?)[0-9]+)|sus[24])*'
    '(/([A-G](##?|bb?)?|(##?|bb?)?[0-9]+))?'
    '((((##?|bb?)|(add|no)(##?|bb?)?)[0-9]+)|sus[24])*'
)


class Chord:
    def create(name=None, octave=4, key="", kind="", add="", adjust="", bass="", adjust2=""):
        if name is None:
            name = f"{key}{kind}{add}{adjust}{bass}{adjust2}"
        return Chord._cached_create(name, octave)

    @functools.lru_cache(256)
    def _cached_create(name=None, octave=4):
        return Chord(name, octave)

    def __init__(self, name=None, octave=4, key="", kind="", add="", adjust="", bass="", adjust2=""):
        self.notes = []

        if name is None:
            self.name = f"{key}{kind}{add}{adjust}{bass}{adjust2}"
            adjust = adjust + adjust2

        else:
            self.name = name

            m = re.match(CHORD_REGEX, name)
            if m is None or m.group(0) != name:
                raise ValueError(f"Invalid chord: {name}")
            key = m.group('key')
            kind = m.group('kind')
            add = m.group('add')
            adjust = m.group('adjust') + m.group('adjust2')
            bass = m.group('bass')

        self.make(key, kind, add, adjust, bass, octave)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.notes == other.notes

    def show(self):
        print(self, ':', [str(pitch) for pitch in self.notes])

    def remove(self, pitch):
        if pitch in self.notes:
            self.notes.remove(pitch)

    def add(self, pitch):
        self.remove(pitch)
        self.notes.append(pitch)

    def get_notes(self):
        return self.notes

    def make(self, key, kind, add, adjust, bass, octave=4):  # noqa: C901
        self.valid = False

        if not key:
            return

        # Automatically add root
        root = Pitch.create(key).normal()
        self.add(root)

        # Seventh will get one flat
        minor7 = 1

        major_mode = Scale.modes['Major']

        # Add the appropriate third
        if kind == 'm' or kind == 'dim' or kind == 'mM':
            self.add(root.transpose(major_mode.find_step(3)-1))
        else:
            self.add(root.transpose(major_mode.find_step(3)))

        # Don't flatten seventh if major
        if kind == 'M' or kind == 'mM' or kind == 'maj':
            minor7 = 0

        # Add the appropriate fifth
        if kind == 'dim':
            self.add(root.transpose(major_mode.find_step(5)-1))

            # Flatten seventh twice if diminished
            minor7 = 2

        elif kind == 'aug':
            self.add(root.transpose(major_mode.find_step(5)+1))
        else:
            self.add(root.transpose(major_mode.find_step(5)))

        if add:
            add_id = int(add)

            # # Implicitly add seventh when notes above seventh are added
            # if add_id > 7:
            #     if minor7 == 0:
            #         self.add(root.transpose(major_mode.find_step(7)))
            #     elif minor7 == 1:
            #         self.add(root.transpose(major_mode.find_step(7)-1))
            #     elif minor7 == 2:
            #         self.add(root.transpose(major_mode.find_step(7)-2))

            if add_id == 7 and minor7 == 1:
                self.add(root.transpose(major_mode.find_step(add_id)-1))
            elif add_id == 7 and minor7 == 2:
                self.add(root.transpose(major_mode.find_step(add_id)-2))
            else:
                # # Add seventh when explicitly major
                # if add_id != 7 and (kind == 'M' or kind == 'mM' or kind == 'maj'):
                #     self.add(root.transpose(major_mode.find_step(7)))
                self.add(root.transpose(major_mode.find_step(add_id)))
        else:
            # # Add seventh when explicitly major
            # if kind == 'M' or kind == 'mM' or kind == 'maj':
            #     self.add(root.transpose(major_mode.find_step(7)))
            pass

        adjusted_root = root
        if adjust:
            # First deal with omissions so that we don't overwrite other adjustments
            no_base = re.sub(r'((((?<!no)##|(?<!no)bb|add(##?|bb?)?)[0-9]+)|sus[24])*', '', adjust)

            # Scrappy workaround to differentiate double sharps/flats
            no_base = re.sub('no##', 'DS', no_base)
            no_base = re.sub('nobb', 'DF', no_base)
            no_base = re.sub(r'((?<!no)#|(?<!no)b)[0-9]+', '', no_base)
            no_base = re.sub('DS', 'no##', no_base)
            no_base = re.sub('DF', 'nobb', no_base)

            for no_arg in no_base.split('no'):
                base_step_adjust = 0
                if no_arg:
                    if no_arg[0] == 'b':
                        base_step_adjust -= 1
                    elif no_arg[0] == '#':
                        base_step_adjust += 1
                    if len(no_arg) > 1:
                        if no_arg[1] == 'b':
                            base_step_adjust -= 1
                        elif no_arg[1] == '#':
                            base_step_adjust += 1
                    no_arg = re.sub(r'[#b]', '', no_arg)
                    self.remove(root.transpose(major_mode.find_step(int(no_arg)) + base_step_adjust))

            # Next deal with the suspended third so that thirds added later aren't overwritten
            sus_base = re.sub(r'(((##?|bb?)|(add|no)(##?|bb?)?)[0-9]+)*', '', adjust)
            for sus_split in sus_base.split('sus'):
                if sus_split:
                    next_step = int(sus_split)
                    # Remove existing third to be suspended
                    if kind in ['m', 'dim', 'mM']:
                        self.remove(root.transpose(major_mode.find_step(3)-1))
                    else:
                        self.remove(root.transpose(major_mode.find_step(3)))
                    self.add(root.transpose(major_mode.find_step(next_step)))

            # Deal with sharps
            sharp_base = re.sub(r'(((bb?|(add|no)(##?|bb?)?)[0-9]+)|sus[24])*', '', adjust)
            for sharp_split in sharp_base.split(r'(?<!#)#'):
                sharp_step_adjust = 1
                if sharp_split:
                    if sharp_split[1] == '#':
                        sharp_step_adjust = 2
                    sharp_split = re.sub('#', '', sharp_split)
                    new_note = root.transpose(major_mode.find_step(int(sharp_split)))
                    # Remove existing note to be sharpened
                    self.remove(new_note)
                    if new_note == root:
                        adjusted_root = new_note.transpose(sharp_step_adjust)
                        self.add(adjusted_root)
                    else:
                        self.add(new_note.transpose(sharp_step_adjust))

            # Deal with flats
            flat_base = re.sub(r'(((##?|(add|no)(##?|bb?)?)[0-9]+)|sus[24])*', '', adjust)
            for flat_split in flat_base.split(r'(?<!b)b'):
                flat_step_adjust = -1
                if flat_split:
                    if flat_split[1] == 'b':
                        flat_step_adjust = -2
                    flat_split = re.sub('b', '', flat_split)
                    new_note = root.transpose(major_mode.find_step(int(flat_split)))
                    # Remove existing note to be flattened
                    self.remove(new_note)
                    if new_note == root:
                        adjusted_root = new_note.transpose(flat_step_adjust)
                        self.add(adjusted_root)
                    else:
                        self.add(new_note.transpose(flat_step_adjust))

        bass_note = adjusted_root.transpose(0)

        if len(bass) > 1:
            step_adjust = 0
            if bass[1] == 'b':
                step_adjust -= 1
            elif bass[1] == '#':
                step_adjust += 1
            if len(bass) > 2:
                if bass[2] == 'b':
                    step_adjust -= 1
                elif bass[2] == '#':
                    step_adjust += 1
            bass_id = re.sub(r'/(##?|bb?)?', '', bass)

            if bass_id[0] >= '0' and bass_id[0] <= '9':
                bass_note = root.transpose(major_mode.find_step(int(bass_id)) + step_adjust)
            else:
                bass_note = Pitch.create(bass_id, adjusted_root.octave)
                bass_note = bass_note.set_octave(
                    adjusted_root.octave+1 if bass_note.value < adjusted_root.value else adjusted_root.octave)
            self.add(bass_note)

        # Deal with additions last, so other modifications don't affect them
        if adjust:
            add_base = re.sub(r'((((?<!add)##|(?<!add)bb|no(##?|bb?)?)[0-9]+)|sus[24])*', '', adjust)

            # Scrappy workaround to differentiate double sharps/flats
            add_base = re.sub('add##', 'DS', add_base)
            add_base = re.sub('addbb', 'DF', add_base)
            add_base = re.sub(r'((?<!add)#|(?<!add)b)[0-9]+', '', add_base)
            add_base = re.sub('DS', 'add##', add_base)
            add_base = re.sub('DF', 'addbb', add_base)

            for add_arg in add_base.split('add'):
                base_step_adjust = 0
                if add_arg:
                    if add_arg[0] == 'b':
                        base_step_adjust -= 1
                    elif add_arg[0] == '#':
                        base_step_adjust += 1
                    if len(add_arg) > 1:
                        if add_arg[1] == 'b':
                            base_step_adjust -= 1
                        elif add_arg[1] == '#':
                            base_step_adjust += 1
                    add_arg = re.sub(r'[#b]', '', add_arg)
                    self.add(root.transpose(major_mode.find_step(int(add_arg)) + base_step_adjust))

        self.order(bass_note, octave)

        self.notes.sort(key=lambda el: el.value)
        self.valid = True

    def order(self, bass_note, octave=4):
        # Sort notes so that bass_note would be positioned first
        if bass_note in self.notes:
            self.notes.sort(key=lambda el: el.value)
            next = self.notes[0]
            octave_diff = bass_note.octave - next.octave
            octave_diff += 1 if bass_note.value % 12 > next.value % 12 else 0
            while next.value != bass_note.value:
                self.remove(next)
                replace = next.raise_octave(octave_diff)
                if replace == bass_note:
                    self.add(replace.raise_octave(1))
                else:
                    self.add(replace)
                next = self.notes[0]
            octave_diff = octave - next.octave
            for i in range(len(self.notes)):
                self.notes[i] = self.notes[i].raise_octave(octave_diff)
        else:
            self.add(bass_note)
            self.order(bass_note)
            self.remove(bass_note)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find the notes of a given chord.')
    parser.add_argument('chord',
                        help='The target chord in standard format (e.g. Ebdim7, C#sus4, C#sus4#5/A).')
    parser.add_argument('-p', '--play', action='store_true',
                        help='Play the given chord.')
    args = parser.parse_args()

    c = Chord(args.chord, -1)
    if c.valid:
        c.show()

        if args.play:
            staff = Staff()
            staff.add(c.notes, 4)

            print('playing..', flush=True)
            player = StaffPlayer(staff)
            player.play()

    else:
        print("Chord must match regex:", REDUCED_CHORD_REGEX)
