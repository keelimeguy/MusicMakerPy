import logging

from typing import List
from abc import ABC

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
                logger.warning(f"character not parsed: {c.encode('utf-8')}")

    @classmethod
    def _gen_charset_from_line_helper(cls, line):
        for c in line:
            yield c

    @classmethod
    def get_charset(cls) -> List:
        return cls._charset

    @classmethod
    def get_suffix_lookup(cls) -> dict:
        return cls._suffix_lookup
