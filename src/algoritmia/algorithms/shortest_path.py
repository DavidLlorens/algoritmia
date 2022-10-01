from collections.abc import Iterable

from algoritmia.algorithms.traversers import bf_edge_traverser, dijkstra_edge_traverser, dijkstra_metric_edge_traverser
from algoritmia.datastructures.graphs import IGraph, TVertex, TEdge, WeightingFunction

TPath = list[TVertex]  # Generic path


def shortest_path_unweighted_graph(g: IGraph[TVertex], v_source: TVertex, v_target: TVertex) -> TPath:
    edges = bf_edge_traverser(g, v_source)
    return path_recover(edges, v_target)


def shortest_path_positive_weighted_graph(g: IGraph[TVertex], d: WeightingFunction,
                                          v_source: TVertex, v_target: TVertex) -> TPath:
    edges = dijkstra_edge_traverser(g, d, v_source)
    return path_recover(edges, v_target)


def shortest_path_metric_graph(g: IGraph[TVertex], d: WeightingFunction,
                               v_source: TVertex, v_target: TVertex) -> TPath:
    edges = dijkstra_metric_edge_traverser(g, d, v_source, v_target)
    return path_recover(edges, v_target)


def path_recover(edges: Iterable[TEdge], v: TVertex) -> TPath:
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

    from algoritmia.datastructures.graphs import UndirectedGraph

    Vertex = tuple[int, int]
    Edge = tuple[Vertex, Vertex]

    my_edges: list[Edge] = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((1, 1), (1, 2)),
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

    spath = shortest_path_positive_weighted_graph(iberia, km, 'Madrid', 'Bilbao')
    print('shortest_path_positive_weighted_graph:', spath)

    # ---------------
    # Output: ['Madrid', 'Venturada', 'Aranda de Duero', 'Lerma', 'Burgos', 'Miranda del Ebro', 'Armiñón', 'Basauri', 'Bilbao']

    from algoritmia.data.iberia import iberia2d, km2d, coords2d, coords2d_inv

    spath_mg = shortest_path_metric_graph(iberia2d, km2d, coords2d['Madrid'], coords2d['Bilbao'])
    psath = [coords2d_inv[c] for c in spath_mg]
    print('shortest_path_metric_graph:', spath)
