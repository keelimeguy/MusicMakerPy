import logging
import random

from typing import List

from musicmaker.theory.pitch import Pitch, REV_NOTE_MAP

from .language.hiragana import Hiragana
from .language.language import Language
from .language.english import English
from .note import Note

logger = logging.getLogger(__name__)


class Lyric():
    LENGTH_QUARTER_NOTE = 480

    def __init__(self, note: Note, value: str = Hiragana.get_charset()[0], length: float = 1):
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

        val = random.randrange(3)

        lyric = Lyric(Note(Pitch(REV_NOTE_MAP[val])), value=c)
        lyrics.append(lyric)

    return lyrics


def parse_lyrics(file, language: Language = Hiragana) -> List[Lyric]:
    lyrics = []
    conversion_key = ''

    for line in file:
        line = line.strip()
        if not line:
            continue

        if language.is_conversion_section(line):
            conversion_key = line
            continue

        line = language.convert_section(line, conversion_key)

        for word in line.split():
            word = word.strip()
            logger.debug(word)
            lyrics = _add_line_to_lyrics(word+' ', lyrics, language)

    return lyrics
