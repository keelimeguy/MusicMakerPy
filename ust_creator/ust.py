from typing import List

from .voice import Voice, VoiceType
from .lyric import Lyric


class UST:

    _suffix_lookup = {
        'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
        'か': 'a', 'き': 'i', 'く': 'u', 'け': 'e', 'こ': 'o',
        'が': 'a', 'ぎ': 'i', 'ぐ': 'u', 'げ': 'e', 'ご': 'o',
        'さ': 'a', 'し': 'i', 'す': 'u', 'せ': 'e', 'そ': 'o',
        'ざ': 'a', 'じ': 'i', 'ず': 'u', 'ぜ': 'e', 'ぞ': 'o',
        'た': 'a', 'ち': 'i', 'つ': 'u', 'て': 'e', 'と': 'o',
        'だ': 'a', 'ぢ': 'i', 'づ': 'u', 'で': 'e', 'ど': 'o',
        'な': 'a', 'に': 'i', 'ぬ': 'u', 'ね': 'e', 'の': 'o',
        'は': 'a', 'ひ': 'i', 'ふ': 'u', 'へ': 'e', 'ほ': 'o',
        'ば': 'a', 'び': 'i', 'ぶ': 'u', 'べ': 'e', 'ぼ': 'o',
        'ぱ': 'a', 'ぴ': 'i', 'ぷ': 'u', 'ぺ': 'e', 'ぽ': 'o',
        'ま': 'a', 'み': 'i', 'む': 'u', 'め': 'e', 'も': 'o',
        'や': 'a', 'ゆ': 'u', 'よ': 'o',
        'ら': 'a', 'り': 'i', 'る': 'u', 'れ': 'e', 'ろ': 'o',
        'わ': 'a', 'を': 'o', 'ん': '-',
        'きゃ': 'a', 'きゅ': 'u', 'きょ': 'o',
        'ぎゃ': 'a', 'ぎゅ': 'u', 'ぎょ': 'o',
        'しゃ': 'a', 'しゅ': 'u', 'しょ': 'o',
        'じゃ': 'a', 'じゅ': 'u', 'じょ': 'o',
        'ちゃ': 'a', 'ちゅ': 'u', 'ちょ': 'o',
        'ぢゃ': 'a', 'ぢゅ': 'u', 'ぢょ': 'o',
        'にゃ': 'a', 'にゅ': 'u', 'にょ': 'o',
        'ひゃ': 'a', 'ひゅ': 'u', 'ひょ': 'o',
        'びゃ': 'a', 'びゅ': 'u', 'びょ': 'o',
        'ぴゃ': 'a', 'ぴゅ': 'u', 'ぴょ': 'o',
        'みゃ': 'a', 'みゅ': 'u', 'みょ': 'o',
        'りゃ': 'a', 'りゅ': 'u', 'りょ': 'o',
        '-': '-', 'R': '-'
    }

    def __init__(self, project_name: str, wav_filename: str, voice: Voice, tempo: float = 100.0, flags: str = ''):
        self._project_name = project_name
        self._wav_filename = wav_filename
        self._voice = voice
        self._tempo = tempo
        self._flags = flags

        self._lyric_number = 0
        self._last_lyric_value = '-'

    def write(self, file, lyrics: List[Lyric]):
        self._write_section_version(file)
        self._write_section_setting(file)

        self._begin_section_lyric()
        for lyric in lyrics:
            self._add_lyric(file, lyric)
        self._end_section_lyric(file)

    def _write_line(self, file, line: str):
        file.write(f"""
{line}""".encode('shift-jis'))

    def _write_section_version(self, file):
        file.write(f"""[#VERSION]
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

    def _add_lyric(self, file, lyric: Lyric):
        file.write(f"""
[#{self._lyric_number:04}]
Length={lyric.length}""".encode('shift-jis'))

        if self._voice.voice_type == VoiceType.CV:
            self._write_line(file, f"Lyric={lyric.value}")

        elif self._voice.voice_type == VoiceType.VCV:
            self._write_line(file, f"Lyric={self._suffix_lookup[self._last_lyric_value]} {lyric.value}")

        elif self._voice.voice_type == VoiceType.CVVC:
            raise NotImplementedError(f"VoiceType not implemented: {self._voice.voice_type.name}")

        elif self._voice.voice_type == VoiceType.VCCV:
            raise NotImplementedError(f"VoiceType not implemented: {self._voice.voice_type.name}")

        self._last_lyric_value = lyric.value

        file.write(f"""
NoteNum={lyric.note.value}
PreUtterance={lyric.note.pre_utterance_ms}
VoiceOverlap={lyric.note.voice_overlap_ms}
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

        if lyric.note.tuning.pbm:
            self._write_line(file, f"PBM={lyric.note.tuning.pbm}")

        if lyric.note.consonant_velocity:
            self._write_line(file, f"Velocity={lyric.note.consonant_velocity}")

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
