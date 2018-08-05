
class WeightedDigraph:
    class Node:
        def __init__(self, value):
            self.value = value
            self.adj = {}

        def __str__(self):
            return str(self.value)

        def add_neighbor(self, node, weight=0):
            self.adj[node] = weight

        def neighbors(self):
            return self.adj.keys()

        def value(self):
            return value

        def get_weight(self, node):
            return self.adj[node]

    def __init__(self):
        self.V = {}

    def add(self, value):
        node = self.Node(value)
        self.V[value] = node
        return node

    def get(self, value):
        if value in self.V:
            return self.V[value]
        else:
            return None

    def add_edge(self, head, tail, weight=0):
        if head not in self.V:
            node = self.add(head)
        else:
            node = self.get(head)
        if tail not in self.V:
            self.add(tail)

        node.add_neighbor(tail, weight)

    def vertixes(self):
        return self.V.keys()

    def show(self):
        for key in sorted(self.V, key=lambda n:str(n)):
            v = self.V[key]
            print(str(v),':')
            for adj in sorted(v.adj, key=lambda n:(v.adj[n], str(n))):
                print('\t->(', v.adj[adj], ') \t', str(adj))
