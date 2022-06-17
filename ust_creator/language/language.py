import logging

from typing import List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Language(ABC):
    _charset = []
    _suffix_lookup = {}
    _as_valid = {}

    @classmethod
    def gen_charset_from_line(cls, line):
        for c in cls._gen_charset_from_line_helper(line):
            if c in cls._as_valid:
                c = cls._as_valid[c]

            if c in cls._charset:
                yield c

            else:
                logger.warning(f"exported invalid sequence: {c}")
                yield c

    @classmethod
    def _gen_charset_from_line_helper(cls, line: str):  # noqa: C901
        output = []
        next_from_charset = ''
        line = line[::-1]

        for i, c in enumerate(line):
            logger.debug("--------------")
            logger.debug(f"current:{next_from_charset}")
            logger.debug(f"newchar:{c}")

            if c in cls._as_valid.keys() or c == 'R':
                if next_from_charset:
                    logger.debug(f"out:{next_from_charset}")
                    output.append(next_from_charset)
                    next_from_charset = ''

                logger.debug(f"out:{c}")
                if c in cls._as_valid:
                    if isinstance(cls._as_valid[c], list):
                        output += cls._as_valid[c]
                    else:
                        output.append(cls._as_valid[c])
                else:
                    output.append(c)
                continue

            # Greedy method ...
            new_word = next_from_charset
            found_future_match = False

            for j in range(i, min(i+3, len(line))):
                new_word = line[j] + new_word
                if new_word in cls._charset:
                    found_future_match = True
                    break

            if found_future_match:
                next_from_charset = c + next_from_charset
                continue

            if next_from_charset in cls._charset:
                logger.debug(f"out:{next_from_charset}")
                output.append(next_from_charset)
                next_from_charset = c
                continue

            next_from_charset = c + next_from_charset

        if next_from_charset in cls._charset:
            logger.debug("--------------")
            logger.debug("leftovers")
            logger.debug(f"out:{next_from_charset}")
            output.append(next_from_charset)

        else:
            line = line[::-1]
            new_word = next_from_charset
            done = False
            for j in range(len(next_from_charset), min(len(next_from_charset)+3, len(line))):
                new_word = new_word + line[j]
                if new_word in cls._charset:
                    logger.debug(f"out:{new_word}")
                    output.append(new_word)
                    done = True
                    break

            if not done:
                output.append(next_from_charset)

        for phenome in output[::-1]:
            yield phenome

    @classmethod
    def get_charset(cls) -> List:
        return cls._charset

    @classmethod
    def get_suffix_lookup(cls) -> dict:
        return cls._suffix_lookup

    @classmethod
    @abstractmethod
    def convert_section(cls, line: str, conversion_key: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def is_conversion_section(cls, line: str) -> bool:
        pass
