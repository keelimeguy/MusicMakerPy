from musicmaker.theory.pitch import Pitch

from .tuning import Tuning


class Note:
    def __init__(
        self,
        pitch: Pitch,
        tuning: Tuning = Tuning(),
        pre_utterance_ms: int = 0,
        voice_overlap_ms: int = 0,
        start_point: int = 0,
        intensity_percentage: int = 100,
        modulation_percentage: int = 0,
        consonant_velocity: int = 0,
        tempo: float = 0.0,
        bre: int = 50,
        no_formant_filter: bool = False,
    ):
        self._value = pitch.value
        self._tuning = tuning
        self._pre_utterance_ms = pre_utterance_ms
        self._voice_overlap_ms = voice_overlap_ms
        self._start_point = start_point
        self._intensity_percentage = intensity_percentage
        self._modulation_percentage = modulation_percentage
        self._consonant_velocity = consonant_velocity
        self._tempo = tempo
        self._bre = bre
        self._no_formant_filter = no_formant_filter

    def get_flags(self):
        flags = f"B{self._bre}"
        if self._no_formant_filter:
            flags += 'N'
        return flags

    def apply_tuning(self, tuning: Tuning):
        self._tuning = tuning

    @property
    def value(self):
        return self._value

    @property
    def pre_utterance_ms(self):
        return self._pre_utterance_ms

    @property
    def voice_overlap_ms(self):
        return self._voice_overlap_ms

    @property
    def start_point(self):
        return self._start_point

    @property
    def intensity_percentage(self):
        return self._intensity_percentage

    @property
    def modulation_percentage(self):
        return self._modulation_percentage

    @property
    def tuning(self):
        return self._tuning

    @property
    def tempo(self):
        return self._tempo

    @property
    def consonant_velocity(self):
        return self._consonant_velocity
