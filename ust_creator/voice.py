from enum import Enum

VoiceType = Enum('VoiceType', 'CV VCV CVVC VCCV')


class Voice:
    def __init__(self, directory: str, voice_type: VoiceType = VoiceType.VCV):
        self._directory = f"%VOICE%{directory}"

        if isinstance(voice_type, str):
            if voice_type == 'CV':
                voice_type = VoiceType.CV
            elif voice_type == 'VCV':
                voice_type = VoiceType.VCV
            elif voice_type == 'CVVC':
                voice_type = VoiceType.CVVC
            elif voice_type == 'VCCV':
                voice_type = VoiceType.VCCV
            else:
                raise ValueError(f"unrecognized voice type: {voice_type}")

        self._voice_type = voice_type

    @property
    def directory(self):
        return self._directory

    @property
    def voice_type(self):
        return self._voice_type
