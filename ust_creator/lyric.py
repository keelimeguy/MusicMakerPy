import logging

from typing import List

from musicmaker.theory.pitch import Pitch

from .note import Note

logger = logging.getLogger(__name__)


class Lyric():
    _valid_lyrics = [
        'あ', 'い', 'う', 'え', 'お',
        'か', 'き', 'く', 'け', 'こ',
        'が', 'ぎ', 'ぐ', 'げ', 'ご',
        'さ', 'し', 'す', 'せ', 'そ',
        'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
        'た', 'ち', 'つ', 'て', 'と',
        'だ', 'ぢ', 'づ', 'で', 'ど',
        'な', 'に', 'ぬ', 'ね', 'の',
        'は', 'ひ', 'ふ', 'へ', 'ほ',
        'ば', 'び', 'ぶ', 'べ', 'ぼ',
        'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ',
        'ま', 'み', 'む', 'め', 'も',
        'や', 'ゆ', 'よ',
        'ら', 'り', 'る', 'れ', 'ろ',
        'わ', 'を', 'ん',
        'きゃ', 'きゅ', 'きょ',
        'ぎゃ', 'ぎゅ', 'ぎょ',
        'しゃ', 'しゅ', 'しょ',
        'じゃ', 'じゅ', 'じょ',
        'ちゃ', 'ちゅ', 'ちょ',
        'ぢゃ', 'ぢゅ', 'ぢょ',
        'にゃ', 'にゅ', 'にょ',
        'ひゃ', 'ひゅ', 'ひょ',
        'びゃ', 'びゅ', 'びょ',
        'ぴゃ', 'ぴゅ', 'ぴょ',
        'みゃ', 'みゅ', 'みょ',
        'りゃ', 'りゅ', 'りょ',
        'R'
    ]

    LENGTH_QUARTER_NOTE = 480

    def __init__(self, note: Note, value: str = _valid_lyrics[0], length: float = 1):
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


def parse_lyrics(file) -> List[Lyric]:
    lyrics = []

    pitch = Pitch()
    for line in file:
        for c in line:
            if c in Lyric._valid_lyrics:
                lyric = Lyric(Note(pitch), value=c)
                lyrics.append(lyric)
                pitch = pitch.transpose()
            else:
                logger.warning(f"character not parsed: {c.encode('utf-8')}")

    return lyrics
