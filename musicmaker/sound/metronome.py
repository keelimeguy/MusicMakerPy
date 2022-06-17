import argparse

from time import time, sleep
from threading import Thread


class Metronome(Thread):
    def __init__(self, bpm, task):
        Thread.__init__(self)
        self.spb = 60/bpm
        self.task = task
        self.done = False

    def run(self):
        # Sync time (delay noticeable for very low bpm)
        sleep(self.spb - time() % self.spb)
        while not self.done:
            self.task()
            sleep(self.spb - time() % self.spb)

    def stop(self):
        self.done = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a neverending metronome at a given BPM.')
    parser.add_argument('bpm', help='The target BPM of the metronome (e.g. 60).')
    args = parser.parse_args()

    m = Metronome(int(args.bpm), lambda: print(time(), flush=True))
    print('Starting..', flush=True)
    m.start()
