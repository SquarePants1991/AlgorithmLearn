class Graph:

    def __init__(self):
        self.relationships = {}

    def add_vertex(self, vertex):
        vertices = self.relationships.keys()
        if vertex in vertices:
            return False
        self.relationships[vertex] = []
        return True

    def add_edge(self, begin, end):
        vertices = self.relationships.keys()
        if begin in vertices and end in vertices:
            self.relationships[begin].append(end)
            self.relationships[end].append(begin)
            return True
        return False

    def adj(self, vertex):
        return self.relationships[vertex]

    def vertex_count(self):
        return len(self.relationships.keys())

    def edge_count(self):
        edges = 0
        for vertex in self.relationships.keys():
            edges += len(self.relationships[vertex])
        return edges / 2

    def to_string(self):
        output = str.format('Vertices: {0}\nEdges: {1}\n', self.vertex_count(), self.edge_count())
        for vertex in self.relationships.keys():
            output += str.format('{0} {1}\n', vertex, self.relationships[vertex])
        return output


class Search:
    def __init__(self, graph, start):
        self.marked = {}
        self.edgeTo = {}
        self.graph = graph
        self.start = start
        self._broad_first_search(self.start, self.marked)

    def _deep_first_search(self, start, marked):
        marked[start] = True
        for vertex in self.graph.adj(start):
            if vertex not in marked:
                self.edgeTo[vertex] = start
                self._deep_first_search(vertex, marked)

    def _broad_first_search(self, start, marked):
        queue = [start]
        while len(queue) > 0:
            start_vertex = queue[0]
            del queue[0]
            for vertex in self.graph.adj(start_vertex):
                if vertex not in marked:
                    marked[vertex] = True
                    self.edgeTo[vertex] = start_vertex
                    queue.append(vertex)

    def connected(self, target):
        return target in self.marked

    def count(self):
        return len(self.marked.keys()) - 1

    def path_to(self, target):
        if self.connected(target) is False:
            return []
        path = []
        vertex = target
        while True:
            path.append(vertex)
            if vertex == self.start:
                break
            vertex = self.edgeTo[vertex]
        path.reverse()
        return path

class Cycle:
    def __init__(self, graph, start):
        self.marked = {}
        self.graph = graph
        self.has_cycle = False
        self._deep_first_search(start, start, self.marked)

    def _deep_first_search(self, start, parent, marked):
        marked[start] = True
        for vertex in self.graph.adj(start):
            if vertex not in marked:
                self._deep_first_search(vertex, start, marked)
            elif vertex != parent:
                self.has_cycle = True

    def cycle_exist(self):
        return self.has_cycle


class TowColorable:
    def __init__(self, graph, start):
        self.marked = {}
        self.graph = graph
        self.tow_colorable = True
        self.colors = {}
        self.colors[start] = True
        self._deep_first_search(start, self.marked)

    def _deep_first_search(self, start, marked):
        marked[start] = True
        for vertex in self.graph.adj(start):
            if vertex not in marked:
                self.colors[vertex] = not self.colors[start]
                self._deep_first_search(vertex, marked)
            elif self.colors[vertex] == self.colors[start]:
                self.tow_colorable = False

    def can_two_colored(self):
        return self.tow_colorable



if __name__ == '__main__':
    graph = Graph()
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(2, 4)
    graph.add_edge(1, 5)
    print(graph.to_string())

    search = Search(graph, 1)
    print(search.connected(4))
    print(search.count())
    print(search.path_to(5))

    graph_has_cycle = Graph()
    graph_has_cycle.add_vertex(1)
    graph_has_cycle.add_vertex(2)
    graph_has_cycle.add_vertex(3)
    graph_has_cycle.add_edge(1, 2)
    graph_has_cycle.add_edge(2, 3)
    graph_has_cycle.add_edge(3, 2)
    cycle = Cycle(graph_has_cycle, 1)
    print(cycle.cycle_exist())

    graph_two_color = Graph()
    graph_two_color.add_vertex(1)
    graph_two_color.add_vertex(2)
    graph_two_color.add_vertex(3)
    graph_two_color.add_vertex(4)
    graph_two_color.add_edge(1, 2)
    graph_two_color.add_edge(2, 3)
    graph_two_color.add_edge(3, 4)
    graph_two_color.add_edge(4, 1)

    tow_colored = TowColorable(graph_two_color, 1)
    print(tow_colored.can_two_colored())