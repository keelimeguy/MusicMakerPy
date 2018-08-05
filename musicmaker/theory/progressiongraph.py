from ..structure.weighteddigraph import WeightedDigraph
from .chord import Chord

class ProgressionGraph(WeightedDigraph):
    position_dict = {}

    class Weight:
        PRIMARY=0
        RESOLVE=1
        COMMON=2
        UNCOMMON=4
        SPARSE=8
        RARE=16

    class Position:
        def __init__(self, name, root_step, base_adjust, opt_adjust):
            self.name = name
            self.root_step = root_step
            self.base_adjust = base_adjust
            self.opt_adjust = opt_adjust

        def __str__(self):
            return self.name

        def get_base_pitch(self, scale):
            pitch = scale.root.half_step(scale.mode.find_step(int(abs(self.root_step))))
            if int(abs(self.root_step)) != self.root_step:
                if self.root_step < 0:
                    pitch = pitch.flat()
                else:
                    pitch = pitch.sharp()
            return pitch

        def get_base_chord(self, scale):
            pitch = get_base_pitch(scale)
            Chord(pitch.name + self.base_adjust);

        def get_adjusted_chord(self, scale, i):
            pitch = get_base_pitch(scale)
            Chord(pitch.name + self.opt_adjust[i]);

    def __init__(self, scale, resolve, start=None):
        WeightedDigraph.__init__(self)
        self.scale = scale
        self.resolve = resolve
        if start:
            self.start = start
        else:
            self.start = resolve

    def add_transition_edge(self, head_position_str, tail_position_str, weight=Weight.PRIMARY):
        self.add_edge(self.position_dict[head_position_str], self.position_dict[tail_position_str], weight)

    def show(self):
        WeightedDigraph.show(self)
