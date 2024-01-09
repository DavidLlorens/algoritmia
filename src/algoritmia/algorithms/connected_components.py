from collections.abc import Iterator

from algoritmia.algorithms.traverse import Traverse
from algoritmia.datastructures.graphs import UndirectedGraph

type CC[T] = set[T]  # Connected Component

def connected_components[T](g: UndirectedGraph[T],
                            traverse: Traverse[T]) -> Iterator[CC]:
    pending_vertices = set(g.V)
    while len(pending_vertices) > 0:
        u = pending_vertices.pop()
        cc_vertices = set([v for (u, v) in traverse(g, u)])
        pending_vertices -= cc_vertices
        yield cc_vertices


if __name__ == '__main__':
    from traverse import traverse_bf, traverse_df

    edges = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)),
             ((2, 2), (2, 3)), ((0, 1), (1, 1)), ((0, 2), (1, 2)),
             ((1, 2), (2, 2)), ((2, 0), (2, 1)), ((0, 3), (1, 3))]

    my_graph = UndirectedGraph(E=edges)

    ccs_bf = list(connected_components(my_graph, traverse_bf))
    print("Breath first:", ccs_bf)

    ccs_df = list(connected_components(my_graph, traverse_df))
    print("Depth first:", ccs_df)
