import eng_to_ipa as ipa
import logging

from typing import List

from musicmaker.theory.pitch import Pitch

from .language.katakana import Katakana
from .language.language import Language
from .language.english import English
from .note import Note

logger = logging.getLogger(__name__)


class Lyric():
    LENGTH_QUARTER_NOTE = 480

    def __init__(self, note: Note, value: str = Katakana.get_charset()[0], length: float = 1):
        self._value = value
        self._note = note
        self._length = length*self.LENGTH_QUARTER_NOTE

    @property
    def value(self):
        return self._value

    @property
    def note(self):
        return self._note

    @property
    def length(self):
        return self._length


KEYWORDS = [
    '',
]


def _add_line_to_lyrics(line, lyrics: List[Lyric], language: Language):
    for c in language.gen_charset_from_line(line):
        lyric = Lyric(Note(Pitch()), value=c)
        lyrics.append(lyric)

    return lyrics


def parse_lyrics(file, language: Language = Katakana) -> List[Lyric]:
    lyrics = []
    do_ipa_convert = False

    for line in file:
        if line == 'TO_IPA':
            do_ipa_convert = True

        elif do_ipa_convert:
            line = ipa.convert(line, keep_punct=False)

        lyrics = _add_line_to_lyrics(line, lyrics, language)

    return lyrics
