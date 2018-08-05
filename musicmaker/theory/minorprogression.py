import argparse
import sys

from .progressiongraph import ProgressionGraph
from .scale import Scale
from .pitch import Pitch

# Based on http://mugglinworks.com/chordmaps/GenericMapMinor.pdf
# Defined here in order: blue top to bottom, left green top to bottom, then right green top to bottom
class MinorProgression(ProgressionGraph):
    position_dict = {
        # Mb9no7 used in opt_adjust instead of b9 to avoid conflicts with e.g. Bb 9 and B b9
        'iidim':      ProgressionGraph.Position('iidim', 2, 'dim', []),
        'viidim/2':   ProgressionGraph.Position('viidim/2', 7, 'dim/2', []),
        'V':          ProgressionGraph.Position('V', 5, '', ['7','Mb9no7','Mb13no7','sus4']),
        'bIIIaug':    ProgressionGraph.Position('bIIIaug', -3.5, 'aug', []),
        'im/b3':      ProgressionGraph.Position('im/b3', 1, 'm/b3', []),
        'bVI':        ProgressionGraph.Position('bVI', -6.5, '', ['6', 'M7']),
        'ivm/b6':     ProgressionGraph.Position('ivm/b6', 4, 'm/b6', ['m6/b6', 'm7/b6']),
        'ivm':        ProgressionGraph.Position('ivm', 4, 'm', ['m6', 'm7', 'm9']),
        'bII/4':      ProgressionGraph.Position('bII/4', -2.5, '/4', []),
        'im/b3':      ProgressionGraph.Position('im/b3', 1, 'm/b3', []),
        'im/5':       ProgressionGraph.Position('im/5', 1, 'm/5', []),
        'im':         ProgressionGraph.Position('im', 1, '', ['2','sus4']),
        'ivm/1':      ProgressionGraph.Position('ivm/1', 4, 'm/1', []),
        'V/1':        ProgressionGraph.Position('V/1', 5, '/1', []),

        'iidim7':     ProgressionGraph.Position('iidim7', 2, 'dim7', []),
        'V*':         ProgressionGraph.Position('V*', 5, '', ['7', 'Mb9no7']),
        'Vdim7':      ProgressionGraph.Position('Vdim7', 5, 'dim7', ['7', 'm7b5']),
        'iiidim7':    ProgressionGraph.Position('iiidim7', 3, 'dim7', []),
        'I':          ProgressionGraph.Position('I', 1, '', ['7', 'Mb9no7']),
        '#ivdim7':    ProgressionGraph.Position('#ivdim7', 4.5, 'dim7', []),
        'vim7b5':     ProgressionGraph.Position('vim7b5', 6, 'm7b5', []),
        'II':         ProgressionGraph.Position('II', 2, '', ['7', 'b9']),
        'bVI*':       ProgressionGraph.Position('bVI*', -6.5, '', []),
        'bVII':       ProgressionGraph.Position('bVII', -7.5, '', ['9']),
        'ivm7':       ProgressionGraph.Position('ivm7', 4, 'm7', []),
        'Vm7b5':      ProgressionGraph.Position('Vm7b5', 5, 'm7b5', ['dim7']),
        'bIII':       ProgressionGraph.Position('bIII', -3.5, '', ['7', '9', 'b9']),
        'bviim7b5':   ProgressionGraph.Position('bviim7b5', -7.5, 'm7b5', []),
        'bVI7':       ProgressionGraph.Position('bVI7', -6.5, '7', []),
    }

    def __init__(self, root, start=None):
        resolve = self.position_dict['im']
        ProgressionGraph.__init__(self, Scale(root, Scale.modes['Minor']), resolve, start)
        self.setup()

    def setup(self):
        for position_str in ['iidim', 'viidim/2']:
            self.add_transition_edge(position_str, 'V')
            for position_str_2 in ['bIIIaug', 'im/b3']:
                self.add_transition_edge(position_str, position_str_2)
                self.add_transition_edge(position_str_2, position_str, self.Weight.SPARSE)
        for position_str in ['bIIIaug', 'im/b3', 'bVI', 'ivm/b6']:
            self.add_transition_edge('V', position_str)
            self.add_transition_edge(position_str, 'V', self.Weight.SPARSE)
        for position_str in ['bIIIaug', 'im/b3']:
            self.add_transition_edge(position_str, 'im', self.Weight.RESOLVE)
            for position_str_2 in ['ivm', 'bII/4', 'bVI', 'ivm/b6']:
                self.add_transition_edge(position_str, position_str_2)
                self.add_transition_edge(position_str_2, position_str, self.Weight.SPARSE)
        for position_str in ['bVI', 'ivm/b6']:
            for position_str_2 in ['ivm', 'bII/4', 'iidim', 'viidim/2']:
                self.add_transition_edge(position_str, position_str_2)
                self.add_transition_edge(position_str_2, position_str, self.Weight.SPARSE)
        for position_str in ['ivm', 'bII/4']:
            self.add_transition_edge(position_str, 'im', self.Weight.RESOLVE)
            self.add_transition_edge(position_str, 'V')
            self.add_transition_edge('V', position_str, self.Weight.SPARSE)
            for position_str_2 in ['iidim', 'viidim/2']:
                self.add_transition_edge(position_str, position_str_2)
                self.add_transition_edge(position_str_2, position_str, self.Weight.SPARSE)
            self.add_transition_edge(position_str, 'im/5', self.Weight.COMMON)
            self.add_transition_edge('im/5', position_str, self.Weight.SPARSE)
            self.add_transition_edge(position_str, 'im/b3', self.Weight.UNCOMMON)
            self.add_transition_edge('im/b3', position_str, self.Weight.UNCOMMON)
        for position_str in ['iidim', 'viidim/2']:
            self.add_transition_edge('im/b3', position_str, self.Weight.UNCOMMON)
            self.add_transition_edge(position_str, 'im/b3', self.Weight.UNCOMMON)
            self.add_transition_edge(position_str, 'ivm7', self.Weight.RESOLVE)
            self.add_transition_edge(position_str, 'im/5', self.Weight.COMMON)
        self.add_transition_edge('im/5', 'V')
        self.add_transition_edge('V', 'im', self.Weight.RESOLVE)
        self.add_transition_edge('ivm/1', 'im')
        self.add_transition_edge('V/1', 'im')
        self.add_transition_edge('im', 'ivm/1', self.Weight.UNCOMMON)
        self.add_transition_edge('im', 'V/1', self.Weight.UNCOMMON)

        for position_str in ['bIIIaug', 'im/b3']:
            self.add_transition_edge('V*', position_str)
            self.add_transition_edge('iidim7', position_str)
        self.add_transition_edge('Vdim7', 'I')
        for position_str in ['ivm', 'bII/4']:
            self.add_transition_edge('I', position_str)
            self.add_transition_edge('iiidim7', position_str)
        self.add_transition_edge('vim7b5', 'II')
        self.add_transition_edge('II', 'V')
        self.add_transition_edge('#ivdim7', 'V')
        self.add_transition_edge('bVI*', 'bVII')
        self.add_transition_edge('bVII', 'im')
        self.add_transition_edge('ivm7', 'im')
        for position_str in ['bVI', 'ivm/b6']:
            self.add_transition_edge('Vm7b5', position_str)
            self.add_transition_edge('bIII', position_str)
        self.add_transition_edge('bviim7b5', 'bIII')
        self.add_transition_edge('bVI7', 'im/5')
        self.add_transition_edge('#ivdim7', 'im/5')

        for position_str in ['iidim', 'bIIIaug', 'ivm', 'V', 'bVI', 'im/5', 'im/b3', 'ivm/1', 'V/1']:
            for position_str_2 in ['V*', 'iidim7', 'Vdim7', 'I', 'iiidim7', 'vim7b5', 'II', '#ivdim7',
                        'bVI*', 'bVII', 'ivm7', 'Vm7b5', 'bIII', 'bviim7b5', 'bVI7', '#ivdim7']:
                self.add_transition_edge(position_str, position_str_2, self.Weight.RARE)

        for position_str in ['iidim', 'bIIIaug', 'ivm', 'V', 'bVI']:
            self.add_transition_edge('im', position_str)
        for position_str in ['V*', 'iidim7', 'Vdim7', 'I', 'iiidim7', 'vim7b5', 'II', '#ivdim7',
                        'bVI*', 'bVII', 'ivm7', 'Vm7b5', 'bIII', 'bviim7b5', 'bVI7', '#ivdim7']:
            self.add_transition_edge('im', position_str, self.Weight.SPARSE)
        self.add_transition_edge('im', 'im/5', self.Weight.UNCOMMON)
        self.add_transition_edge('im', 'im/b3', self.Weight.UNCOMMON)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate minor chord progression.')
    parser.add_argument('root',
        help='The root of the minor progression.')
    args = parser.parse_args()

    if not Pitch.valid(args.root):
        print('Valid roots are', [root for root in Pitch.notes()])
        sys.exit()

    p = MinorProgression(Pitch(args.root));
    p.show();
