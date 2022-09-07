from algoritmia.datastructures.graphs import UndirectedGraph, WeightingFunction, Vertex
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.prioritymaps import MinHeapMap
from algoritmia.utils import argmin


# MST para grafos no diriguidos: kruslkal y prim
# Para grafos diriguidos ver algoritmo de Chu-Liu/Edmonds


def kruskal(g: UndirectedGraph[Vertex],
            d: WeightingFunction[Vertex]) -> UndirectedGraph[Vertex]:
    edges: list[tuple[Vertex, Vertex]] = []
    forest = MergeFindSet[Vertex]((v,) for v in g.V)
    n = 0
    for (u, v) in sorted(g.E, key=lambda e: d(e)):
        if forest.find(u) != forest.find(v):
            forest.merge(u, v)
            edges.append((u, v))
            n += 1
            if n == len(g.V) - 1:
                break
    return UndirectedGraph(E=edges)


# Use dict[Vertex, Vertex]
def prim_dic(g: UndirectedGraph[Vertex],
             d: WeightingFunction[Vertex]) -> UndirectedGraph[Vertex]:
    edges: list[tuple[Vertex, Vertex]] = []
    fixed: set[Vertex] = set()
    for u in g.V:
        if u not in fixed:
            fixed.add(u)
            bp = dict((v, u) for v in g.succs(u))
            while len(bp) > 0:
                (v, u) = argmin(bp.items(), d)
                del bp[v]
                fixed.add(v)
                edges.append((u, v))
                for w in g.succs(v):
                    if w in fixed: continue
                    if w not in bp or d(v, w) < d(bp[w], w):
                        bp[w] = v
    return UndirectedGraph(E=edges)


# Uses MinHeapMap[Vertex, tuple[Weight, Vertex]]
def prim(g: UndirectedGraph[Vertex],
         d: WeightingFunction[Vertex]) -> UndirectedGraph[Vertex]:
    edges: list[tuple[Vertex, Vertex]] = []
    fixed: set[Vertex] = set()
    for u in g.V:
        if u not in fixed:
            fixed.add(u)
            min_hm = MinHeapMap((v, (d(u, v), u)) for v in g.succs(u))
            while len(min_hm) > 0:
                (v, (_, u)) = min_hm.extract_opt_item()
                fixed.add(v)
                edges.append((u, v))
                for w in g.succs(v):
                    if w in fixed: continue
                    if w not in min_hm or d(v, w) < d(min_hm[w][1], w):
                        min_hm[w] = (d(v, w), v)
    return UndirectedGraph(E=edges)


if __name__ == '__main__':
    from algoritmia.data.mallorca import Mallorca, km

    mst_kruskal = kruskal(Mallorca, km)
    print(mst_kruskal)

    mst_prim_dic = prim_dic(Mallorca, km)
    print(mst_prim_dic)

    mst_prim = prim(Mallorca, km)
    print(mst_prim)
