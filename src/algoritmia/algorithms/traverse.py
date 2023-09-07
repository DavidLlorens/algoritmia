from collections.abc import Iterator, Callable

from algoritmia.datastructures.graphs import IGraph, TVertex, TEdge, WeightingFunction, Weight
from algoritmia.datastructures.prioritymaps import MinHeapMap
from algoritmia.datastructures.queues import Fifo
from algoritmia.utils import argmin, infinity

Traverse = Callable[[IGraph[TVertex], TVertex], Iterator[TEdge]]

def traverse_bf(graph: IGraph[TVertex],
                v_initial: TVertex) -> Iterator[TEdge]:
    queue: Fifo[TEdge] = Fifo()         # Cola de aristas
    seen: set[TVertex] = set()          # Conjunto de vértices vistos
    queue.push((v_initial, v_initial))  # Añadimos la arista fantasma inicial
    seen.add(v_initial)
    while len(queue) > 0:
        u, v = queue.pop()
        yield u, v                      # Generamos una arista
        for suc in graph.succs(v):
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)

def traverse_df(graph: IGraph[TVertex],
                v_initial: TVertex,
                preorder: bool = True) -> Iterator[TEdge]:
    def traverse_from(u: TVertex, v: TVertex) -> Iterator[TEdge]:
        seen.add(v)
        if preorder:
            yield u, v  # Generamos una arista (recorrido en preorden)
        for suc_v in graph.succs(v):
            if suc_v not in seen:
                yield from traverse_from(v, suc_v)
        if not preorder:
            yield u, v  # Generamos una arista (recorrido en postorden)

    seen: set[TVertex] = set()
    return traverse_from(v_initial, v_initial)  # Arista fantasma inicial

# Con diccionario: O(|V|^2)
def traverse_dijkstra_dict(g: IGraph[TVertex],
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
def traverse_dijkstra_heapmap(g: IGraph[TVertex],
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

# Con diccionario: O(|V|^2)
# En la práctica el coste es O(|V|) para grafos densos y O(sqrt(|V|) para grafos dispersos.
def traverse_dijkstra_metric_dict(g: IGraph[TVertex],
                                  d: WeightingFunction[TVertex],
                                  dist: Callable[[TVertex, TVertex], float],  # Function: Euclidean distance
                                  v_initial: TVertex,
                                  v_final: TVertex) -> Iterator[TEdge]:
    D: dict[TVertex, Weight] = dict((v, infinity) for v in g.V)
    D[v_initial] = 0
    bp: dict[TVertex, TVertex] = {v_initial: v_initial}
    fixed: set[TVertex] = set()
    while len(bp) > 0:
        v = argmin(bp.keys(), lambda u: D[u] + dist(u, v_final))
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
    initial_vertex = (0, 0)

    print('traverse_bf', list(traverse_bf(my_graph, initial_vertex)))
    print('traverse_df', list(traverse_df(my_graph, initial_vertex)))

    # ---------------

    from algoritmia.data.iberia import iberia, km, coords2d
    print('traverse_dijkstra_dict', list(traverse_dijkstra_dict(iberia, km, 'Madrid')))

    # ---------------

    def dist(c1, c2):
        u, v = coords2d[c1], coords2d[c2]
        a,b = u[0] - v[0], u[1] - v[1]
        return (a * a + b * b)**0.5

    print('traverse_dijkstra_metric_dict', list(traverse_dijkstra_metric_dict(iberia, km, dist, 'Madrid', 'Bilbao')))
