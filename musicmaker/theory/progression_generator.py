import random

from ..structure.weighteddigraph import WeightedDigraph
from .chord import Chord
from .progression import Progression


class ProgressionGenerator(WeightedDigraph):
    position_dict = {}

    class Weight:
        PRIMARY = 0
        RESOLVE = 1
        COMMON = 2
        UNCOMMON = 4
        SPARSE = 8
        RARE = 16

    class Position:
        def __init__(self, name, root_step, base_adjust='', opt_adjust='', step_adjust=0):
            self.name = name
            self.root_step = root_step
            self.base_adjust = base_adjust
            self.opt_adjust = opt_adjust
            self.step_adjust = step_adjust

        def __str__(self):
            return self.name

        def __lt__(self, other):
            return str(self) < str(other)

        def get_base_pitch(self, scale):
            return scale.get_pitch(self.root_step).transpose(self.step_adjust)

        def get_base_chord(self, scale):
            if scale.root:
                pitch = self.get_base_pitch(scale)
                return Chord.create(pitch.name + self.base_adjust)
            return (self.name, [str(self.root_step)+'('+str(self.step_adjust)+')', self.base_adjust])

        def get_adjusted_chord(self, scale, i):
            if scale.root:
                pitch = self.get_base_pitch(scale)
                return Chord.create(pitch.name + self.opt_adjust[i])
            return (self.name, [str(self.root_step)+'('+str(self.step_adjust)+')', self.opt_adjust[i]])

        def get_random_adjusted_chord(self, scale):
            i = random.randint(0, len(self.opt_adjust))
            if i != len(self.opt_adjust):
                return self.get_adjusted_chord(scale, i)
            else:
                return self.get_base_chord(scale)

        def get_chord_list(self, scale):
            return [chord for chord in [self.get_base_chord(scale)] + [self.get_adjusted_chord(
                scale, i) for i in range(len(self.opt_adjust))]]

    def __init__(self, scale, resolve, start=None):
        WeightedDigraph.__init__(self)
        self.scale = scale
        self.resolve = self.get_else_add(resolve)
        if start:
            self.start = self.get_else_add(start)
        else:
            self.start = self.resolve

    def add_transition_edge(self, head_position_str, tail_position_str, weight=Weight.PRIMARY):
        self.add_edge(self.position_dict[head_position_str], self.position_dict[tail_position_str], weight)

    def show(self):
        for key in sorted(self.V):
            v = self.V[key]
            if self.scale.root:
                print(str(v.value), [str(chord) for chord in v.value.get_chord_list(self.scale)], ':')
            else:
                print(str(v.value), ':')
            for adj in sorted(v.adj, key=lambda n: (v.adj[n], n.value)):
                if self.scale.root:
                    print('\t->(', v.adj[adj], ') \t', str(adj.value), [str(chord)
                          for chord in adj.value.get_chord_list(self.scale)])
                else:
                    print('\t->(', v.adj[adj], ') \t', str(adj.value))

    def set_scale(self, scale):
        self.scale = scale

    def generate(self, length=4, loop=True, ext=True):
        p = Progression(loop=loop, tempo=60)
        cur = self.start
        p.add(cur.value.get_base_chord(self.scale))
        for i in range(length-1):
            next = random.randint(0, cur.outdegree()-1)
            cur = cur.neighbors()[next]
            if ext:
                p.add(cur.value.get_random_adjusted_chord(self.scale))
            else:
                p.add(cur.value.get_base_chord(self.scale))

        return p
