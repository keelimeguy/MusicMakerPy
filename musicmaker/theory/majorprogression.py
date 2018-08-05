import argparse
import sys

from .progressiongraph import ProgressionGraph
from .scale import Scale
from .pitch import Pitch

# Based on http://mugglinworks.com/chordmaps/GenericMap.pdf
# Defined here in order: blue top to bottom, left green top to bottom, then right green top to bottom
class MajorProgression(ProgressionGraph):
    position_dict = {
        'iim':        ProgressionGraph.Position('iim', 2, 'm', ['m7','m9']),
        'V':          ProgressionGraph.Position('V', 5, '', ['7','9','11','13','sus4']),
        'iiim':       ProgressionGraph.Position('iiim', 3, 'm', ['m7']),
        'vim':        ProgressionGraph.Position('vim', 6, 'm', ['m7', 'm9']),
        'IV':         ProgressionGraph.Position('IV', 4, '', ['6', 'M7', 'm', 'm6']),
        'I/3':        ProgressionGraph.Position('I/3', 1, '/3', []),
        'I/5':        ProgressionGraph.Position('I/5', 1, '/5', []),
        'I':          ProgressionGraph.Position('I', 1, '', ['2','6','M7','M9','sus4']),
        'IV/1':       ProgressionGraph.Position('IV/1', 4, '/1', []),
        'V/1':        ProgressionGraph.Position('V/1', 5, '/1', []),

        # Mb9no7 used in opt_adjust instead of b9 to avoid conflicts with e.g. Bb 9 and B b9
        'IIIm7b5':    ProgressionGraph.Position('IIIm7b5', 3, 'm7b5', []),
        'VI':         ProgressionGraph.Position('VI', 6, '', ['7', '9', 'Mb9no7']),
        '#Idim7':     ProgressionGraph.Position('#Idim7', 1.5, 'dim7', []),
        '#IVm7b5':    ProgressionGraph.Position('#IVm7b5', 4.5, 'm7b5', []),
        'VII':        ProgressionGraph.Position('VII', 7, '', ['7', '9', 'Mb9no7']),
        '#IIdim7':    ProgressionGraph.Position('#IIdim7', 2.5, 'dim7', []),
        'Vm':         ProgressionGraph.Position('Vm', 5, 'm', ['7']),
        'I*':         ProgressionGraph.Position('I*', 1, '7', ['7', '9', 'Mb9no7']),
        'Im6':        ProgressionGraph.Position('Im6', 1, 'm6', []),
        'V/2':        ProgressionGraph.Position('V/2', 5, '/2', []),
        'II':         ProgressionGraph.Position('II', 2, '', ['7', '9', 'Mb9no7']),
        'bVI':        ProgressionGraph.Position('bVI', -6.5, '', []),
        'bVII':       ProgressionGraph.Position('bVII', -7.5, '', ['9']),
        'IVm7':       ProgressionGraph.Position('IVm7', 4, 'm7', []),
        'bII7':       ProgressionGraph.Position('bII7', -2.5, '7', []),
        'VIm7b5/b3':  ProgressionGraph.Position('VIm7b5/b3', 6, 'm7b5/b3', []),
        '#Vdim7':     ProgressionGraph.Position('#Vdim7', 5.5, 'dim7', []),
        'VIIm7b5':    ProgressionGraph.Position('VIIm7b5', 7, 'm7b5', []),
        'III':        ProgressionGraph.Position('III', 3, '', ['7', '9', 'Mb9no7']),
        'Idim/b3':    ProgressionGraph.Position('Idim/b3', 1, 'dim/b3', []),
        'bVI7':       ProgressionGraph.Position('bVI7', -6.5, '7', []),
        'bVII9':      ProgressionGraph.Position('bVII9', -7.5, '9', [])
    }

    def __init__(self, root=None, start=None):
        resolve = self.position_dict['I']
        ProgressionGraph.__init__(self, Scale(root, 'Major'), resolve, start)
        self.setup()

    def setup(self):
        self.add_transition_edge('iim', 'V')
        self.add_transition_edge('iim', 'iiim')
        self.add_transition_edge('iiim', 'iim', self.Weight.SPARSE)
        self.add_transition_edge('V', 'iiim')
        self.add_transition_edge('iiim', 'V', self.Weight.SPARSE)
        self.add_transition_edge('V', 'vim')
        self.add_transition_edge('vim', 'V', self.Weight.SPARSE)
        self.add_transition_edge('iiim', 'I', self.Weight.RESOLVE)
        self.add_transition_edge('iiim', 'IV')
        self.add_transition_edge('IV', 'iiim', self.Weight.SPARSE)
        self.add_transition_edge('iiim', 'vim')
        self.add_transition_edge('vim', 'iiim', self.Weight.SPARSE)
        self.add_transition_edge('vim', 'IV')
        self.add_transition_edge('IV', 'vim', self.Weight.SPARSE)
        self.add_transition_edge('vim', 'iim')
        self.add_transition_edge('iim', 'vim', self.Weight.SPARSE)
        self.add_transition_edge('IV', 'I', self.Weight.RESOLVE)
        self.add_transition_edge('IV', 'V')
        self.add_transition_edge('V', 'IV', self.Weight.SPARSE)
        self.add_transition_edge('IV', 'iim')
        self.add_transition_edge('iim', 'IV', self.Weight.SPARSE)
        self.add_transition_edge('IV', 'I/5', self.Weight.COMMON)
        self.add_transition_edge('I/5', 'IV', self.Weight.SPARSE)
        self.add_transition_edge('IV', 'I/3', self.Weight.UNCOMMON)
        self.add_transition_edge('I/3', 'IV', self.Weight.UNCOMMON)
        self.add_transition_edge('I/3', 'iim', self.Weight.UNCOMMON)
        self.add_transition_edge('iim', 'I/3', self.Weight.UNCOMMON)
        self.add_transition_edge('iim', 'IVm7', self.Weight.RESOLVE)
        self.add_transition_edge('iim', 'I/5', self.Weight.COMMON)
        self.add_transition_edge('I/5', 'V')
        self.add_transition_edge('V', 'I', self.Weight.RESOLVE)
        self.add_transition_edge('IV/1', 'I')
        self.add_transition_edge('V/1', 'I')
        self.add_transition_edge('I', 'IV/1', self.Weight.UNCOMMON)
        self.add_transition_edge('I', 'V/1', self.Weight.UNCOMMON)

        self.add_transition_edge('IIIm7b5', 'VI')
        self.add_transition_edge('VI', 'iim')
        self.add_transition_edge('#Idim7', 'iim')
        self.add_transition_edge('#IVm7b5', 'VII')
        self.add_transition_edge('VII', 'iiim')
        self.add_transition_edge('#IIdim7', 'iiim')
        self.add_transition_edge('Vm', 'I*')
        self.add_transition_edge('I*', 'IV')
        self.add_transition_edge('IIIm7b5', 'IV')
        self.add_transition_edge('Im6', 'V/2')
        self.add_transition_edge('Im6', 'II')
        self.add_transition_edge('V/2', 'II')
        self.add_transition_edge('II', 'V')
        self.add_transition_edge('#IVm7b5', 'V')
        self.add_transition_edge('bVI', 'bVII')
        self.add_transition_edge('bVII', 'I')
        self.add_transition_edge('IVm7', 'I')
        self.add_transition_edge('bII7', 'I')
        self.add_transition_edge('VIm7b5/b3', 'II')
        self.add_transition_edge('#Vdim7', 'vim')
        self.add_transition_edge('III', 'vim')
        self.add_transition_edge('VIIm7b5', 'III')
        self.add_transition_edge('Idim/b3', 'iim')
        self.add_transition_edge('bVI7', 'I/5')
        self.add_transition_edge('bVII9', 'I/5')
        self.add_transition_edge('#IVm7b5', 'I/5')

        for position_str in ['iim', 'iiim', 'IV', 'V', 'vim', 'I/5', 'I/3', 'IV/1', 'V/1']:
            for position_str_2 in ['IIIm7b5', 'VI', '#Idim7', '#IVm7b5', 'VII', '#IIdim7',
                        'Vm', 'I*', 'Im6', 'V/2', 'II', 'bVI', 'bVII', 'IVm7', 'bII7',
                        'VIm7b5/b3', '#Vdim7', 'III', 'VIIm7b5', 'Idim/b3', 'bVI7', 'bVII9']:
                self.add_transition_edge(position_str, position_str_2, self.Weight.RARE)

        for position_str in ['iim', 'iiim', 'IV', 'V', 'vim']:
            self.add_transition_edge('I', position_str)
        for position_str in ['IIIm7b5', 'VI', '#Idim7', '#IVm7b5', 'VII', '#IIdim7',
                    'Vm', 'I*', 'Im6', 'V/2', 'II', 'bVI', 'bVII', 'IVm7', 'bII7',
                    'VIm7b5/b3', '#Vdim7', 'III', 'VIIm7b5', 'Idim/b3', 'bVI7', 'bVII9']:
            self.add_transition_edge('I', position_str, self.Weight.SPARSE)
        self.add_transition_edge('I', 'I/5', self.Weight.UNCOMMON)
        self.add_transition_edge('I', 'I/3', self.Weight.UNCOMMON)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate major chord progression.')
    parser.add_argument('-r', '--root',
        help='The root of the major progression (e.g. C, Bb, F#).')
    parser.add_argument('-g', '--generate',
        help='Generate a major progression with the given length.')
    args = parser.parse_args()

    if args.root:
        if not Pitch.valid(args.root):
            print('Valid roots are', ['None']+[root for root in Pitch.notes()])
            sys.exit()
        p = MajorProgression(Pitch(args.root));
    else:
        p = MajorProgression();

    if args.generate:
        p.generate(int(args.generate)).show()
    else:
        p.show();
