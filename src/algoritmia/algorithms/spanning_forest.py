from collections.abc import Iterator

from algoritmia.algorithms.traverse import Traverse
from algoritmia.datastructures.graphs import UndirectedGraph


def spanning_forest[T](g: UndirectedGraph[T], traverser: Traverse[T]) -> Iterator[UndirectedGraph]:
    pending_vertices = set(g.V)
    while len(pending_vertices) > 0:
        u = pending_vertices.pop()
        e_gen = iter(traverser(g, u))
        next(e_gen)  # skip phantom edge
        visited_edges = list(e_gen)
        pending_vertices -= set([v for (u, v) in visited_edges])
        yield UndirectedGraph(E=list(visited_edges))


if __name__ == '__main__':
    from traverse import traverse_bf, traverse_df

    type Vertex = tuple[int, int]

    edges = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((2, 0), (2, 1)),
             ((2, 2), (2, 3)), ((0, 1), (1, 1)), ((0, 2), (1, 2)), ((0, 3), (1, 3)),
             ((1, 2), (2, 2))]

    my_graph = UndirectedGraph(E=edges)

    print("Breath first:")
    graphs_bf = list(spanning_forest(my_graph, traverse_bf))
    for g0 in graphs_bf:
        print(g0)

    print("Depth first:")
    graphs_df = list(spanning_forest(my_graph, traverse_df))
    for g0 in graphs_df:
        print(g0)
