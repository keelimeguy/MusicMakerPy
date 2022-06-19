import unittest

from musicmaker.theory.chord import Chord
from musicmaker.theory.pitch import Pitch
from musicmaker.theory.scale import Scale


class ChordTestCase(unittest.TestCase):
    def test_chord_keys(self):
        for octave in [-1, 4, 9]:
            for note in Pitch.notes():
                p = Pitch.create(f"{note}", octave)
                root = p.value

                for kind, base_steps in [("", [0, 4, 7]), ("maj", [0, 4, 7]), ("mM", [0, 3, 7]), ("m", [0, 3, 7]),
                                         ("M", [0, 4, 7]), ("dim", [0, 3, 6]), ("aug", [0, 4, 8])]:

                    c = Chord.create(f"{note}{kind}", octave)
                    self.assertEqual(c, Chord.create(None, octave, key=f"{note}", kind=kind))
                    self.assertEqual(c.get_notes(), [Pitch.create(midi=root+i) for i in base_steps])

    def test_chord_additions(self):
        for octave in [-1, 4, 9]:
            for note in Pitch.notes():
                p = Pitch.create(f"{note}", octave)
                root = p.value

                major_mode = Scale.modes['Major']
                for add in [2, 3, 4, 7, 8, 9, 13]:

                    mod7 = 0
                    if add == 7:
                        mod7 = -1

                    for kind, base_steps, add_mod in [("", [0, 4, 7], mod7), ("maj", [0, 4, 7], 0), ("mM", [0, 3, 7], 0),
                                                      ("m", [0, 3, 7], mod7), ("M", [0, 4, 7], 0),
                                                      ("dim", [0, 3, 6], mod7*2), ("aug", [0, 4, 8], mod7)]:

                        c = Chord(f"{note}{kind}{add}", octave)
                        self.assertEqual(c, Chord.create(None, octave, key=f"{note}", kind=kind, add=f"{add}"))
                        self.assertEqual(c.get_notes(), [Pitch.create(midi=root+i)
                                         for i in sorted(set(base_steps + [major_mode.find_step(add) + add_mod]))])

                    for add2 in [2, 7, 8, 13]:
                        for mod, mod_adjust in [('', 0), ('#', 1), ('##', 2), ('b', -1), ('bb', -2)]:

                            for kind, base_steps, add_mod in [("", [0, 4, 7], mod7), ("maj", [0, 4, 7], 0),
                                                              ("mM", [0, 3, 7], 0), ("m", [0, 3, 7], mod7),
                                                              ("M", [0, 4, 7], 0), ("dim", [0, 3, 6], mod7*2),
                                                              ("aug", [0, 4, 8], mod7)]:

                                c = Chord(f"{note}{kind}{add}add{mod}{add2}", octave)
                                self.assertEqual(c, Chord.create(None, octave, key=f"{note}", kind=kind,
                                                                 add=f"{add}", adjust=f"add{mod}{add2}"))
                                self.assertEqual(c, Chord.create(None, octave, key=f"{note}", kind=kind,
                                                                 add=f"{add}", adjust2=f"add{mod}{add2}"))
                                self.assertEqual(c.get_notes(), [Pitch.create(midi=root+i)
                                                 for i in sorted(set(
                                                     base_steps + [major_mode.find_step(add) + add_mod,
                                                                   major_mode.find_step(add2)+mod_adjust]))])

    def test_chord_sus(self):
        for octave in [-1, 4, 9]:
            for note in Pitch.notes():
                p = Pitch.create(f"{note}", octave)
                root = p.value
                major_mode = Scale.modes['Major']

                for sus in [2, 4]:

                    for kind, base_7 in [("", 7), ("maj", 7), ("mM", 7), ("m", 7), ("M", 7), ("dim", 6), ("aug", 8)]:

                        c = Chord(f"{note}{kind}sus{sus}", octave)
                        self.assertEqual(c, Chord.create(None, octave, key=f"{note}", kind=kind, adjust=f"sus{sus}"))
                        self.assertEqual(c, Chord.create(None, octave, key=f"{note}", kind=kind, adjust2=f"sus{sus}"))
                        self.assertEqual(c.get_notes(), [Pitch.create(midi=root+i)
                                         for i in [0, major_mode.find_step(sus), base_7]])

    def test_chord_bass(self):
        for octave in [-1, 4, 9]:
            for note in Pitch.notes():
                p = Pitch.create(f"{note}", octave)
                root = p.value
                major_mode = Scale.modes['Major']

                for bass in [0, 3, 5, 12]:
                    step = major_mode.find_step(bass)

                    octave_diff = int((root+step)/12) - int(root/12)
                    octave_diff += 1 if (root+step) % 12 > root % 12 else 0

                    overall_octave_diff = octave - int((root+step)/12) + 1

                    for kind, base_steps in [("", [0, 4, 7]), ("maj", [0, 4, 7]), ("mM", [0, 3, 7]), ("m", [0, 3, 7]),
                                             ("M", [0, 4, 7]), ("dim", [0, 3, 6]), ("aug", [0, 4, 8])]:

                        c = Chord(f"{note}{kind}/{bass}", octave)
                        self.assertEqual(c, Chord.create(None, octave, key=f"{note}", kind=kind, bass=f"/{bass}"))
                        expected_pitches = [Pitch.create(midi=root+i)
                                            for i in sorted(set(base_steps+[step]))]
                        for i in range(len(expected_pitches)):
                            if expected_pitches[i].value == root+step:
                                break
                            replace = expected_pitches[i].raise_octave(octave_diff)
                            if replace.value == root+step:
                                expected_pitches[i] = replace.raise_octave(1)
                            else:
                                expected_pitches[i] = replace
                        self.assertEqual(c.get_notes(), [p.raise_octave(overall_octave_diff)
                                         for p in sorted(expected_pitches, key=lambda v: v.value)])


if __name__ == '__main__':
    unittest.main()
