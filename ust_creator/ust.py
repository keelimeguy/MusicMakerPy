from typing import List

from .language.hiragana import Hiragana
from .language.language import Language
from .voice import Voice, VoiceType
from .lyric import Lyric


class UST:
    def __init__(self, project_name: str, wav_filename: str, voice: Voice,
                 tempo: float = 100.0, flags: str = ''):
        self._project_name = project_name
        self._wav_filename = wav_filename
        self._voice = voice
        self._tempo = tempo
        self._flags = flags

        self._lyric_number = 0
        self._last_lyric_value = '-'

    def write(self, file, lyrics: List[Lyric], language: Language = Hiragana):
        self._write_section_version(file)
        self._write_section_setting(file)

        self._begin_section_lyric()
        for lyric in lyrics:
            self._add_lyric(file, lyric, language=language)
        self._end_section_lyric(file)

    def _write_line(self, file, line: str):
        file.write(f"""
{line}""".encode('shift-jis'))

    def _write_section_version(self, file):
        file.write("""[#VERSION]
UST Version1.2
""".encode('shift-jis'))

    def _write_section_setting(self, file):
        file.write(f"""[#SETTING]
Tempo={self._tempo:.2f}
Tracks=1
ProjectName={self._project_name}
VoiceDir={self._voice.directory}
OutFile={self._wav_filename}
CacheDir={''.join(self._wav_filename.split('.')[:-1])}.cache
Tool1=wavtool.exe
Tool2=resampler.exe
Mode2=True""".encode('shift-jis'))

        if self._flags:
            self._write_line(file, f"Flags={self._flags}")

    def _begin_section_lyric(self):
        self._lyric_number = 0
        self._last_lyric_value = '-'

    def _add_lyric(self, file, lyric: Lyric, language: Language = Hiragana):  # noqa: C901
        file.write(f"""
[#{self._lyric_number:04}]
Length={lyric.length}""".encode('shift-jis'))

        if self._voice.voice_type == VoiceType.CV:
            self._write_line(file, f"Lyric={lyric.value}")

        elif self._voice.voice_type == VoiceType.VCV:
            self._write_line(file, f"Lyric={language.get_suffix_lookup()[self._last_lyric_value]} {lyric.value}")

        elif self._voice.voice_type == VoiceType.CVVC:
            raise NotImplementedError(f"VoiceType not implemented: {self._voice.voice_type.name}")

        elif self._voice.voice_type == VoiceType.VCCV:
            raise NotImplementedError(f"VoiceType not implemented: {self._voice.voice_type.name}")

        self._last_lyric_value = lyric.value

        file.write(f"""
NoteNum={lyric.note.value}
Intensity={lyric.note.intensity_percentage}
Modulation={lyric.note.modulation_percentage}""".encode('shift-jis'))

        if lyric.note.tuning.pitch_bend:
            self._write_line(file, f"PBType={lyric.note.tuning.pitch_bend.pbtype}")
            self._write_line(file, f"PBStart={lyric.note.tuning.pitch_bend.pbstart}")
            self._write_line(file, f"PitchBend={','.join([str(i) for i in lyric.note.tuning.pitch_bend.pitchbend])}")

        elif lyric.note.tuning.pitches:
            self._write_line(file, f"PBType={lyric.note.tuning.pitches.pbtype}")
            self._write_line(file, f"Pitches={','.join([str(i) for i in lyric.note.tuning.pitches.pitches])}")

        if lyric.note.tuning.portamento:
            self._write_line(file, f"PBW={','.join([str(i) for i in lyric.note.tuning.portamento.pbw])}")
            self._write_line(file, f"PBS={';'.join([str(i) for i in lyric.note.tuning.portamento.pbs])}")
            self._write_line(file, f"PBY={','.join([str(i) for i in lyric.note.tuning.portamento.pby])}")

        if lyric.note.pre_utterance_ms:
            self._write_line(file, f"PreUtterance={lyric.note.pre_utterance_ms}")
        if lyric.note.voice_overlap_ms:
            self._write_line(file, f"VoiceOverlap={lyric.note.voice_overlap_ms}")

        if lyric.note.tuning.pbm:
            self._write_line(file, f"PBM={lyric.note.tuning.pbm}")
        if lyric.note.consonant_velocity:
            self._write_line(file, f"Velocity={lyric.note.consonant_velocity}")
        if lyric.note.start_point:
            self._write_line(file, f"StartPoint={lyric.note.start_point}")

        self._write_line(file, f"Envelope={','.join([str(i) for i in lyric.note.tuning.envelope])}")

        if lyric.note.tuning.vbr:
            self._write_line(file, f"VBR={','.join([str(i) for i in lyric.note.tuning.vbr])}")
        if lyric.note.tempo:
            self._write_line(file, f"Tempo={lyric.note.tempo:.2f}")

        self._lyric_number += 1

    def _end_section_lyric(self, file):
        self._write_line(file, """[#TRACKEND]
""")
