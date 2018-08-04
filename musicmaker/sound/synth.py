import math
import pyaudio

class Synth:
    def __init__(self):
        pass

    def sine_tone(freq=440.0, duration_ms=500, volume=1.0, sample_rate=44100.0):
        audio = []
        num_samples = duration_ms * (sample_rate / 1000.0)
        for x in range(int(num_samples)):
            audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))
        return audio

    def rest(duration_ms=500, sample_rate=44100.0):
        audio = []
        num_samples = duration_ms * (sample_rate / 1000.0)
        for x in range(int(num_samples)):
            audio.append(0.0)
        return audio
