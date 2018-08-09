# Based on https://github.com/campagnola/pyabc/blob/master/pyabc.py

import sys
import re

from musicmaker.theory.scale import Scale
from musicmaker.theory.pitch import Pitch
from musicmaker.theory.staff import Staff

# Information field table copied from
# http://abcnotation.com/wiki/abc:standard:v2.1#abc_files_tunes_and_fragments
# Columns are:
# X:Field, file header, tune header, tune body, inline, type
information_field_table = """
A:area              yes     yes     no      no      string
B:book              yes     yes     no      no      string
C:composer          yes     yes     no      no      string
D:discography       yes     yes     no      no      string
F:file url          yes     yes     no      no      string
G:group             yes     yes     no      no      string
H:history           yes     yes     no      no      string
I:instruction       yes     yes     yes     yes     instruction
K:key               no      yes     yes     yes     instruction
L:unit note length  yes     yes     yes     yes     instruction
M:meter             yes     yes     yes     yes     instruction
m:macro             yes     yes     yes     yes     instruction
N:notes             yes     yes     yes     yes     string
O:origin            yes     yes     no      no      string
P:parts             no      yes     yes     yes     instruction
Q:tempo             no      yes     yes     yes     instruction
R:rhythm            yes     yes     yes     yes     string
r:remark            yes     yes     yes     yes     -
S:source            yes     yes     no      no      string
s:symbol line       no      no      yes     no      instruction
T:tune title        no      yes     yes     no      string
U:user defined      yes     yes     yes     yes     instruction
V:voice             no      yes     yes     yes     instruction
W:words             no      yes     yes     no      string
w:words             no      no      yes     no      string
X:reference number  no      yes     no      no      instruction
Z:transcription     yes     yes     no      no      string
"""

class InfoKey(object):
    def __init__(self, key, name, file_header, tune_header, tune_body, inline, type):
        self.key = key
        self.name = name.strip()
        self.file_header = file_header=='yes'
        self.tune_header = tune_header=='yes'
        self.tune_body = tune_body=='yes'
        self.inline = inline=='yes'
        self.type = type.strip()

# parse info field table
info_keys = {}
for line in information_field_table.split('\n'):
    if line.strip() == '':
        continue
    key = line[0]
    fields = re.match(r'(.*)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+(.*)', line[2:]).groups()
    info_keys[key] = InfoKey(key, *fields)

file_header_fields = {k:v for k,v in info_keys.items() if v.file_header}
tune_header_fields = {k:v for k,v in info_keys.items() if v.tune_header}
tune_body_fields = {k:v for k,v in info_keys.items() if v.tune_body}
inline_fields = {k:v for k,v in info_keys.items() if v.inline}

# Decoration symbols from
# http://abcnotation.com/wiki/abc:standard:v2.1#decorations
symbols = """
!trill!                "tr" (trill mark)
!trill(!               start of an extended trill
!trill)!               end of an extended trill
!lowermordent!         short /|/|/ squiggle with a vertical line through it
!uppermordent!         short /|/|/ squiggle
!mordent!              same as !lowermordent!
!pralltriller!         same as !uppermordent!
!roll!                 a roll mark (arc) as used in Irish music
!turn!                 a turn mark (also known as gruppetto)
!turnx!                a turn mark with a line through it
!invertedturn!         an inverted turn mark
!invertedturnx!        an inverted turn mark with a line through it
!arpeggio!             vertical squiggle
!>!                    > mark
!accent!               same as !>!
!emphasis!             same as !>!
!fermata!              fermata or hold (arc above dot)
!invertedfermata!      upside down fermata
!tenuto!               horizontal line to indicate holding note for full duration
!0! - !5!              fingerings
!+!                    left-hand pizzicato, or rasp for French horns
!plus!                 same as !+!
!snap!                 snap-pizzicato mark, visually similar to !thumb!
!slide!                slide up to a note, visually similar to a half slur
!wedge!                small filled-in wedge mark
!upbow!                V mark
!downbow!              squared n mark
!open!                 small circle above note indicating open string or harmonic
!thumb!                cello thumb symbol
!breath!               a breath mark (apostrophe-like) after note
!pppp! !ppp! !pp! !p!  dynamics marks
!mp! !mf! !f! !ff!     more dynamics marks
!fff! !ffff! !sfz!     more dynamics marks
!crescendo(!           start of a < crescendo mark
!<(!                   same as !crescendo(!
!crescendo)!           end of a < crescendo mark, placed after the last note
!<)!                   same as !crescendo)!
!diminuendo(!          start of a > diminuendo mark
!>(!                   same as !diminuendo(!
!diminuendo)!          end of a > diminuendo mark, placed after the last note
!>)!                   same as !diminuendo)!
!segno!                2 ornate s-like symbols separated by a diagonal line
!coda!                 a ring with a cross in it
!D.S.!                 the letters D.S. (=Da Segno)
!D.C.!                 the letters D.C. (=either Da Coda or Da Capo)
!dacoda!               the word "Da" followed by a Coda sign
!dacapo!               the words "Da Capo"
!fine!                 the word "fine"
!shortphrase!          vertical line on the upper part of the staff
!mediumphrase!         same, but extending down to the centre line
!longphrase!           same, but extending 3/4 of the way down
"""

class Token(object):
    def __init__(self, line, char, text):
        self._line = line
        self._char = char
        self._text = text

    def __repr__(self):
        return "<%s \"%s\">" % (self.__class__.__name__, self._text)

class Note(Token):
    def __init__(self, key, time, note, accidental, octave, num, denom, **kwds):
        Token.__init__(self, **kwds)
        self.key = key
        self.time_sig = time
        self.note = note
        self.accidental = accidental
        self.octave = octave
        self._length = (num, denom)

        acc = ''
        if accidental:
            acc = accidental
            acc.replace('^', '#')
            acc.replace('_', 'b')
            acc.replace('=', '')
        else:
            accidentals = key.accidentals
            if note.upper() in accidentals:
                acc = accidentals[note.upper()]
        self.name = note.upper()+acc

    @property
    def pitch(self):
        return Pitch(self.name, self.octave+4)

    @property
    def length(self):
        n,d = self._length
        return (int(n) if n is not None else 1, int(d) if d is not None else 1)

    @property
    def duration(self):
        return self.length[0] / self.length[1]

    def dotify(self, dots, direction):
        """Apply dot(s) to the duration of this note.
        """
        assert direction in ('left', 'right')
        longer = direction == 'left'
        if '<' in dots:
            longer = not longer
        n_dots = len(dots)
        num, den = self.length
        if longer:
            num = num * 2 + 1
            den = den * 2
            self._length = (num, den)
        else:
            den = den * 2
            self._length = (num, den)

class Beam(Token):
    pass

class Space(Token):
    pass

class Slur(Token):
    """   ( or )   """
    pass

class Tie(Token):
    """   -   """
    pass

class Newline(Token):
    pass

class Continuation(Token):
    """  \ at end of line  """
    pass

class GracenoteBrace(Token):
    """  {  {/  or }  """
    pass

class ChordBracket(Token):
    """  [  or  ]  """
    pass

class ChordSymbol(Token):
    """   "Amaj"   """
    pass

class Annotation(Token):
    """    "<stuff"   """
    pass

class Decoration(Token):
    """  .~HLMOPSTuv  """
    pass

class Tuplet(Token):
    """  (5   """
    def __init__(self, num, **kwds):
        Token.__init__(self, **kwds)
        self.num = num

class BodyField(Token):
    pass

class InlineField(Token):
    pass

class Rest(Token):
    def __init__(self, symbol, num, denom, **kwds):
        # char==X or Z means length is in measures
        Token.__init__(self, **kwds)
        self.symbol = symbol
        self.length = (num, denom)

# map mode names relative to Ionian (in chromatic steps)
mode_values = {'major': 0, 'minor': 3, 'ionian': 0, 'aeolian': 3,
               'mixolydian': -7, 'dorian': -2, 'phrygian': -4, 'lydian': -5,
               'locrian': 1}

# mode name normalization
mode_abbrev = {m[:3]: m for m in mode_values}

# sharps/flats in ionian keys
key_sig = {'C#': 7, 'F#': 6, 'B': 5, 'E': 4, 'A': 3, 'D': 2, 'G': 1, 'C': 0,
           'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7}
sharp_order = "FCGDAEB"
flat_order = "BEADGCF"

class Key(Scale):
    def __init__(self, name=None, root=None, mode=None):
        if name is not None:
            assert root is None and mode is None
            root, mode = self.parse_key(name)
        self.mode_name = mode[0].upper()+mode[1:]
        Scale.__init__(self, root, self.mode_name)

    def parse_key(self, name):
        # highland pipe keys
        if key in ['HP', 'Hp']:
            return 'G', 'Lydian'

        m = re.match(r'([A-G])(\#|b)?\s*(\w+)?(.*)', name)
        if m is None:
            raise ValueError('Invalid key "%s"' % name)
        base, acc, mode, extra = m.groups()
        if acc is None:
            acc = ''
        if mode is None:
            mode = 'major'
        try:
            mode = mode_abbrev[mode[:3].lower()]
        except KeyError:
            raise ValueError("Unrecognized key signature %s" % name)
        mode = mode[0].upper()+mode[1:]
        return base+acc, mode

    @property
    def key_signature(self):
        """
        List of accidentals that should be displayed in the key
        signature for the given key description.
        """
        # determine number of sharps/flats for this key by first converting
        # to ionian, then doing the key lookup
        key = self.relative_ionian
        num_acc = key_sig[key.root.name]
        sig = []
        # sharps or flats?
        if num_acc > 0:
            for i in range(num_acc):
                sig.append(sharp_order[i] + '#')
        else:
            for i in range(-num_acc):
                sig.append(flat_order[i] + 'b')
        return sig

    @property
    def accidentals(self):
        """A dictionary of accidentals in the key signature.
        """
        return {p:a for p,a in self.key_signature}

    @property
    def relative_ionian(self):
        """
        Return the ionian mode relative to the given key and mode.
        """
        key, mode = self.root, self.mode_name.lower()
        rel = mode_values[mode]
        root = key.transpose(rel)

        # Select flat or sharp to match the current key name
        if '#' in key.name:
            root2 = root.sharp_normal()
            if len(root2.name) == 2:
                root = root2
        elif 'b' in key.name:
            root2 = root.normal()
            if len(root2.name) == 2:
                root = root2

        return Key(root=root, mode='ionian')


class AbcStaff(Staff):
    def __init__(self, abc):
        Staff.__init__(self)
        self.parse(abc)

    def parse(self, abc):
        self.abc = abc
        header = []
        tune = []
        in_tune = False
        for line in abc.split('\n'):
            line = re.split(r'([^\\]|^)%', line)[0]
            line = line.strip()
            if line == '':
                continue
            if in_tune:
                tune.append(line)
            else:
                if line[0] in info_keys and line[1] == ':':
                    header.append(line)
                    if line[0] == 'K':
                        in_tune = True
                elif line[:2] == '+:':
                    header[-1] += ' ' + line[2:]
        self.parse_header(header)
        self.parse_tune(tune)

        in_chord = False
        notes = []
        length = 0
        for token in self.tokens:
            if isinstance(token, ChordBracket):
                in_chord = not in_chord
            elif isinstance(token, Note):
                notes.append(token.pitch)
                length = token.length
                length = length[0]/length[1]
            if not in_chord and len(notes) > 0:
                self.add(notes, length)
                notes = []

    def parse_header(self, header):
        h = {}
        for line in header:
            key = line[0]
            data = line[2:].strip()
            h[info_keys[key].name] = data
        self.header = h
        self.reference = h['reference number']
        self.title = h['tune title']
        self.key = h['key']

    def parse_tune(self, tune):
        self.tokens = self.tokenize(tune, self.header)

    def tokenize(self, tune, header):
        # get initial key signature from header
        key = Key(self.header['key'])

        # get initial time signature from header
        meter = self.header.get('meter', 'free')
        if meter != 'free':
            meter = meter.split('/')
            self.meter_beats = float(meter[0])
            self.meter_base = float(meter[1])

        self.unit = self.header.get('unit note length', None)
        # determine default unit note length from meter if possible
        if self.unit is None and meter != 'free':
            if self.meter_beats / self.meter_base < 0.75:
                self.unit = 1/16
            else:
                self.unit = 1/8
        else:
            self.unit = eval(self.unit)

        tempo = self.header.get('tempo', None)
        if tempo:
            self.tempo = tempo

        tokens = []
        for i,line in enumerate(tune):
            line = line.rstrip()

            if len(line) > 2 and line[1] == ':' and (line[0] == '+' or line[0] in tune_body_fields):
                tokens.append(BodyField(line=i, char=0, text=line))
                continue

            pending_dots = None
            j = 0
            while j < len(line):
                part = line[j:]

                # Field
                if part[0] == '[' and len(part) > 3 and part[2] == ':':
                    fields = ''.join(inline_fields.keys())
                    m = re.match(r'\[[%s]:([^\]]+)\]' % fields, part)
                    if m is not None:
                        if m.group()[1] == 'K':
                            key = Key(m.group()[3:-1])

                        tokens.append(InlineField(line=i, char=j, text=m.group()))
                        j += m.end()
                        continue

                # Space
                m = re.match(r'(\s+)', part)
                if m is not None:
                    tokens.append(Space(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Note
                # Examples:  c  E'  _F2  ^^G,/4  =a,',3/2
                m = re.match(r"(?P<acc>\^|\^\^|=|_|__)?(?P<note>[a-gA-G])(?P<oct>[,']*)(?P<num>\d+)?(?P<slash>/+)?(?P<den>\d+)?", part)
                if m is not None:
                    g = m.groupdict()
                    octave = int(g['note'].islower())
                    if g['oct'] is not None:
                        octave -= g['oct'].count(",")
                        octave += g['oct'].count("'")

                    num = g.get('num', 1)
                    if g['den'] is not None:
                        denom = g['den']
                    elif g['slash'] is not None:
                        denom = 2 * g['slash'].count('/')
                    else:
                        denom = 1

                    tokens.append(Note(key=key, time=(self.meter_beats, self.meter_base, self.unit, self.tempo), note=g['note'], accidental=g['acc'],
                        octave=octave, num=num, denom=denom, line=i, char=j, text=m.group()))

                    if pending_dots is not None:
                        tokens[-1].dotify(pending_dots, 'right')
                        pending_dots = None

                    j += m.end()
                    continue

                # Beam  |   :|   |:   ||   and Chord  [ABC]
                m = re.match(r'([\[\]\|\:]+)([0-9\-,])?', part)
                if m is not None:
                    if m.group() in '[]':
                        tokens.append(ChordBracket(line=i, char=j, text=m.group()))
                    else:
                        tokens.append(Beam(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Broken rhythm
                if len(tokens) > 0 and isinstance(tokens[-1], (Note, Rest)):
                    m = re.match('<+|>+', part)
                    if m is not None:
                        tokens[-1].dotify(part, 'left')
                        pending_dots = part
                        j += m.end()
                        continue

                # Rest
                m = re.match(r'([XZxz])(\d+)?(/(\d+)?)?', part)
                if m is not None:
                    g = m.groups()
                    tokens.append(Rest(g[0], num=g[1], denom=g[3], line=i, char=j, text=m.group()))

                    if pending_dots is not None:
                        tokens[-1].dotify(pending_dots, 'right')
                        pending_dots = None

                    j += m.end()
                    continue

                # Tuplets  (must parse before slur)
                m = re.match(r'\(([2-9])', part)
                if m is not None:
                    tokens.append(Tuplet(num=m.groups()[0], line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Slur
                if part[0] in '()':
                    tokens.append(Slur(line=i, char=j, text=part[0]))
                    j += 1
                    continue

                # Tie
                if part[0] == '-':
                    tokens.append(Tie(line=i, char=j, text=part[0]))
                    j += 1
                    continue

                # Embelishments
                m = re.match(r'(\{\\?)|\}', part)
                if m is not None:
                    tokens.append(GracenoteBrace(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Decorations (single character)
                if part[0] in '.~HLMOPSTuv':
                    tokens.append(Decoration(line=i, char=j, text=part[0]))
                    j += 1
                    continue

                # Decorations (!symbol!)
                m = re.match(r'\!([^\! ]+)\!', part)
                if m is not None:
                    tokens.append(Decoration(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Continuation
                if j == len(line) - 1 and j == '\\':
                    tokens.append(Continuation(line=i, char=j, text='\\'))
                    j += 1
                    continue

                # Annotation
                m = re.match(r'"[\^\_\<\>\@][^"]+"', part)
                if m is not None:
                    tokens.append(Annotation(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                # Chord symbol
                m = re.match(r'"[\w#/]+"', part)
                if m is not None:
                    tokens.append(ChordSymbol(line=i, char=j, text=m.group()))
                    j += m.end()
                    continue

                raise Exception("Unable to parse: %s\n%s" % (part, self.url))

            if not isinstance(tokens[-1], Continuation):
                tokens.append(Newline(line=i, char=j, text='\n'))

        return tokens


if __name__ == '__main__':
    from musicmaker.sound.staffplayer import StaffPlayer

    abc = \
"""X: 6
T: A Birthday
R: polka
M: 2/4
K: Gmajor
[DG]g eg/e/|dB GF/E/|DF Ac|BG GD-|
Dg eg/e/|dB GF/E/|DF AB/A/|G4||
g2 fe|dB GF/E/|DF Ac|BG GD-|
Dg eg/e/|dB GF/E/|DF AB/A/|G4||
A3d|BG GB|Ad cA|BG GB|
A3d|BG GB|de/d/ cA| AG G2-||
"""

    abc_staff = AbcStaff(abc)

    print(abc)

    print('playing..', flush=True)
    player = StaffPlayer(abc_staff)
    player.play()
