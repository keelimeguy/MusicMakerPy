import argparse
import pyaudio
import struct
import numpy
import math
import wave
import sys

from .synth import Synth

class Wav:
    def __init__(self, sample_rate=44100):
        self.audio = []
        self.sample_rate = sample_rate
        self.synth = Synth(sample_rate)

    def add_rest(self, duration_ms=500):
        num_samples = int(self.sample_rate * (duration_ms / 1000.0))
        self.audio.append(numpy.sin(numpy.zeros(num_samples)))

    def append_sound(self, audio):
        self.audio.append(audio)

    def save(self, file_name):
        wav_file = wave.open(file_name,'w')

        nchannels = 1
        sampwidth = 2
        nframes = len(self.audio)
        comptype = 'NONE'
        compname = 'not compressed'
        wav_file.setparams((nchannels, sampwidth, self.sample_rate, nframes, comptype, compname))

        # (short) 16-bit signed integers for the sample size
        #   [32767 is the maximum value for a short integer.]
        chunk = numpy.concatenate(self.audio)
        chunk = numpy.vectorize(lambda sample: struct.pack('h', int( sample * 32767.0 )))(chunk)
        wav_file.writeframes(chunk)

        wav_file.close()
        return

    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True
        )

        chunk = numpy.concatenate(self.audio)
        stream.write(chunk.astype(numpy.float32).tostring())

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
        sound1 = wav.synth.chime
        sound2 = wav.synth.chime_soft
        wav.append_sound(wav.synth.chord([440.00], sound2)+wav.synth.chord([440.00], sound1))
        wav.append_sound(wav.synth.chord([440.00, 493.88], sound2)+wav.synth.chord([493.88], sound1))
        wav.append_sound(wav.synth.chord([440.00, 493.88, 554.37], sound2)+wav.synth.chord([554.37], sound1))
        wav.append_sound(wav.synth.chord([440.00, 493.88, 554.37, 880.0], sound2)+wav.synth.chord([880.0], sound1))
        wav.add_rest()

        if args.output:
            print('Saving to', args.output, flush=True)
            wav.save(args.output)
        if args.generate:
            wav.play()

    if args.play:
        print('Playing', args.play, flush=True)
        Wav.play_file(args.play)
