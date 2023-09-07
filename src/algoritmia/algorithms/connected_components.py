from collections.abc import Iterator

from algoritmia.algorithms.traverse import Traverse
from algoritmia.datastructures.graphs import UndirectedGraph, TVertex

TCC = list[TVertex]  # Generic Connected Component

def connected_components(g: UndirectedGraph[TVertex],
                         traverse: Traverse) -> Iterator[TCC]:
    pending_vertices = set(g.V)
    while len(pending_vertices) > 0:
        u = pending_vertices.pop()
        visited_vertices = [v for (u, v) in traverse(g, u)]
        pending_vertices -= set(visited_vertices)
        yield visited_vertices


if __name__ == '__main__':
    from traverse import traverse_bf, traverse_df
    Vertex = tuple[int, int]
    Edge = tuple[Vertex, Vertex]

    edges: list[Edge] = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)),
                         ((2, 2), (2, 3)), ((0, 1), (1, 1)), ((0, 2), (1, 2)),
                         ((1, 2), (2, 2)), ((2, 0), (2, 1)), ((0, 3), (1, 3))]

    my_graph = UndirectedGraph(E=edges)

    ccs_bf = list(connected_components(my_graph, traverse_bf))
    print("Breath first:", ccs_bf)

    ccs_df = list(connected_components(my_graph, traverse_df))
    print("Depth first:", ccs_df)
