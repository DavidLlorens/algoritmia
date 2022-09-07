from typing import *
from math import sqrt

from algoritmia.datastructures.graphs import IGraph, Vertex, Edge, WeightingFunction, Weight
from algoritmia.datastructures.queues import Fifo
from algoritmia.datastructures.prioritymaps import MinHeapMap
from algoritmia.utils import argmin, infinity

VertexTraverser = Callable[[IGraph, Vertex], Iterable[Vertex]]
EdgeTraverser = Callable[[IGraph, Vertex], Iterable[Edge]]


# Vertex traversers ----------------------------------------------------------------

def bf_vertex_traverser(graph: IGraph, v_initial: Vertex) -> Iterable[Vertex]:
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


def df_vertex_traverser(graph: IGraph, v_initial: Vertex) -> Iterable[Vertex]:
    def traverse_from(v: Vertex) -> Iterable[Vertex]:
        seen.add(v)
        yield v  # pre-order
        for suc in graph.succs(v):
            if suc not in seen:
                yield from traverse_from(suc)
        # yield v # post-order

    seen = set()
    yield from traverse_from(v_initial)


# Edge traversers ----------------------------------------------------------------

def bf_edge_traverser(graph: IGraph, v_initial: Vertex) -> Iterable[Edge]:
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


def df_edge_traverser(graph: IGraph, v_initial: Vertex) -> Iterable[Edge]:
    def traverse_from(u: Vertex, v: Vertex) -> Iterable[Edge]:
        seen.add(v)
        yield u, v  # pre-order
        for suc in graph.succs(v):
            if suc not in seen:
                yield from traverse_from(v, suc)
        # yield u, v # post-order

    seen = set()
    return traverse_from(v_initial, v_initial)


# Con diccionario: O(|V|^2)
def dijkstra_edge_traverser(g: IGraph, d: WeightingFunction,
                            v_initial: Vertex) -> Iterable[Edge]:
    D: dict[Vertex, Weight] = dict((v, infinity) for v in g.V)
    D[v_initial] = 0
    bp: dict[Vertex, Vertex] = {v_initial: v_initial}
    fixed: set[Vertex] = set()
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
def dijkstra_hm_edge_traverser(g: IGraph, d: WeightingFunction,
                               v_initial: Vertex) -> Iterable[Edge]:
    D: MinHeapMap[Vertex, Weight] = MinHeapMap((v, infinity) for v in g.V)  # O(|V|)
    D[v_initial] = 0
    bp: dict[Vertex, Vertex] = {v_initial: v_initial}
    fixed: set[Vertex] = set()
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


def dijkstra_metric_edge_traverser(g: IGraph, d: WeightingFunction,
                                   v_initial: Vertex, v_final: Vertex) -> Iterable[Edge]:
    D: dict[Vertex, Weight] = dict((v, infinity) for v in g.V)
    D[v_initial] = 0
    bp: dict[Vertex, Vertex] = {v_initial: v_initial}
    fixed: set[Vertex] = set()
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

    my_edges = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((0, 1), (0, 2)),
                ((2, 0), (1, 0)), ((2, 1), (2, 2)), ((2, 2), (2, 3)), ((0, 1), (1, 1)),
                ((0, 2), (1, 2)), ((0, 3), (1, 3)), ((1, 1), (2, 1)), ((1, 2), (2, 2))]

    my_graph = UndirectedGraph(E=my_edges)
    my_vertex_source = (0, 0)

    print('vertex_traverser_breadthfirst:', list(bf_vertex_traverser(my_graph, my_vertex_source)))
    print('edge_traverser_breadthfirst', list(bf_edge_traverser(my_graph, my_vertex_source)))

    print('vertex_traverser_depthfirst', list(df_vertex_traverser(my_graph, my_vertex_source)))
    print('edge_traverser_depthfirst', list(df_edge_traverser(my_graph, my_vertex_source)))

    # ---------------

    from algoritmia.data.mallorca import Mallorca, km

    print('edge_traverser_dijkstra', list(dijkstra_edge_traverser(Mallorca, km, 'Andratx')))
