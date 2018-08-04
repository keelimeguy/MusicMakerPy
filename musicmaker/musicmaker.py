import argparse

class MusicMaker:
    def __init__(self):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A program to make, generate, and play: chord progressions, phrases, and other such musical things.')
    args = parser.parse_args()

    mm = MusicMaker()
