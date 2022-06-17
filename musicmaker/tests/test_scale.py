import unittest

from musicmaker.theory.scale import Scale
from musicmaker.theory.pitch import Pitch


class ScaleTestCase(unittest.TestCase):
    def test_scale(self):
        notes = [
            (1, 'C4'), (2, 'D4'), (3, 'Eb4'), (4, 'F4'), (5, 'G4'), (6, 'A4'), (7, 'B4'),
            (8, 'C5'), (9, 'D5'), (10, 'Eb5'), (11, 'F5'), (12, 'G5'), (13, 'A5'), (14, 'B5'), (15, 'C6'),
            (-1, 'Bb3'), (-2, 'Ab3'), (-3, 'G3'), (-4, 'F3'), (-5, 'Eb3'), (-6, 'D3'), (-7, 'C3'),
            (-8, 'Bb2'), (-9, 'Ab2'), (-10, 'G2'), (-11, 'F2'), (-12, 'Eb2'), (-13, 'D2'), (-14, 'C2'),
        ]

        s = Scale(Pitch('C'), Scale.Mode('MelodicMinor', [0, 2, 3, 5, 7, 9, 11], [10, 8, 7, 5, 3, 2, 0]))
        for i, note in notes:
            self.assertEqual(str(s.get_pitch(i)), note)

        s = Scale(Pitch('C'), Scale.Mode('MelodicMinor', [2, 1, 2, 2, 2, 2, 1], [2, 2, 1, 2, 2, 1, 2], as_intervals=True))
        for i, note in notes:
            self.assertEqual(str(s.get_pitch(i)), note)


if __name__ == '__main__':
    unittest.main()
