from typing import List
from enum import Enum

Vibrato = Enum('Vibrato', 'Default, Strong, Weak')


class Pitches():
    def __init__(self, pbtype: int = 5, pitches: List[int] = [0]*179):
        self._pbtype = pbtype
        self._pitches = pitches

    @property
    def pbtype(self):
        return self._pbtype

    @property
    def pitches(self):
        return self._pitches


class PitchBend():
    def __init__(self, pbtype: int = 5, pbstart: float = -300, pitchbend: List[int] = [0]*114):
        self._pbtype = pbtype
        self._pbstart = pbstart
        self._pitchbend = pitchbend

    @property
    def pbtype(self):
        return self._pbtype

    @property
    def pbstart(self):
        return self._pbstart

    @property
    def pitchbend(self):
        return self._pitchbend


class Portamento():
    Position = Enum('Position', 'Middle Left Right')

    def __init__(self,  width_ms: List[float] = [], start_ms: List[float] = [], amplitude: List[float] = []):
        self._pbw = width_ms
        self._pbs = start_ms
        self._pby = amplitude

    def set_start(self, start: Position = Position.Middle):
        width = sum(self._pbw) / len(self._pbw)
        if start == self.Position.Middle:
            self._pbs = -width/2.0
        elif start == self.Position.Left:
            self._pbs = -width
        elif start == self.Position.Right:
            self._pbs = 0
        else:
            raise ValueError(f"unrecognized starting position: {start}")

    @property
    def pbw(self):
        return self._pbw

    @property
    def pbs(self):
        return self._pbs

    @property
    def pby(self):
        return self._pby


class Tuning():
    def __init__(self,
                 pitch_bend: PitchBend = None,
                 portamento: Portamento = None,
                 pitches: Pitches = None,
                 pbm: str = '', vbr: List[float] = [],
                 envelope: List[float] = [0, 0, 35, 0, 100, 100, 0]
                 ):
        self._pitch_bend = pitch_bend
        self._portamento = portamento
        self._pbm = pbm
        self._vbr = vbr
        self._envelope = envelope
        self._pitches = pitches

    def set_envelope_params(self,
                            p1: float = 0, v1: float = 0,
                            p2: float = 0, v2: float = 100,
                            p3: float = 35, v3: float = 100,
                            p4: float = 0, v4: float = 0,
                            p5: float = 0, v5: float = 0
                            ):
        self._envelope = [p1, p2, p3, v1, v2, v3, v4, '%', p4, p5, v5]

    def set_vibrato_params(self,
                           length_percentage: float = 65,
                           cycle_ms: float = 180,
                           depth_cents: float = 35,
                           in_percentage: float = 20,
                           out_percentage: float = 20,
                           phase_percentage: float = 0,
                           pitch_percentage: float = 0,
                           magic_value: float = 0,
                           ):
        self._vbr = [
            length_percentage, cycle_ms, depth_cents,
            in_percentage, out_percentage, phase_percentage,
            pitch_percentage, magic_value
        ]

    def set_vibrato(self, vibrato_type: Vibrato = Vibrato.Default):
        if vibrato_type == Vibrato.Default:
            self._vbr = [65, 180, 35, 20, 20, 0, 0, 0]
        elif vibrato_type == Vibrato.Strong:
            self._vbr = [65, 210, 55, 20, 20, 0, 0, 200]
        elif vibrato_type == Vibrato.Weak:
            self._vbr = [65, 165, 20, 20, 20, 0, 0, 50]
        else:
            raise ValueError(f"unrecognized vibrato type: {vibrato_type}")

    @property
    def pbm(self):
        return self._pbm

    @property
    def portamento(self):
        return self._portamento

    @property
    def vbr(self):
        return self._vbr

    @property
    def envelope(self):
        return self._envelope

    @property
    def pitch_bend(self):
        return self._pitch_bend

    @property
    def pitches(self):
        return self._pitches
