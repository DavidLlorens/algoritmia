from collections.abc import Iterable
from typing import Union

from algoritmia.algorithms.traversers import bf_edge_traverser, dijkstra_edge_traverser, dijkstra_metric_edge_traverser
from algoritmia.datastructures.graphs import IGraph, Digraph, TVertex, TEdge, WeightingFunction
from algoritmia.utils import infinity

# Cinco algoritmos para obtener el camino más corto entre dos vertices de un grafo:
# - Tres basados en recorredores:
#   - shortest_path_unweighted_graph(): Para grafos no ponderados
#   - shortest_path_positive_weighted_graph(): Para grafos ponderados positivos (algoritmo de Dijkstra)
#   - shortest_path_metric_graph(): Para grafos métricos (algoritmo de Dijkstra modificado)
# - Dos que utilizan programación dinamica:
#   - shortest_path_acyclic_digraph(): Para digrafos ponderados acíclicos
#   - shortest_path_digraph()/bellman_ford(): Para digrafos ponderados sin ciclos negativos (algoritmo de Bellman-Ford)

# ----------------------------------------------------------------
# Tres algoritmos basados en recorredores
# ----------------------------------------------------------------

TPath = list[TVertex]  # Generic path


# Devuelve el camino más corto entre dos vértices en grafos no ponderados
# Coste temporal: O(|V| + |E|)
def shortest_path_unweighted_graph(g: IGraph[TVertex], v_source: TVertex, v_target: TVertex) -> TPath:
    edges = bf_edge_traverser(g, v_source)
    return path_recover(edges, v_target)


# Devuelve el camino más corto entre dos vértices en grafos ponderados positivos (algoritmo de Dijkstra)
# Coste temporal: O(|V|^2)
def shortest_path_positive_weighted_graph(g: IGraph[TVertex], d: WeightingFunction,
                                          v_source: TVertex, v_target: TVertex) -> TPath:
    edges = dijkstra_edge_traverser(g, d, v_source)  # Con diccionario: O(|V|^2)
    # edges = dijkstra_hm_edge_traverser(g, d, v_source)  # Con diccionario de prioridad: O(|V| + |E| log |V|)
    return path_recover(edges, v_target)


# Devuelve el camino más corto entre dos vértices en grafos métricos (algoritmo de Dijkstra modificado)
# Coste temporal: O(|V|^2)
# En la práctica es O(|V|) para grafos densos y O(sqrt(|V|)) para grafos dispersos.
def shortest_path_metric_graph(g: IGraph[TVertex], d: WeightingFunction,
                               v_source: TVertex, v_target: TVertex) -> TPath:
    edges = dijkstra_metric_edge_traverser(g, d, v_source, v_target)
    return path_recover(edges, v_target)


# Dada la lista de aristas que devuelve un recorredor y un vértice final,
# devuelve el camino desde el vértice inicial al final
# Coste temporal: O(|V|), porque los recorredores devuelven una arista por vértice: len(edges) = |V|
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


# ----------------------------------------------------------------
# Dos algoritmos de programación dinámica
# ----------------------------------------------------------------

Score = Union[int, float]
Decision = TVertex
Solution = tuple[Score, list[Decision]]
LParams = TVertex               # Para sp_acyclic_digraph()
LParams2 = tuple[TVertex, int]  # Para sp_digraph()/bellman_ford()


# Devuelve el camino más corto entre dos vértices en dígrafos ponderados acíclicos
# Coste temporal: O(|V| + |E|)
def shortest_path_acyclic_digraph(g: Digraph[TVertex],
                                  d: WeightingFunction[TVertex],
                                  v_initial: TVertex,
                                  v_final: TVertex) -> Solution:
    def L(v: TVertex) -> Score:
        if v == v_initial:
            return 0
        if v not in mem:
            res: list[tuple[Score, LParams]] = []
            for u in g.preds(v):
                c_score: Score = L(u) + d(u, v)
                previous: LParams = u
                # La decision, u, coincide con el previous
                res.append((c_score, previous))
            mem[v] = min(res, default=infinity)
        return mem[v][0]

    mem: dict[LParams, tuple[Score, LParams]] = {}
    score = L(v_final)
    if score == infinity:
        return score, []  # El vértice destino es inalcanzable desde el origen
    v0 = v_final
    sol: list[Decision] = [v0]
    while v0 != v_initial:
        _, v0 = mem[v0]
        sol.append(v0)
    sol.reverse()
    return score, sol


# Devuelve el camino más corto entre dos vértices en digrafos ponderados sin ciclos negativos
# Utiliza el algoritmo de Bellman-Ford (algoritmo de programación dinámica)
# Coste temporal: O(|V| |E|)
def shortest_path_digraph(g: Digraph[TVertex],
                          d: WeightingFunction[TVertex],
                          v_initial: TVertex,
                          v_final: TVertex) -> Solution:
    def L(v: TVertex, n: int) -> Score:
        if v == v_initial:
            return 0
        if n == 0:
            return infinity
        if (v, n) not in mem:
            res: list[tuple[Score, LParams2]] = []
            for u in g.preds(v):
                c_score: Score = L(u, n - 1) + d(u, v)
                previous: LParams2 = u, n - 1
                # La decision, u, se puede extraer del previous
                res.append((c_score, previous))
            mem[v, n] = min(res, default=infinity)
        return mem[v, n][0]

    mem: dict[LParams2, tuple[Score, LParams2]] = {}
    score: Score = L(v_final, len(g.V) - 1)
    if score == infinity:
        return score, []  # El vértice destino es inalcanzable desde el origen
    v0 = v_final
    n0 = len(g.V) - 1
    sol: list[Decision] = [v0]
    while v0 != v_initial:
        _, (v0, n0) = mem[v0, n0]
        sol.append(v0)
    sol.reverse()
    return score, sol


bellman_ford = shortest_path_digraph  # Creamos un alias para la función


# ----------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------

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
    v_initial0 = (0, 0)
    v_final0 = (1, 3)

    path0 = shortest_path_unweighted_graph(my_graph, v_initial0, v_final0)
    print('shortest_path_unweighted_graph:', path0)

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

    # Digraph without cycles ----------------------
    Vertex = int
    Edge = tuple[int, int]
    Weight = int

    d0: dict[Edge, Weight] = {(0, 1): 1, (0, 3): 50, (1, 2): 10, (2, 3): 3, (3, 4): 4}
    g0 = Digraph(E=d0.keys())
    wf0 = WeightingFunction((e for e in d0.items()))
    print('shortest_path_acyclic_digraph:', shortest_path_acyclic_digraph(g0, wf0, 0, 3))

    # DiGraph with cycles ----------------------
    d1: dict[Edge, Weight] = {(0, 1): 1, (0, 3): 50, (1, 2): 10, (2, 0): 2, (2, 3): -3, (3, 1): -2, (3, 2): 100,
                              (3, 4): 4}
    g1 = Digraph(E=d1.keys())
    wf1 = WeightingFunction((e for e in d1.items()))
    print('shortest_path_digraph:', shortest_path_digraph(g1, wf1, 3, 2))
