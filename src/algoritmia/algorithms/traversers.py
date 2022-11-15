from collections.abc import Iterator, Callable
from math import sqrt

from algoritmia.datastructures.graphs import IGraph, TVertex, TEdge, WeightingFunction, Weight
from algoritmia.datastructures.prioritymaps import MinHeapMap
from algoritmia.datastructures.queues import Fifo
from algoritmia.utils import argmin, infinity

TVertexTraverser = Callable[[IGraph[TVertex], TVertex], Iterator[TVertex]]
TEdgeTraverser = Callable[[IGraph[TVertex], TVertex], Iterator[TEdge]]


# Vertex traversers ----------------------------------------------------------------

def bf_vertex_traverser(graph: IGraph[TVertex],
                        v_initial: TVertex) -> Iterator[TVertex]:
    queue = Fifo()
    seen = set()
    queue.push(v_initial)
    seen.add(v_initial)
    while len(queue) > 0:
        v = queue.pop()
        yield v
        for suc in graph.succs(v):
            if suc not in seen:
                queue.push(suc)
                seen.add(suc)


def df_vertex_traverser(graph: IGraph[TVertex],
                        v_initial: TVertex) -> Iterator[TVertex]:
    def traverse_from(v: TVertex) -> Iterator[TVertex]:
        seen.add(v)
        yield v  # pre-order
        for suc in graph.succs(v):
            if suc not in seen:
                yield from traverse_from(suc)
        # yield v # post-order

    seen = set()
    yield from traverse_from(v_initial)


# Edge traversers ----------------------------------------------------------------

def bf_edge_traverser(graph: IGraph[TVertex],
                      v_initial: TVertex) -> Iterator[TEdge]:
    queue = Fifo()
    seen = set()
    queue.push((v_initial, v_initial))
    seen.add(v_initial)
    while len(queue) > 0:
        u, v = queue.pop()
        yield u, v
        for suc in graph.succs(v):
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)


def df_edge_traverser(graph: IGraph[TVertex],
                      v_initial: TVertex) -> Iterator[TEdge]:
    def traverse_from(u: TVertex, v: TVertex) -> Iterator[TEdge]:
        seen.add(v)
        yield u, v  # pre-order
        for suc in graph.succs(v):
            if suc not in seen:
                yield from traverse_from(v, suc)
        # yield u, v # post-order

    seen = set()
    return traverse_from(v_initial, v_initial)


# Con diccionario: O(|V|^2)
def dijkstra_edge_traverser(g: IGraph[TVertex],
                            d: WeightingFunction[TVertex],
                            v_initial: TVertex) -> Iterator[TEdge]:
    D: dict[TVertex, Weight] = dict((v, infinity) for v in g.V)
    D[v_initial] = 0
    bp: dict[TVertex, TVertex] = {v_initial: v_initial}
    fixed: set[TVertex] = set()
    while len(bp) > 0:  # O(|V|) veces
        v = argmin(bp.keys(), lambda u: D[u])  # O(|V|)
        fixed.add(v)
        pred_v = bp[v]
        yield pred_v, v
        del bp[v]
        for suc_v in g.succs(v):  # O(|V|)
            if suc_v not in fixed and D[v] + d(v, suc_v) < D[suc_v]:
                D[suc_v] = D[v] + d(v, suc_v)
                bp[suc_v] = v


# Con diccionario de prioridad: O(|V| + |E| log |V|)
def dijkstra_hm_edge_traverser(g: IGraph[TVertex],
                               d: WeightingFunction[TVertex],
                               v_initial: TVertex) -> Iterator[TEdge]:
    D: MinHeapMap[TVertex, Weight] = MinHeapMap((v, infinity) for v in g.V)  # O(|V|)
    D[v_initial] = 0
    bp: dict[TVertex, TVertex] = {v_initial: v_initial}
    fixed: set[TVertex] = set()
    while len(D) > 0:
        v, dv = D.extract_opt_item()  # O(log |V|), O(|V|) veces
        fixed.add(v)
        pred_v = bp[v]
        yield pred_v, v
        for suc_v in g.succs(v):
            if suc_v not in fixed and dv + d(v, suc_v) < D[suc_v]:
                D[suc_v] = dv + d(v, suc_v)  # O(log |V|), O(|E|) veces
                bp[suc_v] = v


# Distancia euclídea
def d_eu(u, v):
    a = u[0] - v[0]
    b = u[1] - v[1]
    return sqrt(a * a + b * b)


# Con diccionario: O(|V|^2)
# En la práctica el coste es O(|V|) para grafos densos y O(sqrt(|V|) para grafos dispersos.
def dijkstra_metric_edge_traverser(g: IGraph[TVertex],
                                   d: WeightingFunction[TVertex],
                                   v_initial: TVertex, v_final: TVertex) -> Iterator[TEdge]:
    D: dict[TVertex, Weight] = dict((v, infinity) for v in g.V)
    D[v_initial] = 0
    bp: dict[TVertex, TVertex] = {v_initial: v_initial}
    fixed: set[TVertex] = set()
    while len(bp) > 0:
        v = argmin(bp.keys(), lambda u: D[u] + d_eu(u, v_final))
        fixed.add(v)
        pred_v = bp[v]
        yield pred_v, v
        if v == v_final:
            break
        del bp[v]
        for suc_v in g.succs(v):
            if suc_v not in fixed and D[v] + d(v, suc_v) < D[suc_v]:
                D[suc_v] = D[v] + d(v, suc_v)
                bp[suc_v] = v


if __name__ == '__main__':
    from algoritmia.datastructures.graphs import UndirectedGraph

    Vertex = tuple[int, int]
    Edge = tuple[Vertex, Vertex]

    my_edges = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((0, 1), (0, 2)),
                ((2, 0), (1, 0)), ((2, 1), (2, 2)), ((2, 2), (2, 3)), ((0, 1), (1, 1)),
                ((0, 2), (1, 2)), ((0, 3), (1, 3)), ((1, 1), (2, 1)), ((1, 2), (2, 2))]

    my_graph = UndirectedGraph[Vertex](E=my_edges)
    my_vertex_source = (0, 0)

    print('vertex_traverser_breadthfirst:', list(bf_vertex_traverser(my_graph, my_vertex_source)))
    print('edge_traverser_breadthfirst', list(bf_edge_traverser(my_graph, my_vertex_source)))

    print('vertex_traverser_depthfirst', list(df_vertex_traverser(my_graph, my_vertex_source)))
    print('edge_traverser_depthfirst', list(df_edge_traverser(my_graph, my_vertex_source)))

    # ---------------

    from algoritmia.data.mallorca import Mallorca, km

    print('edge_traverser_dijkstra', list(dijkstra_edge_traverser(Mallorca, km, 'Andratx')))
