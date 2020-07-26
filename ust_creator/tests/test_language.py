import unittest

from ust_creator.language.english import English


class LanguageTestCase(unittest.TestCase):
    def test_gen_charset_from_line_english(self):
        test_cases = [
            ('ak', ['ak']),
            ('ka', ['ka']),

            ('aa', ['a', 'a']),

            ('akak', ['ak', 'ak']),
            ('akka', ['ak', 'ka']),
            ('kaak', ['ka', 'ak']),
            ('kaka', ['ka', 'ka']),

            ('akath', ['ak', 'ath']),
            ('aktha', ['ak', 'tha']),
            ('kaath', ['ka', 'ath']),
            ('katha', ['ka', 'tha']),

            ('athath', ['ath', 'ath']),
            ('aththa', ['ath', 'tha']),
            ('thaath', ['tha', 'ath']),
            ('thatha', ['tha', 'tha']),

            ('athak', ['ath', 'ak']),
            ('athka', ['ath', 'ka']),
            ('thaak', ['tha', 'ak']),
            ('thaka', ['tha', 'ka']),

            ('kakaa', ['ka', 'ka', 'a']),
            ('akkaa', ['ak', 'ka', 'a']),
            ('kaaka', ['ka', 'ak', 'a']),
            ('akaka', ['ak', 'ak', 'a']),

            ('kaaak', ['ka', 'a', 'ak']),
            ('akaak', ['ak', 'a', 'ak']),

            ('aakka', ['a', 'ak', 'ka']),
            ('aakak', ['a', 'ak', 'ak']),
        ]

        for line, expected in test_cases:
            answer = [c for c in English.gen_charset_from_line(line)]
            self.assertEqual(answer, expected)


if __name__ == '__main__':
    unittest.main()
