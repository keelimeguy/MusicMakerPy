import unittest
import math

from musicmaker.theory.pitch import Pitch

class PitchTestCase(unittest.TestCase):
    def test_pitch_steps(self):
        notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        for note in Pitch.notes():
            p = Pitch(note, 4, 440)
            i = p.value%12
            for step in range(-40, 60):
                self.assertEqual(p.transpose(step), Pitch(notes[(i+step)%12], 4 + math.floor((i+step)/12)))
            self.assertEqual(p.transpose(1), p.sharp())
            self.assertEqual(p.transpose(-1), p.flat())
            self.assertEqual(p.transpose(12).freq(), p.freq()*2)
            self.assertEqual(p.transpose(12).octave, p.octave+1)

if __name__ == '__main__':
    unittest.main()
