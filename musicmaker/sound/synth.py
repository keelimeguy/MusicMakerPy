import math
import numpy
import pyaudio
from scipy import interpolate
from operator import itemgetter

# Including techniques from:
#   https://davywybiral.blogspot.com/2010/09/procedural-music-with-pyaudio-and-numpy.html

class Synth:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def shape(self, data, points, kind='slinear'):
        items = points.items()
        sorted(items, key=itemgetter(0))
        keys = list(map(itemgetter(0), items))
        vals = list(map(itemgetter(1), items))
        interp = interpolate.interp1d(keys, vals, kind=kind)
        factor = 1.0 / len(data)
        shape = interp(numpy.arange(len(data)) * factor)
        return data * shape

    def tongue(self, data):
        return self.shape(data, {0.0: 0.0, 0.02: 1.0, 1.0: 1.0})

    def release(self, data):
        return self.shape(data, {0.0: 1.0, 0.98: 1.0, 1.0: 0.0})

    def clean_ends(self, data):
        return self.shape(data, {0.0: 0.0, 0.02: 1.0, 0.98: 1.0, 1.0: 0.0})

    def sine_tone(self, freq=440.0, duration_ms=1000, volume=1.0):
        num_samples = int(self.sample_rate * (duration_ms / 1000.0))
        factor = freq * (math.pi * 2.0) / self.sample_rate
        return numpy.sin(numpy.arange(num_samples) * factor) * 0.2

    def harmonics(self, freq, duration_ms=1000, volume=1.0):
        a = self.sine_tone(freq, duration_ms, volume)
        b = self.sine_tone(freq*2.0, duration_ms, volume) * 0.5
        c = self.sine_tone(freq*4.0, duration_ms, volume) * 0.125
        return a + b + c

    def harmonics_soft(self, freq, duration_ms=1000, volume=1.0):
        a = self.sine_tone(freq, duration_ms, volume)
        b = self.sine_tone(freq*2.0, duration_ms, volume) * 0.5
        return a + b

    def chime(self, freq, duration_ms=1000, volume=1.0):
        chunk = self.harmonics(freq, duration_ms, volume)
        return self.shape(chunk, {0.0: 0.0, 0.005: 1.0, 0.25: 0.5, 0.9: 0.1, 1.0:0.0})

    def chime_soft(self, freq, duration_ms=1000, volume=1.0):
        chunk = self.harmonics_soft(freq, duration_ms, volume)
        return self.shape(chunk, {0.0: 0.0, 0.5:0.75, 0.8:0.4, .98:0.1, 1.0:0.0})

    def chord(self, freqs, effect, duration_ms=1000, volume=1.0):
        data = effect(freqs[0], duration_ms, volume)
        for freq in freqs[1:]:
            data += effect(freq, duration_ms, volume)
        return data
