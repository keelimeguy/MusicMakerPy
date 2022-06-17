import unittest

from ust_creator.language.english import English
from ust_creator.language.hiragana import Hiragana


class LanguageTestCase(unittest.TestCase):
    def test_gen_charset_from_line_english(self):
        test_cases = [
            ('EnngllEsh', ['E', 'nng', 'll', 'Esh']),
        ]

        for line, expected in test_cases:
            answer = [c for c in English.gen_charset_from_line(line)]
            self.assertEqual(answer, expected)

    def test_gen_charset_from_line_hiragana(self):
        test_cases = [
            ('ちゃっく', ['ちゃ', 'っ', 'く']),
        ]

        for line, expected in test_cases:
            answer = [c for c in Hiragana.gen_charset_from_line(line)]
            self.assertEqual(answer, expected)


if __name__ == '__main__':
    unittest.main()
