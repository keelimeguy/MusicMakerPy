import unittest

from musicmaker.theory.instrument.string_instrument import StringInstrument
from musicmaker.theory.pitch import Pitch


class StringInstrumentTestCase(unittest.TestCase):
    def test_string_instrument(self):
        instr = StringInstrument(24, [Pitch('A', 1), Pitch('B', 1), Pitch('C', 2), Pitch('D', 2)])

        self.assertEqual(instr.pluck(2, 14), Pitch('C##', 3))
        self.assertEqual(instr.strum(), [Pitch('D', 2), Pitch('C', 2), Pitch('B', 1), Pitch('A', 1)])
        self.assertEqual(instr.strum([-1, 0, 2, 1]), [Pitch('C', 2), Pitch('C#', 2), Pitch('A#', 1)])
        self.assertEqual(instr.find_frets_for_note_on_string('A', 4), [0, 12, 24])
        self.assertEqual(instr.find_frets_for_note_on_string('C', 4), [3, 15])
        self.assertEqual(instr.find_frets_for_note_on_string('A', 2), [9, 21])


if __name__ == '__main__':
    unittest.main()
