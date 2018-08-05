
class WeightedDigraph:
    class Node:
        def __init__(self, value):
            self.value = value
            self.adj = {}

        def add_neighbor(self, node, weight=0):
            self.adj[node] = weight

        def outdegree(self):
            return len(self.adj)

        def neighbors(self):
            return sorted(self.adj.keys(), key=lambda n: n.value)

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

    def get_else_add(self, value):
        if value in self.V:
            return self.V[value]
        else:
            return self.add(value)

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
            tail_node = self.add(tail)
        else:
            tail_node = self.get(tail)

        node.add_neighbor(tail_node, weight)

    def vertixes(self):
        return self.V.keys()

    def show(self):
        for key in sorted(self.V):
            v = self.V[key]
            print(str(v.value),':')
            for adj in sorted(v.adj, key=lambda n: (v.adj[n], n.value)):
                print('\t->(', v.adj[adj], ') \t', str(adj.value))
