from collections.abc import Iterator, Callable

from algoritmia.datastructures.graphs import IGraph, Edge, WeightingFunction, Weight
from algoritmia.datastructures.prioritymaps import MinHeapMap
from algoritmia.datastructures.queues import Fifo
from algoritmia.utils import argmin, infinity

type Traverse[T] = Callable[[IGraph[T], T], Iterator[Edge[T]]]


def traverse_bf[T](graph: IGraph[T],
                   v_initial: T) -> Iterator[Edge[T]]:
    queue: Fifo[Edge[T]] = Fifo()  # Cola de aristas
    seen: set[T] = set()  # Conjunto de vértices vistos
    queue.push((v_initial, v_initial))  # Añadimos la arista fantasma inicial
    seen.add(v_initial)
    while len(queue) > 0:
        u, v = queue.pop()
        yield u, v  # Generamos una arista
        for suc in graph.succs(v):
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)


def traverse_df[T](graph: IGraph[T],
                   v_initial: T,
                   preorder: bool = True) -> Iterator[Edge[T]]:
    def traverse_from(u: T, v: T) -> Iterator[Edge[T]]:
        seen.add(v)
        if preorder:
            yield u, v  # Generamos una arista (recorrido en preorden)
        for suc_v in graph.succs(v):
            if suc_v not in seen:
                yield from traverse_from(v, suc_v)
        if not preorder:
            yield u, v  # Generamos una arista (recorrido en postorden)

    seen: set[T] = set()
    return traverse_from(v_initial, v_initial)  # Arista fantasma inicial


# Con diccionario: O(|V|^2)
def traverse_dijkstra_dict[T](g: IGraph[T],
                              d: WeightingFunction[T],
                              v_initial: T) -> Iterator[Edge[T]]:
    D: dict[T, Weight] = dict((v, infinity) for v in g.V)
    D[v_initial] = 0
    bp: dict[T, T] = {v_initial: v_initial}
    fixed: set[T] = set()
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
def traverse_dijkstra_heapmap[T](g: IGraph[T],
                                 d: WeightingFunction[T],
                                 v_initial: T) -> Iterator[Edge[T]]:
    D: MinHeapMap[T, Weight] = MinHeapMap((v, infinity) for v in g.V)  # O(|V|)
    D[v_initial] = 0
    bp: dict[T, T] = {v_initial: v_initial}
    fixed: set[T] = set()
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
def traverse_dijkstra_metric_dict[T](g: IGraph[T],
                                     wf: WeightingFunction[T],
                                     eu_dist: Callable[[T, T], float],  # Function: Euclidean distance
                                     v_initial: T,
                                     v_final: T) -> Iterator[Edge[T]]:
    D: dict[T, Weight] = dict((v, infinity) for v in g.V)
    D[v_initial] = 0
    bp: dict[T, T] = {v_initial: v_initial}
    fixed: set[T] = set()
    while len(bp) > 0:
        v = argmin(bp.keys(), lambda u: D[u] + eu_dist(u, v_final))
        fixed.add(v)
        pred_v = bp[v]
        yield pred_v, v
        if v == v_final:
            break
        del bp[v]
        for suc_v in g.succs(v):
            if suc_v not in fixed and D[v] + wf(v, suc_v) < D[suc_v]:
                D[suc_v] = D[v] + wf(v, suc_v)
                bp[suc_v] = v


if __name__ == '__main__':
    from algoritmia.datastructures.graphs import UndirectedGraph

    type Vertex = tuple[int, int]

    my_edges = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((0, 1), (0, 2)),
                ((2, 0), (1, 0)), ((2, 1), (2, 2)), ((2, 2), (2, 3)), ((0, 1), (1, 1)),
                ((0, 2), (1, 2)), ((0, 3), (1, 3)), ((1, 1), (2, 1)), ((1, 2), (2, 2))]

    my_graph = UndirectedGraph(E=my_edges)
    initial_vertex = (0, 0)

    print('traverse_bf', list(traverse_bf(my_graph, initial_vertex)))
    print('traverse_df', list(traverse_df(my_graph, initial_vertex)))

    # ---------------------------------------------------------------------------------------

    from algoritmia.data.iberia import iberia, km, coords2d

    type Vertex = str  # Los vértices de iberia son nombres de ciudades

    traverse_from_Madrid = traverse_dijkstra_dict(iberia, km, 'Madrid')
    # Muestra solo los vértices:
    print('traverse_dijkstra_dict', [v for u, v in traverse_from_Madrid])


    def eu_dist0(city_a: Vertex, city_b: Vertex) -> float:
        pos2d_a, pos2d_b = coords2d[city_a], coords2d[city_b]
        dx, dy = pos2d_a[0] - pos2d_b[0], pos2d_a[1] - pos2d_b[1]
        return (dx * dx + dy * dy) ** 0.5


    Madrid_to_Bilbao = traverse_dijkstra_metric_dict(iberia, km, eu_dist0, 'Madrid', 'Bilbao')
    # Muestra solo los vértices:
    print('traverse_dijkstra_metric_dict', [v for u, v in Madrid_to_Bilbao])
