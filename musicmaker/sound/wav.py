import argparse
import pyaudio
import struct
import math
import wave
import sys

from .synth import Synth

class Wav:
    def __init__(self, sample_rate=44100.0):
        self.audio = []
        self.sample_rate = sample_rate

    def add_rest(self, duration_ms=500):
        self.audio += Synth.rest(duration_ms=duration_ms, sample_rate=self.sample_rate)

    def add_sine(self, freq=440.0, duration_ms=500, volume=1.0):
        self.audio += Synth.sine_tone(freq=freq, duration_ms=duration_ms, volume=volume, sample_rate=self.sample_rate)

    def save(self, file_name):
        wav_file = wave.open(file_name,'w')

        nchannels = 1
        sampwidth = 2
        nframes = len(self.audio)
        comptype = 'NONE'
        compname = 'not compressed'
        wav_file.setparams((nchannels, sampwidth, self.sample_rate, nframes, comptype, compname))

        # (short) 16-bit signed integers for the sample size
        # 32767 is the maximum value for a short integer.
        for sample in self.audio:
            wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

        wav_file.close()
        return

    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(2),
            channels=1,
            rate=self.sample_rate,
            output=True
        )

        for sample in self.audio:
            stream.write(struct.pack('h', int( sample * 32767.0 )))

        stream.stop_stream()
        stream.close()

        p.terminate()

    def play_file(file):
        CHUNK = 1024

        wf = wave.open(file, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        data = wf.readframes(CHUNK)
        while data != b'':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Play .wav files.')
    parser.add_argument('-p', '--play',
        help='Play the given .wav file.')
    parser.add_argument('-g', '--generate', action='store_true',
        help='Generate a wav file and play it.')
    parser.add_argument('-o', '--output',
        help='Generate a wav file and save it to this ouput.')

    args = parser.parse_args()
    if not (args.output or args.generate or args.play):
        print('Nothing to do. Try running with -h')
        sys.exit()

    if args.output or args.generate:
        wav = Wav(88200)
        wav.add_sine(440.0, 1000, 1)
        wav.add_rest()
        wav.add_sine(220.0, 500, 1)
        wav.add_rest()
        wav.add_sine(880.0, 500, 1)

        if args.output:
            print('Saving to', args.output, flush=True)
            wav.save(args.output)
        if args.generate:
            wav.play()

    if args.play:
        print('Playing', args.play, flush=True)
        Wav.play_file(args.play)
