class Vertex:
    def __init__(self, name : str):
        self.name = name
    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return 'Vertex({})'.format(repr(self.name))

class Graph:
    def __init__(self):
        self.vertices = set()
        self.adjacents = dict()

    def __iter__(self):
        return iter(self.vertices)

    def __getitem__(self, item):
        return iter(self.adjacents[item])

    def add_vertex(self, vertex : Vertex):
        if vertex not in self.adjacents:
            self.vertices.add(vertex)
            self.adjacents[vertex] = set()

    def add_edge(self, v1 : Vertex, v2 : Vertex):
        self.adjacents[v1].add(v2)
        self.adjacents[v2].add(v1)