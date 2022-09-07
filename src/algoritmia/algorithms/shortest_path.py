from typing import TypeVar, Iterable

from algoritmia.datastructures.graphs import IGraph, UndirectedGraph, WeightingFunction

from algoritmia.algorithms.traversers import bf_edge_traverser, dijkstra_edge_traverser, dijkstra_metric_edge_traverser

Vertex = TypeVar('Vertex')
Edge = tuple[Vertex, Vertex]
Path = list[Vertex]


def shortest_path_unweighted_graph(g: IGraph[Vertex], v_source: Vertex, v_target: Vertex) -> Path:
    edges = bf_edge_traverser(g, v_source)
    return path_recover(edges, v_target)


def shortest_path_positive_weighted_graph(g: IGraph[Vertex], d: WeightingFunction,
                                          v_source: Vertex, v_target: Vertex) -> Path:
    edges = dijkstra_edge_traverser(g, d, v_source)
    return path_recover(edges, v_target)


def shortest_path_metric_graph(g: IGraph[Vertex], d: WeightingFunction,
                               v_source: Vertex, v_target: Vertex) -> Path:
    edges = dijkstra_metric_edge_traverser(g, d, v_source, v_target)
    return path_recover(edges, v_target)


# Slide 37
def path_recover(edges: Iterable[Edge], v: Vertex) -> Path:
    # Creates backpointer dictionary (bp)
    bp = {}
    for o, d in edges:
        bp[d] = o
        if d == v:  # I have all I need
            break
    # Recover the path jumping back
    path = [v]
    while v != bp[v]:
        v = bp[v]
        path.append(v)
    # reverse the path
    path.reverse()
    return path


if __name__ == '__main__':
    # -------------
    # Output: [(0, 0), (0, 1), (1, 1), (1, 2), (0, 2), (0, 3), (1, 3)]

    my_edges = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((1, 1), (1, 2)),
                ((2, 0), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (2, 3)), ((0, 1), (1, 1)),
                ((0, 2), (1, 2)), ((0, 3), (1, 3)), ((1, 1), (2, 1)), ((1, 2), (2, 2))]
    my_graph = UndirectedGraph(E=my_edges)
    v_initial = (0, 0)
    v_final = (1, 3)

    path = shortest_path_unweighted_graph(my_graph, v_initial, v_final)
    print('shortest_path_unweighted_graph:', path)

    # ---------------
    # Output: ['Madrid', 'Venturada', 'Aranda de Duero', 'Lerma', 'Burgos', 'Miranda del Ebro', 'Armiñón', 'Basauri', 'Bilbao']

    from algoritmia.data.iberia import iberia, km

    path = shortest_path_positive_weighted_graph(iberia, km, 'Madrid', 'Bilbao')
    print('shortest_path_positive_weighted_graph:', path)

    from algoritmia.data.iberia import iberia2d, km2d, coords2d, coords2d_inv

    pathc = shortest_path_metric_graph(iberia2d, km2d, coords2d['Madrid'], coords2d['Bilbao'])
    path = [coords2d_inv[c] for c in pathc]
    print('shortest_path_metric_graph:', path)
