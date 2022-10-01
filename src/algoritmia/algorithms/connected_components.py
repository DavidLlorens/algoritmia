from collections.abc import Iterator

from algoritmia.algorithms.traversers import TVertexTraverser
from algoritmia.datastructures.graphs import UndirectedGraph, TVertex

TCC = list[TVertex]  # Generic Connected Component


def connected_components(g: UndirectedGraph[TVertex],
                         vertex_traverser: TVertexTraverser) -> Iterator[TCC]:
    pending_vertices = set(g.V)
    while len(pending_vertices) > 0:
        u = pending_vertices.pop()
        visited_vertices = list(vertex_traverser(g, u))
        pending_vertices -= set(visited_vertices)
        yield visited_vertices


if __name__ == '__main__':
    from traversers import bf_vertex_traverser, df_vertex_traverser
    Vertex = tuple[int, int]
    Edge = tuple[Vertex, Vertex]

    edges: list[Edge] = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)),
                         ((2, 2), (2, 3)), ((0, 1), (1, 1)), ((0, 2), (1, 2)),
                         ((1, 2), (2, 2)), ((2, 0), (2, 1)), ((0, 3), (1, 3))]

    my_graph = UndirectedGraph(E=edges)

    ccs_bf = list(connected_components(my_graph, bf_vertex_traverser))
    print("Breath first::", ccs_bf)

    ccs_df = list(connected_components(my_graph, df_vertex_traverser))
    print("Depth first:", ccs_df)
