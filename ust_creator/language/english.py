import logging

from .language import Language

logger = logging.getLogger(__name__)


class English(Language):
    # Not all combinations are necessarily possible, despite existing here

    _charset = [
        'a',  # awful
        'e',  # bet
        'i',  # pick
        'o',  # loot
        'u',  # cut
        'A',  # aim
        'E',  # beet
        'I',  # right
        'O',  # bowl
        '@',  # cat
        '3',  # heard
        '1',  # king or think, please combine with 1ng or enk endings (can also be used as a less-harsh E)
        '&',  # and / amber
        '6',  # look, or your when combined with 6r ending
        '8',  # town, out
        '9',  # ball, gawk
        'Q',  # void, or boar when combined with Or ending

        '-a', '-e', '-i', '-o', '-u', '-A', '-E', '-I', '-O', '-@', '-3', '-1', '-&', '-6', '-8', '-9', '-Q',
        'a-', 'e-', 'i-', 'o-', 'u-', 'A-', 'E-', 'I-', 'O-', '@-', '3-', '1-', '&-', '6-', '8-', '9-', 'Q-',

        'ab', 'eb', 'ib', 'ob', 'ub', 'Ab', 'Eb', 'Ib', 'Ob', '@b', '3b', '1b', '&b', '6b', '8b', '9b', 'Qb',
        'ba', 'be', 'bi', 'bo', 'bu', 'bA', 'bE', 'bI', 'bO', 'b@', 'b3', 'b1', 'b&', 'b6', 'b8', 'b9', 'bQ',

        'ac', 'ec', 'ic', 'oc', 'uc', 'Ac', 'Ec', 'Ic', 'Oc', '@c', '3c', '1c', '&c', '6c', '8c', '9c', 'Qc',
        'ca', 'ce', 'ci', 'co', 'cu', 'cA', 'cE', 'cI', 'cO', 'c@', 'c3', 'c1', 'c&', 'c6', 'c8', 'c9', 'cQ',

        'ad', 'ed', 'id', 'od', 'ud', 'Ad', 'Ed', 'Id', 'Od', '@d', '3d', '1d', '&d', '6d', '8d', '9d', 'Qd',
        'da', 'de', 'di', 'do', 'du', 'dA', 'dE', 'dI', 'dO', 'd@', 'd3', 'd1', 'd&', 'd6', 'd8', 'd9', 'dQ',

        'af', 'ef', 'if', 'of', 'uf', 'Af', 'Ef', 'If', 'Of', '@f', '3f', '1f', '&f', '6f', '8f', '9f', 'Qf',
        'fa', 'fe', 'fi', 'fo', 'fu', 'fA', 'fE', 'fI', 'fO', 'f@', 'f3', 'f1', 'f&', 'f6', 'f8', 'f9', 'fQ',

        'ag', 'eg', 'ig', 'og', 'ug', 'Ag', 'Eg', 'Ig', 'Og', '@g', '3g', '1g', '&g', '6g', '8g', '9g', 'Qg',
        'ga', 'ge', 'gi', 'go', 'gu', 'gA', 'gE', 'gI', 'gO', 'g@', 'g3', 'g1', 'g&', 'g6', 'g8', 'g9', 'gQ',

        'ah', 'eh', 'ih', 'oh', 'uh', 'Ah', 'Eh', 'Ih', 'Oh', '@h', '3h', '1h', '&h', '6h', '8h', '9h', 'Qh',
        'ha', 'he', 'hi', 'ho', 'hu', 'hA', 'hE', 'hI', 'hO', 'h@', 'h3', 'h1', 'h&', 'h6', 'h8', 'h9', 'hQ',

        'aj', 'ej', 'ij', 'oj', 'uj', 'Aj', 'Ej', 'Ij', 'Oj', '@j', '3j', '1j', '&j', '6j', '8j', '9j', 'Qj',
        'ja', 'je', 'ji', 'jo', 'ju', 'jA', 'jE', 'jI', 'jO', 'j@', 'j3', 'j1', 'j&', 'j6', 'j8', 'j9', 'jQ',

        'ak', 'ek', 'ik', 'ok', 'uk', 'Ak', 'Ek', 'Ik', 'Ok', '@k', '3k', '1k', '&k', '6k', '8k', '9k', 'Qk',
        'ka', 'ke', 'ki', 'ko', 'ku', 'kA', 'kE', 'kI', 'kO', 'k@', 'k3', 'k1', 'k&', 'k6', 'k8', 'k9', 'kQ',

        'al', 'el', 'il', 'ol', 'ul', 'Al', 'El', 'Il', 'Ol', '@l', '3l', '1l', '&l', '6l', '8l', '9l', 'Ql',
        'la', 'le', 'li', 'lo', 'lu', 'lA', 'lE', 'lI', 'lO', 'l@', 'l3', 'l1', 'l&', 'l6', 'l8', 'l9', 'lQ',

        'am', 'em', 'im', 'om', 'um', 'Am', 'Em', 'Im', 'Om', '@m', '3m', '1m', '&m', '6m', '8m', '9m', 'Qm',
        'ma', 'me', 'mi', 'mo', 'mu', 'mA', 'mE', 'mI', 'mO', 'm@', 'm3', 'm1', 'm&', 'm6', 'm8', 'm9', 'mQ',

        'an', 'en', 'in', 'on', 'un', 'An', 'En', 'In', 'On', '@n', '3n', '1n', '&n', '6n', '8n', '9n', 'Qn',
        'na', 'ne', 'ni', 'no', 'nu', 'nA', 'nE', 'nI', 'nO', 'n@', 'n3', 'n1', 'n&', 'n6', 'n8', 'n9', 'nQ',

        'ap', 'ep', 'ip', 'op', 'up', 'Ap', 'Ep', 'Ip', 'Op', '@p', '3p', '1p', '&p', '6p', '8p', '9p', 'Qp',
        'pa', 'pe', 'pi', 'po', 'pu', 'pA', 'pE', 'pI', 'pO', 'p@', 'p3', 'p1', 'p&', 'p6', 'p8', 'p9', 'pQ',

        'aq', 'eq', 'iq', 'oq', 'uq', 'Aq', 'Eq', 'Iq', 'Oq', '@q', '3q', '1q', '&q', '6q', '8q', '9q', 'Qq',
        'qa', 'qe', 'qi', 'qo', 'qu', 'qA', 'qE', 'qI', 'qO', 'q@', 'q3', 'q1', 'q&', 'q6', 'q8', 'q9', 'qQ',

        'ar', 'er', 'ir', 'or', 'ur', 'Ar', 'Er', 'Ir', 'Or', '@r', '3r', '1r', '&r', '6r', '8r', '9r', 'Qr',
        'ra', 're', 'ri', 'ro', 'ru', 'rA', 'rE', 'rI', 'rO', 'r@', 'r3', 'r1', 'r&', 'r6', 'r8', 'r9', 'rQ',

        'as', 'es', 'is', 'os', 'us', 'As', 'Es', 'Is', 'Os', '@s', '3s', '1s', '&s', '6s', '8s', '9s', 'Qs',
        'sa', 'se', 'si', 'so', 'su', 'sA', 'sE', 'sI', 'sO', 's@', 's3', 's1', 's&', 's6', 's8', 's9', 'sQ',

        'at', 'et', 'it', 'ot', 'ut', 'At', 'Et', 'It', 'Ot', '@t', '3t', '1t', '&t', '6t', '8t', '9t', 'Qt',
        'ta', 'te', 'ti', 'to', 'tu', 'tA', 'tE', 'tI', 'tO', 't@', 't3', 't1', 't&', 't6', 't8', 't9', 'tQ',

        'av', 'ev', 'iv', 'ov', 'uv', 'Av', 'Ev', 'Iv', 'Ov', '@v', '3v', '1v', '&v', '6v', '8v', '9v', 'Qv',
        'va', 've', 'vi', 'vo', 'vu', 'vA', 'vE', 'vI', 'vO', 'v@', 'v3', 'v1', 'v&', 'v6', 'v8', 'v9', 'vQ',

        'ax', 'ex', 'ix', 'ox', 'ux', 'Ax', 'Ex', 'Ix', 'Ox', '@x', '3x', '1x', '&x', '6x', '8x', '9x', 'Qx',
        'xa', 'xe', 'xi', 'xo', 'xu', 'xA', 'xE', 'xI', 'xO', 'x@', 'x3', 'x1', 'x&', 'x6', 'x8', 'x9', 'xQ',

        'az', 'ez', 'iz', 'oz', 'uz', 'Az', 'Ez', 'Iz', 'Oz', '@z', '3z', '1z', '&z', '6z', '8z', '9z', 'Qz',
        'za', 'ze', 'zi', 'zo', 'zu', 'zA', 'zE', 'zI', 'zO', 'z@', 'z3', 'z1', 'z&', 'z6', 'z8', 'z9', 'zQ',

        'aw', 'ew', 'iw', 'ow', 'uw', 'Aw', 'Ew', 'Iw', 'Ow', '@w', '3w', '1w', '&w', '6w', '8w', '9w', 'Qw',
        'wa', 'we', 'wi', 'wo', 'wu', 'wA', 'wE', 'wI', 'wO', 'w@', 'w3', 'w1', 'w&', 'w6', 'w8', 'w9', 'wQ',

        'ay', 'ey', 'iy', 'oy', 'uy', 'Ay', 'Ey', 'Iy', 'Oy', '@y', '3y', '1y', '&y', '6y', '8y', '9y', 'Qy',
        'ya', 'ye', 'yi', 'yo', 'yu', 'yA', 'yE', 'yI', 'yO', 'y@', 'y3', 'y1', 'y&', 'y6', 'y8', 'y9', 'yQ',

        # dh = there
        'dha', 'dhe', 'dhi', 'dho', 'dhu', 'dhA', 'dhE', 'dhI', 'dhO', 'dh@', 'dh3', 'dh1', 'dh&', 'dh6', 'dh8', 'dh9', 'dhQ',
        'adh', 'edh', 'idh', 'odh', 'udh', 'Adh', 'Edh', 'Idh', 'Odh', '@dh', '3dh', '1dh', '&dh', '6dh', '8dh', '9dh', 'Qdh',
        # th = wrath
        'tha', 'the', 'thi', 'tho', 'thu', 'thA', 'thE', 'thI', 'thO', 'th@', 'th3', 'th1', 'th&', 'th6', 'th8', 'th9', 'thQ',
        'ath', 'eth', 'ith', 'oth', 'uth', 'Ath', 'Eth', 'Ith', 'Oth', '@th', '3th', '1th', '&th', '6th', '8th', '9th', 'Qth',
        # zh = azure
        'zha', 'zhe', 'zhi', 'zho', 'zhu', 'zhA', 'zhE', 'zhI', 'zhO', 'zh@', 'zh3', 'zh1', 'zh&', 'zh6', 'zh8', 'zh9', 'zhQ',
        'azh', 'ezh', 'izh', 'ozh', 'uzh', 'Azh', 'Ezh', 'Izh', 'Ozh', '@zh', '3zh', '1zh', '&zh', '6zh', '8zh', '9zh', 'Qzh',

        'R'
    ]

    _as_valid = {
        '\n': 'R', ' ': 'R'
    }

    _suffix_lookup = {
        'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u', 'A': 'A', 'E': 'E', 'I': 'I', 'O': 'O',
        '@': '@', '3': '3', '1': '1', '&': '&', '6': '6', '8': '8', '9': '9', 'Q': 'Q',

        'a-': '-', 'e-': '-', 'i-': '-', 'o-': '-', 'u-': '-', 'A-': '-', 'E-': '-', 'I-': '-', 'O-': '-',
        '@-': '-', '3-': '-', '1-': '-', '&-': '-', '6-': '-', '8-': '-', '9-': '-', 'Q-': '-',
        '-a': 'a', '-e': 'e', '-i': 'i', '-o': 'o', '-u': 'u', '-A': 'A', '-E': 'E', '-I': 'I', '-O': 'O',
        '-@': '@', '-3': '3', '-1': '1', '-&': '&', '-6': '6', '-8': '8', '-9': '9', '-Q': 'Q',

        'ab': '-', 'eb': '-', 'ib': '-', 'ob': '-', 'ub': '-', 'Ab': '-', 'Eb': '-', 'Ib': '-', 'Ob': '-',
        '@b': '-', '3b': '-', '1b': '-', '&b': '-', '6b': '-', '8b': '-', '9b': '-', 'Qb': '-',
        'ba': 'a', 'be': 'e', 'bi': 'i', 'bo': 'o', 'bu': 'u', 'bA': 'A', 'bE': 'E', 'bI': 'I', 'bO': 'O',
        'b@': '@', 'b3': '3', 'b1': '1', 'b&': '&', 'b6': '6', 'b8': '8', 'b9': '9', 'bQ': 'Q',

        'ac': '-', 'ec': '-', 'ic': '-', 'oc': '-', 'uc': '-', 'Ac': '-', 'Ec': '-', 'Ic': '-', 'Oc': '-',
        '@c': '-', '3c': '-', '1c': '-', '&c': '-', '6c': '-', '8c': '-', '9c': '-', 'Qc': '-',
        'ca': 'a', 'ce': 'e', 'ci': 'i', 'co': 'o', 'cu': 'u', 'cA': 'A', 'cE': 'E', 'cI': 'I', 'cO': 'O',
        'c@': '@', 'c3': '3', 'c1': '1', 'c&': '&', 'c6': '6', 'c8': '8', 'c9': '9', 'cQ': 'Q',

        'ad': '-', 'ed': '-', 'id': '-', 'od': '-', 'ud': '-', 'Ad': '-', 'Ed': '-', 'Id': '-', 'Od': '-',
        '@d': '-', '3d': '-', '1d': '-', '&d': '-', '6d': '-', '8d': '-', '9d': '-', 'Qd': '-',
        'da': 'a', 'de': 'e', 'di': 'i', 'do': 'o', 'du': 'u', 'dA': 'A', 'dE': 'E', 'dI': 'I', 'dO': 'O',
        'd@': '@', 'd3': '3', 'd1': '1', 'd&': '&', 'd6': '6', 'd8': '8', 'd9': '9', 'dQ': 'Q',

        'af': '-', 'ef': '-', 'if': '-', 'of': '-', 'uf': '-', 'Af': '-', 'Ef': '-', 'If': '-', 'Of': '-',
        '@f': '-', '3f': '-', '1f': '-', '&f': '-', '6f': '-', '8f': '-', '9f': '-', 'Qf': '-',
        'fa': 'a', 'fe': 'e', 'fi': 'i', 'fo': 'o', 'fu': 'u', 'fA': 'A', 'fE': 'E', 'fI': 'I', 'fO': 'O',
        'f@': '@', 'f3': '3', 'f1': '1', 'f&': '&', 'f6': '6', 'f8': '8', 'f9': '9', 'fQ': 'Q',

        'ag': '-', 'eg': '-', 'ig': '-', 'og': '-', 'ug': '-', 'Ag': '-', 'Eg': '-', 'Ig': '-', 'Og': '-',
        '@g': '-', '3g': '-', '1g': '-', '&g': '-', '6g': '-', '8g': '-', '9g': '-', 'Qg': '-',
        'ga': 'a', 'ge': 'e', 'gi': 'i', 'go': 'o', 'gu': 'u', 'gA': 'A', 'gE': 'E', 'gI': 'I', 'gO': 'O',
        'g@': '@', 'g3': '3', 'g1': '1', 'g&': '&', 'g6': '6', 'g8': '8', 'g9': '9', 'gQ': 'Q',

        'ah': '-', 'eh': '-', 'ih': '-', 'oh': '-', 'uh': '-', 'Ah': '-', 'Eh': '-', 'Ih': '-', 'Oh': '-',
        '@h': '-', '3h': '-', '1h': '-', '&h': '-', '6h': '-', '8h': '-', '9h': '-', 'Qh': '-',
        'ha': 'a', 'he': 'e', 'hi': 'i', 'ho': 'o', 'hu': 'u', 'hA': 'A', 'hE': 'E', 'hI': 'I', 'hO': 'O',
        'h@': '@', 'h3': '3', 'h1': '1', 'h&': '&', 'h6': '6', 'h8': '8', 'h9': '9', 'hQ': 'Q',

        'aj': '-', 'ej': '-', 'ij': '-', 'oj': '-', 'uj': '-', 'Aj': '-', 'Ej': '-', 'Ij': '-', 'Oj': '-',
        '@j': '-', '3j': '-', '1j': '-', '&j': '-', '6j': '-', '8j': '-', '9j': '-', 'Qj': '-',
        'ja': 'a', 'je': 'e', 'ji': 'i', 'jo': 'o', 'ju': 'u', 'jA': 'A', 'jE': 'E', 'jI': 'I', 'jO': 'O',
        'j@': '@', 'j3': '3', 'j1': '1', 'j&': '&', 'j6': '6', 'j8': '8', 'j9': '9', 'jQ': 'Q',

        'ak': '-', 'ek': '-', 'ik': '-', 'ok': '-', 'uk': '-', 'Ak': '-', 'Ek': '-', 'Ik': '-', 'Ok': '-',
        '@k': '-', '3k': '-', '1k': '-', '&k': '-', '6k': '-', '8k': '-', '9k': '-', 'Qk': '-',
        'ka': 'a', 'ke': 'e', 'ki': 'i', 'ko': 'o', 'ku': 'u', 'kA': 'A', 'kE': 'E', 'kI': 'I', 'kO': 'O',
        'k@': '@', 'k3': '3', 'k1': '1', 'k&': '&', 'k6': '6', 'k8': '8', 'k9': '9', 'kQ': 'Q',

        'al': '-', 'el': '-', 'il': '-', 'ol': '-', 'ul': '-', 'Al': '-', 'El': '-', 'Il': '-', 'Ol': '-',
        '@l': '-', '3l': '-', '1l': '-', '&l': '-', '6l': '-', '8l': '-', '9l': '-', 'Ql': '-',
        'la': 'a', 'le': 'e', 'li': 'i', 'lo': 'o', 'lu': 'u', 'lA': 'A', 'lE': 'E', 'lI': 'I', 'lO': 'O',
        'l@': '@', 'l3': '3', 'l1': '1', 'l&': '&', 'l6': '6', 'l8': '8', 'l9': '9', 'lQ': 'Q',

        'am': '-', 'em': '-', 'im': '-', 'om': '-', 'um': '-', 'Am': '-', 'Em': '-', 'Im': '-', 'Om': '-',
        '@m': '-', '3m': '-', '1m': '-', '&m': '-', '6m': '-', '8m': '-', '9m': '-', 'Qm': '-',
        'ma': 'a', 'me': 'e', 'mi': 'i', 'mo': 'o', 'mu': 'u', 'mA': 'A', 'mE': 'E', 'mI': 'I', 'mO': 'O',
        'm@': '@', 'm3': '3', 'm1': '1', 'm&': '&', 'm6': '6', 'm8': '8', 'm9': '9', 'mQ': 'Q',

        'an': '-', 'en': '-', 'in': '-', 'on': '-', 'un': '-', 'An': '-', 'En': '-', 'In': '-', 'On': '-',
        '@n': '-', '3n': '-', '1n': '-', '&n': '-', '6n': '-', '8n': '-', '9n': '-', 'Qn': '-',
        'na': 'a', 'ne': 'e', 'ni': 'i', 'no': 'o', 'nu': 'u', 'nA': 'A', 'nE': 'E', 'nI': 'I', 'nO': 'O',
        'n@': '@', 'n3': '3', 'n1': '1', 'n&': '&', 'n6': '6', 'n8': '8', 'n9': '9', 'nQ': 'Q',

        'ap': '-', 'ep': '-', 'ip': '-', 'op': '-', 'up': '-', 'Ap': '-', 'Ep': '-', 'Ip': '-', 'Op': '-',
        '@p': '-', '3p': '-', '1p': '-', '&p': '-', '6p': '-', '8p': '-', '9p': '-', 'Qp': '-',
        'pa': 'a', 'pe': 'e', 'pi': 'i', 'po': 'o', 'pu': 'u', 'pA': 'A', 'pE': 'E', 'pI': 'I', 'pO': 'O',
        'p@': '@', 'p3': '3', 'p1': '1', 'p&': '&', 'p6': '6', 'p8': '8', 'p9': '9', 'pQ': 'Q',

        'aq': '-', 'eq': '-', 'iq': '-', 'oq': '-', 'uq': '-', 'Aq': '-', 'Eq': '-', 'Iq': '-', 'Oq': '-',
        '@q': '-', '3q': '-', '1q': '-', '&q': '-', '6q': '-', '8q': '-', '9q': '-', 'Qq': '-',
        'qa': 'a', 'qe': 'e', 'qi': 'i', 'qo': 'o', 'qu': 'u', 'qA': 'A', 'qE': 'E', 'qI': 'I', 'qO': 'O',
        'q@': '@', 'q3': '3', 'q1': '1', 'q&': '&', 'q6': '6', 'q8': '8', 'q9': '9', 'qQ': 'Q',

        'ar': '-', 'er': '-', 'ir': '-', 'or': '-', 'ur': '-', 'Ar': '-', 'Er': '-', 'Ir': '-', 'Or': '-',
        '@r': '-', '3r': '-', '1r': '-', '&r': '-', '6r': '-', '8r': '-', '9r': '-', 'Qr': '-',
        'ra': 'a', 're': 'e', 'ri': 'i', 'ro': 'o', 'ru': 'u', 'rA': 'A', 'rE': 'E', 'rI': 'I', 'rO': 'O',
        'r@': '@', 'r3': '3', 'r1': '1', 'r&': '&', 'r6': '6', 'r8': '8', 'r9': '9', 'rQ': 'Q',

        'as': '-', 'es': '-', 'is': '-', 'os': '-', 'us': '-', 'As': '-', 'Es': '-', 'Is': '-', 'Os': '-',
        '@s': '-', '3s': '-', '1s': '-', '&s': '-', '6s': '-', '8s': '-', '9s': '-', 'Qs': '-',
        'sa': 'a', 'se': 'e', 'si': 'i', 'so': 'o', 'su': 'u', 'sA': 'A', 'sE': 'E', 'sI': 'I', 'sO': 'O',
        's@': '@', 's3': '3', 's1': '1', 's&': '&', 's6': '6', 's8': '8', 's9': '9', 'sQ': 'Q',

        'at': '-', 'et': '-', 'it': '-', 'ot': '-', 'ut': '-', 'At': '-', 'Et': '-', 'It': '-', 'Ot': '-',
        '@t': '-', '3t': '-', '1t': '-', '&t': '-', '6t': '-', '8t': '-', '9t': '-', 'Qt': '-',
        'ta': 'a', 'te': 'e', 'ti': 'i', 'to': 'o', 'tu': 'u', 'tA': 'A', 'tE': 'E', 'tI': 'I', 'tO': 'O',
        't@': '@', 't3': '3', 't1': '1', 't&': '&', 't6': '6', 't8': '8', 't9': '9', 'tQ': 'Q',

        'av': '-', 'ev': '-', 'iv': '-', 'ov': '-', 'uv': '-', 'Av': '-', 'Ev': '-', 'Iv': '-', 'Ov': '-',
        '@v': '-', '3v': '-', '1v': '-', '&v': '-', '6v': '-', '8v': '-', '9v': '-', 'Qv': '-',
        'va': 'a', 've': 'e', 'vi': 'i', 'vo': 'o', 'vu': 'u', 'vA': 'A', 'vE': 'E', 'vI': 'I', 'vO': 'O',
        'v@': '@', 'v3': '3', 'v1': '1', 'v&': '&', 'v6': '6', 'v8': '8', 'v9': '9', 'vQ': 'Q',

        'ax': '-', 'ex': '-', 'ix': '-', 'ox': '-', 'ux': '-', 'Ax': '-', 'Ex': '-', 'Ix': '-', 'Ox': '-',
        '@x': '-', '3x': '-', '1x': '-', '&x': '-', '6x': '-', '8x': '-', '9x': '-', 'Qx': '-',
        'xa': 'a', 'xe': 'e', 'xi': 'i', 'xo': 'o', 'xu': 'u', 'xA': 'A', 'xE': 'E', 'xI': 'I', 'xO': 'O',
        'x@': '@', 'x3': '3', 'x1': '1', 'x&': '&', 'x6': '6', 'x8': '8', 'x9': '9', 'xQ': 'Q',

        'az': '-', 'ez': '-', 'iz': '-', 'oz': '-', 'uz': '-', 'Az': '-', 'Ez': '-', 'Iz': '-', 'Oz': '-',
        '@z': '-', '3z': '-', '1z': '-', '&z': '-', '6z': '-', '8z': '-', '9z': '-', 'Qz': '-',
        'za': 'a', 'ze': 'e', 'zi': 'i', 'zo': 'o', 'zu': 'u', 'zA': 'A', 'zE': 'E', 'zI': 'I', 'zO': 'O',
        'z@': '@', 'z3': '3', 'z1': '1', 'z&': '&', 'z6': '6', 'z8': '8', 'z9': '9', 'zQ': 'Q',

        'aw': '-', 'ew': '-', 'iw': '-', 'ow': '-', 'uw': '-', 'Aw': '-', 'Ew': '-', 'Iw': '-', 'Ow': '-',
        '@w': '-', '3w': '-', '1w': '-', '&w': '-', '6w': '-', '8w': '-', '9w': '-', 'Qw': '-',
        'wa': 'a', 'we': 'e', 'wi': 'i', 'wo': 'o', 'wu': 'u', 'wA': 'A', 'wE': 'E', 'wI': 'I', 'wO': 'O',
        'w@': '@', 'w3': '3', 'w1': '1', 'w&': '&', 'w6': '6', 'w8': '8', 'w9': '9', 'wQ': 'Q',

        'ay': '-', 'ey': '-', 'iy': '-', 'oy': '-', 'uy': '-', 'Ay': '-', 'Ey': '-', 'Iy': '-', 'Oy': '-',
        '@y': '-', '3y': '-', '1y': '-', '&y': '-', '6y': '-', '8y': '-', '9y': '-', 'Qy': '-',
        'ya': 'a', 'ye': 'e', 'yi': 'i', 'yo': 'o', 'yu': 'u', 'yA': 'A', 'yE': 'E', 'yI': 'I', 'yO': 'O',
        'y@': '@', 'y3': '3', 'y1': '1', 'y&': '&', 'y6': '6', 'y8': '8', 'y9': '9', 'yQ': 'Q',

        # dh = there
        'dha': 'a', 'dhe': 'e', 'dhi': 'i', 'dho': 'o', 'dhu': 'u', 'dhA': 'A', 'dhE': 'E', 'dhI': 'I', 'dhO': 'O',
        'dh@': '@', 'dh3': '3', 'dh1': '1', 'dh&': '&', 'dh6': '6', 'dh8': '8', 'dh9': '9', 'dhQ': 'Q',
        'adh': '-', 'edh': '-', 'idh': '-', 'odh': '-', 'udh': '-', 'Adh': '-', 'Edh': '-', 'Idh': '-', 'Odh': '-',
        '@dh': '-', '3dh': '-', '1dh': '-', '&dh': '-', '6dh': '-', '8dh': '-', '9dh': '-', 'Qdh': '-',

        # th = wrat
        'tha': 'a', 'the': 'e', 'thi': 'i', 'tho': 'o', 'thu': 'u', 'thA': 'A', 'thE': 'E', 'thI': 'I', 'thO': 'O',
        'th@': '@', 'th3': '3', 'th1': '1', 'th&': '&', 'th6': '6', 'th8': '8', 'th9': '9', 'thQ': 'Q',
        'ath': '-', 'eth': '-', 'ith': '-', 'oth': '-', 'uth': '-', 'Ath': '-', 'Eth': '-', 'Ith': '-', 'Oth': '-',
        '@th': '-', '3th': '-', '1th': '-', '&th': '-', '6th': '-', '8th': '-', '9th': '-', 'Qth': '-',

        # zh = azur
        'zha': 'a', 'zhe': 'e', 'zhi': 'i', 'zho': 'o', 'zhu': 'u', 'zhA': 'A', 'zhE': 'E', 'zhI': 'I', 'zhO': 'O',
        'zh@': '@', 'zh3': '3', 'zh1': '1', 'zh&': '&', 'zh6': '6', 'zh8': '8', 'zh9': '9', 'zhQ': 'Q',
        'azh': '-', 'ezh': '-', 'izh': '-', 'ozh': '-', 'uzh': '-', 'Azh': '-', 'Ezh': '-', 'Izh': '-', 'Ozh': '-',
        '@zh': '-', '3zh': '-', '1zh': '-', '&zh': '-', '6zh': '-', '8zh': '-', '9zh': '-', 'Qzh': '-',

        '-': '-', 'R': '-'
    }

    _consonants = [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p',
        'q', 'r', 's', 't', 'v', 'x', 'z', 'w', 'y', 'dh', 'th', 'zh'
    ]

    @classmethod
    def _gen_charset_from_line_helper(cls, line: str):
        next_from_charset = ''

        for i, c in enumerate(line):
            logger.debug(f"--------------")
            logger.debug(f"current: {next_from_charset}")
            logger.debug(f"newchar: {c}")

            if c in cls._as_valid or c == 'R':
                if next_from_charset:
                    logger.debug(f"out:{next_from_charset}")
                    yield next_from_charset

                logger.debug(f"out:{c}")
                yield c
                next_from_charset = ''
                continue

            if not next_from_charset:
                next_from_charset += c
                continue

            # New character is a consonant
            if c in cls._consonants:
                logger.debug(f"consonant")

                # Last character was a consonant
                if next_from_charset[-1] in cls._consonants:
                    logger.debug(f"prev=consonant")

                    if next_from_charset+c in cls._charset:
                        logger.debug(f"out:{next_from_charset+c}")
                        yield next_from_charset+c
                        next_from_charset = ''
                        continue

                    elif i < len(line)-1 and line[i+1] not in cls._consonants:
                        if next_from_charset+c+line[i+1] in cls._charset:
                            next_from_charset += c
                            continue

                    logger.debug(f"out:{next_from_charset}")
                    yield next_from_charset
                    next_from_charset = c
                    continue

                # Last character was a vowel
                else:
                    logger.debug(f"prev=vowel")

                    if i < len(line)-1 and line[i+1] in cls._consonants:
                        if next_from_charset+c+line[i+1] in cls._charset:
                            next_from_charset += c
                            continue

                    logger.debug(f"out:{next_from_charset+c}")
                    yield next_from_charset+c
                    next_from_charset = ''
                    continue

            # New character is a vowel
            else:
                logger.debug(f"vowel")

                if next_from_charset+c in cls._charset:
                    logger.debug(f"out:{next_from_charset+c}")
                    yield next_from_charset+c
                    next_from_charset = ''
                    continue

                else:
                    logger.debug(f"out:{next_from_charset}")
                    yield next_from_charset
                    next_from_charset = c
                    continue

        if next_from_charset:
            logger.debug(f"--------------")
            logger.debug(f"leftovers")
            logger.debug(f"out:{next_from_charset}")
            yield next_from_charset

        return
