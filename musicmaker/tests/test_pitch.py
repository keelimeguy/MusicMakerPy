import unittest
import math

from musicmaker.theory.pitch import Pitch


class PitchTestCase(unittest.TestCase):
    def test_pitch(self):
        notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        sharp_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        self.assertEqual(Pitch("Cb", -2), Pitch(midi=-1))

        for octave in range(-1, 9):
            for note in Pitch.notes():
                p = Pitch(note, octave, 440)
                v = p.value % 12

                self.assertEqual(p, Pitch(midi=p.value))

                self.assertEqual(octave, int(p.value / 12) - 1)

                for i, step in enumerate(range(-p.value, 128-p.value)):
                    self.assertEqual(p.transpose(step), Pitch(notes[(v+step) % 12], octave + math.floor((v+step)/12)))
                    self.assertEqual(p.transpose(step).value, i)

                self.assertEqual(p.transpose(1), p.sharp())
                self.assertEqual(p.transpose(-1), p.flat())

                self.assertAlmostEqual(p.transpose(12).freq(), p.freq()*2)
                self.assertEqual(p.transpose(12).octave, p.octave+1)
                self.assertTrue(p.note_kind_equals(p.transpose(12)))

                self.assertAlmostEqual(p.raise_octave(3).freq(), p.freq()*8)
                self.assertEqual(p.raise_octave(3).octave, p.octave+3)
                self.assertTrue(p.note_kind_equals(p.raise_octave(3)))

                self.assertEqual(p.set_octave(-1).octave, -1)
                self.assertTrue(p.note_kind_equals(p.set_octave(-1)))
                self.assertEqual(p.set_octave(7).octave, 7)
                self.assertTrue(p.note_kind_equals(p.set_octave(7)))

                self.assertEqual(p.normal(), p)
                self.assertEqual(p.normal().name, notes[v])

                self.assertEqual(p.sharp_normal(), p)
                self.assertEqual(p.sharp_normal().name, sharp_notes[v])

                self.assertTrue(Pitch.valid(p.name))


if __name__ == '__main__':
    unittest.main()
