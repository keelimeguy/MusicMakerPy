# MusicMakerPy
![build-status-master](https://github.com/keelimeguy/MusicMakerPy/actions/workflows/python-app.yml/badge.svg?branch=master)
[![GitHub license](https://img.shields.io/github/license/keelimeguy/MusicMakerPy)](https://github.com/keelimeguy/MusicMakerPy/blob/master/LICENSE)

A program to make, generate, and play: chord progressions, phrases, and other such musical things.

This program is an inspired rewrite of my [java implementation](https://github.com/keelimeguy/MusicMaker).

There is also a _newer_ [c++ version](https://github.com/keelimeguy/MusicMaker_JUCE).

## Usage
Python virtual environment is always recommended.

A small script is included that might help with usage:
`./run.sh help`

### Requirements
`pip install -r requirements.txt`

#### Install Issues
If you get errors about pyaudio, try:

`sudo apt-get update`

`sudo apt-get install portaudio19-dev --fix-missing`

### Testing
`python -m unittest`

### Command line
`python -m musicmaker.theory.chord -h`

`python -m musicmaker.theory.scale -h`

`python -m musicmaker.sound.metronome -h`

`python -m musicmaker.sound.wav -h`

`python -m musicmaker.sound.staffplayer -h`

`python -m musicmaker.theory.major_progression_generator -h`

`python -m musicmaker.theory.minor_progression_generator -h`

`python -m musicmaker.theory.instrument.ukulele -h`

`python -m musicmaker.theory.instrument.guitar -h`

`python -m musicmaker.parser.abc_parser`

`python -m ust_creator.main -h`
