from collections.abc import Iterable, Callable

from algoritmia.algorithms.traverse import traverse_bf, traverse_dijkstra_dict, traverse_dijkstra_metric_dict
from algoritmia.datastructures.graphs import IGraph, Digraph, Edge, WeightingFunction
from algoritmia.utils import infinity

# Cinco algoritmos para obtener el camino más corto entre dos vertices de un grafo:
# - Tres basados en recorredores:
#   - shortest_path_unweighted_graph(): Para grafos no ponderados
#   - shortest_path_positive_weighted_graph(): Para grafos ponderados positivos (algoritmo de Dijkstra)
#   - shortest_path_metric_graph(): Para grafos métricos (algoritmo de Dijkstra modificado)
# - Dos que utilizan programación dinamica:
#   - shortest_path_acyclic_digraph(): Para digrafos ponderados acíclicos
#   - shortest_path_digraph()/bellman_ford(): Para digrafos ponderados sin ciclos negativos (algoritmo de Bellman-Ford)

type Path[T] = list[T]  # T es el tipo de los vértices


# ----------------------------------------------------------------
# Tres algoritmos basados en recorredores
# ----------------------------------------------------------------


# Devuelve el camino más corto entre dos vértices en grafos no ponderados
# Coste temporal: O(|V| + |E|)
def shortest_path_unweighted_graph[T](g: IGraph[T], v_source: T, v_target: T) -> Path[T]:
    edges = traverse_bf(g, v_source)
    return path_recover(edges, v_target)


# Devuelve el camino más corto entre dos vértices en grafos ponderados positivos (algoritmo de Dijkstra)
# Coste temporal: O(|V|^2)
def shortest_path_positive_weighted_graph[T](g: IGraph[T], d: WeightingFunction,
                                             v_source: T, v_target: T) -> Path[T]:
    edges = traverse_dijkstra_dict(g, d, v_source)  # Con diccionario: O(|V|^2)
    # edges = traverse_dijkstra_heapmap(g, d, v_source)  # Con diccionario de prioridad: O(|V| + |E| log |V|)
    return path_recover(edges, v_target)


# Devuelve el camino más corto entre dos vértices en grafos métricos (algoritmo de Dijkstra modificado)
# Coste temporal: O(|V|^2)
# En la práctica es O(|V|) para grafos densos y O(sqrt(|V|)) para grafos dispersos.
def shortest_path_metric_graph[T](g: IGraph[T], d: WeightingFunction,
                                  dist: Callable[[T, T], float],
                                  v_source: T, v_target: T) -> Path[T]:
    edges = traverse_dijkstra_metric_dict(g, d, dist, v_source, v_target)
    return path_recover(edges, v_target)


# Dada la lista de aristas que devuelve un recorredor y un vértice final,
# devuelve el camino desde el vértice inicial al final
# Coste temporal: O(|V|), porque los recorredores devuelven una arista por vértice: len(edges) = |V|
def path_recover[T](edges: Iterable[Edge[T]], v: T) -> Path[T]:
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

# En este problema, una decisión es un vértice, por lo tanto, su tipo es T (el genérico del grafo)
# Decision = T
type Solution[T] = list[T]

type Score = int | float
type ScoredSolution[T] = tuple[Score, Solution[T]]

type SParams[T] = T  # Para sp_acyclic_digraph()
type SParams2[T] = tuple[T, int]  # Para sp_digraph()/bellman_ford()


# Devuelve el camino más corto entre dos vértices en dígrafos ponderados acíclicos
# Coste temporal: O(|V| + |E|)
def shortest_path_acyclic_digraph[T](g: Digraph[T],
                                     d: WeightingFunction[T],
                                     v_initial: T,
                                     v_final: T) -> ScoredSolution[T]:
    def S(v: T) -> Score:
        if v == v_initial:
            return 0
        if v not in mem:
            res: list[tuple[Score, SParams]] = []
            for u in g.preds(v):
                c_score: Score = S(u) + d(u, v)
                previous: SParams = u
                # La decision, u, coincide con el previous
                res.append((c_score, previous))
            mem[v] = min(res, default=infinity)
        return mem[v][0]

    mem: dict[SParams, tuple[Score, SParams]] = {}
    score = S(v_final)
    if score == infinity:
        return score, []  # El vértice destino es inalcanzable desde el origen
    v0 = v_final
    sol: list[T] = [v0]
    while v0 != v_initial:
        _, v0 = mem[v0]
        sol.append(v0)
    sol.reverse()
    return score, sol


# Devuelve el camino más corto entre dos vértices en digrafos ponderados sin ciclos negativos
# Utiliza el algoritmo de Bellman-Ford (algoritmo de programación dinámica)
# Coste temporal: O(|V| |E|)
def shortest_path_digraph[T](g: Digraph[T],
                             d: WeightingFunction[T],
                             v_initial: T,
                             v_final: T) -> ScoredSolution[T]:
    def S(v: T, n: int) -> Score:
        if v == v_initial:
            return 0
        if n == 0:
            return infinity
        if (v, n) not in mem:
            res: list[tuple[Score, SParams2]] = []
            for u in g.preds(v):
                c_score: Score = S(u, n - 1) + d(u, v)
                previous: SParams2 = u, n - 1
                # La decision, u, se puede extraer del previous
                res.append((c_score, previous))
            mem[v, n] = min(res, default=infinity)
        return mem[v, n][0]

    mem: dict[SParams2, tuple[Score, SParams2]] = {}
    score: Score = S(v_final, len(g.V) - 1)
    if score == infinity:
        return score, []  # El vértice destino es inalcanzable desde el origen
    v0 = v_final
    n0 = len(g.V) - 1
    sol: list[T] = [v0]
    while v0 != v_initial:
        _, (v0, n0) = mem[v0, n0]
        sol.append(v0)
    sol.reverse()
    return score, sol


bellman_ford = shortest_path_digraph  # Creamos un alias para la función


def example_shortest_path_unweighted_graph():
    # Output: [(0, 0), (0, 1), (1, 1), (1, 2), (0, 2), (0, 3), (1, 3)]
    from algoritmia.datastructures.graphs import UndirectedGraph

    type Vertex = tuple[int, int]

    edges = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((1, 1), (1, 2)),
             ((2, 0), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (2, 3)), ((0, 1), (1, 1)),
             ((0, 2), (1, 2)), ((0, 3), (1, 3)), ((1, 1), (2, 1)), ((1, 2), (2, 2))]
    g = UndirectedGraph[Vertex](E=edges)
    v_initial0 = (0, 0)
    v_final0 = (1, 3)
    print('shortest_path_unweighted_graph:', shortest_path_unweighted_graph(g, v_initial0, v_final0))


def example_shortest_path_positive_weighted_graph():
    from algoritmia.data.iberia import iberia, km

    print('shortest_path_positive_weighted_graph:',
          shortest_path_positive_weighted_graph(iberia, km, 'Madrid', 'Bilbao'))


def example_shortest_path_metric_graph():
    from algoritmia.data.iberia import iberia, km, coords2d

    def eu_dist0(city_a: str, city_b: str) -> float:
        pos2d_a, pos2d_b = coords2d[city_a], coords2d[city_b]
        dx, dy = pos2d_a[0] - pos2d_b[0], pos2d_a[1] - pos2d_b[1]
        return (dx * dx + dy * dy) ** 0.5

    print('shortest_path_metric_graph:', shortest_path_metric_graph(iberia, km, eu_dist0, 'Madrid', 'Bilbao'))


def example_shortest_path_acyclic_digraph():
    data = {(0, 1): 1, (0, 3): 50, (1, 2): 10, (2, 3): 3, (3, 4): 4}
    g = Digraph(E=data.keys())
    wf = WeightingFunction(data)
    print('shortest_path_acyclic_digraph:', shortest_path_acyclic_digraph(g, wf, 0, 3))


def example_shortest_path_digraph():
    data = {(0, 1): 1, (0, 3): 50, (1, 2): 10, (2, 0): 2,
            (2, 3): -3, (3, 1): -2, (3, 2): 100, (3, 4): 4}
    g = Digraph(E=data.keys())
    wf = WeightingFunction(data)
    print('shortest_path_digraph:', shortest_path_digraph(g, wf, 3, 2))


# ----------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------


if __name__ == '__main__':
    example_shortest_path_unweighted_graph()
    example_shortest_path_positive_weighted_graph()
    example_shortest_path_metric_graph()
    example_shortest_path_acyclic_digraph()
    example_shortest_path_digraph()
