import sys, os

def __init__():
    cur_file_path = os.path.realpath(__file__) # Get current file abspath
    cur_file_location_path = os.path.dirname(cur_file_path) # Get current file's location abspath
    tmp_path = cur_file_location_path
    rel_path_list = []
    while True:
        tmp_path, x = os.path.split(tmp_path)
        if x == 'src':
            break
        rel_path_list.append('..')
    rel_path = os.path.join(cur_file_location_path, *rel_path_list)
    abs_path = os.path.abspath(rel_path)
    sys.path.append(abs_path)

__init__()

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