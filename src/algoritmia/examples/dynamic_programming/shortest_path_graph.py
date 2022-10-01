from typing import Union

from algoritmia.datastructures.graphs import Digraph, WeightingFunction, TVertex
from algoritmia.utils import infinity

Score = Union[int, float]
Decision = TVertex
Solution = tuple[Score, list[Decision]]
LParams = TVertex

# ----------------------------------------------------------------

# Shortest path in acyclic digraph
def sp_acyclic_digraph(g: Digraph[TVertex],
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
    v0 = v_final
    sol: list[Decision] = [v0]
    while v0 != v_initial:
        _, v0 = mem[v0]
        sol.append(v0)
    sol.reverse()
    return score, sol

# ----------------------------------------------------------------

LParams2 = tuple[TVertex, int]

# Shortest path in general digraph (can have cycles)
def sp_digraph(g: Digraph[TVertex],
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
        return score, []
    v0 = v_final
    n0 = len(g.V) - 1
    sol: list[Decision] = [v0]
    while v0 != v_initial:
        _, (v0, n0) = mem[v0, n0]
        sol.append(v0)
    sol.reverse()
    return score, sol


# ----------------------------------------------------------------


if __name__ == '__main__':
    Vertex = int
    Edge = tuple[int, int]
    Weight = int

    # Digraph without cycles ----------------------

    d0: dict[Edge, Weight] = {(0, 1): 1, (0, 3): 50, (1, 2): 10, (2, 3): 3, (3, 4): 4}
    g0 = Digraph(E=d0.keys())
    wf0 = WeightingFunction((e for e in d0.items()))

    print(sp_acyclic_digraph(g0, wf0, 0, 4))

    # DiGraph with cycles ----------------------

    d1: dict[Edge, Weight] = {(0, 1): 1, (0, 3): 50, (1, 2): 10, (2, 0): 2, (2, 3): -3, (3, 1): -2, (3, 2): 100, (3, 4): 4}
    g1 = Digraph(E=d1.keys())
    wf1 = WeightingFunction((e for e in d1.items()))

    print(sp_digraph(g1, wf1, 3, 2))
