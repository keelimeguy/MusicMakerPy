import contextlib
import argparse
import pyaudio
import struct
import numpy
import wave
import sys
import os

from .synth import Synth


@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


class Wav:
    def __init__(self, sample_rate=44100):
        self.audio = {}
        self.sample_rate = sample_rate
        self.synth = Synth(sample_rate)

    def add_rest(self, duration_ms=500, channel='__default__'):
        num_samples = int(self.sample_rate * (duration_ms / 1000.0))
        if channel not in self.audio:
            self.audio[channel] = []
        self.audio[channel].append(numpy.zeros(num_samples))

    def append_sound(self, audio, channel='__default__'):
        if channel not in self.audio:
            self.audio[channel] = []
        self.audio[channel].append(audio)

    def save(self, file_name):
        wav_file = wave.open(file_name, 'w')

        nchannels = 1
        sampwidth = 2
        nframes = len(self.audio)
        comptype = 'NONE'
        compname = 'not compressed'
        wav_file.setparams((nchannels, sampwidth, self.sample_rate, nframes, comptype, compname))

        chunk_dict = {}
        for channel in self.audio:
            chunk_dict[channel] = numpy.concatenate(self.audio[channel]) * 0.25
        vals = list(chunk_dict.values())
        chunk = vals[0]
        for val in vals[1:]:
            chunk += val

        # (short) 16-bit signed integers for the sample size
        #   [32767 is the maximum value for a short integer.]
        chunk = numpy.vectorize(lambda sample: struct.pack('h', int(sample * 32767.0)))(chunk)
        wav_file.writeframes(chunk)

        wav_file.close()
        return

    def play(self, loop=False):
        with ignore_stderr():
            p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True
        )

        chunk_dict = {}
        maxlen = 0
        for channel in self.audio:
            chunk_dict[channel] = numpy.concatenate(self.audio[channel]) * 0.25
            if len(chunk_dict[channel]) > maxlen:
                maxlen = len(chunk_dict[channel])
        vals = list(chunk_dict.values())
        chunk = vals[0]
        difflen = maxlen - len(chunk)
        if difflen > 0:
            chunk = numpy.pad(chunk, (0, difflen), 'constant')
        for val in vals[1:]:
            difflen = maxlen - len(val)
            if difflen > 0:
                val = numpy.pad(val, (0, difflen), 'constant')
            chunk += val
        chunk = chunk.astype(numpy.float32).tostring()

        if loop:
            while(1):
                stream.write(chunk)

        stream.write(chunk)

        stream.stop_stream()
        stream.close()

        p.terminate()

    @classmethod
    def play_file(cls, file):
        chunk_size = 1024

        wf = wave.open(file, 'rb')

        with ignore_stderr():
            p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        data = wf.readframes(chunk_size)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk_size)

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
