from typing import *

from algoritmia.datastructures.graphs import Digraph, Vertex


def topological_sort(g: Digraph[Vertex]) -> list[Vertex]:
    def traverse_from(v):  # depthfirst postorder
        pending.remove(v)
        for suc in g.succs(v):
            if suc in pending:
                yield from traverse_from(suc)
        yield v

    def next_vertex_no_preds() -> Optional[Vertex]:
        for v in pending:
            if len(g.preds(v)) == 0: return v
        raise Exception("Incompatible graph")

    pending = set(g.V)
    lv = []
    while len(pending) > 0:
        u = next_vertex_no_preds()
        vertices = list(traverse_from(u))
        pending -= set(vertices)
        lv.extend(vertices)
    lv.reverse()
    return lv


if __name__ == '__main__':
    edges = [('C', 'C++'), ('C', 'Java'), ('C', 'Objective-C'), ('C', 'C#'),
             ('C++', 'Java'), ('C++', 'C#'),
             ('Java', 'C#'),
             ('MT', 'Haskell'), ('Haskell', 'C#')]

    my_graph = Digraph(E=edges)

    print(topological_sort(my_graph))
