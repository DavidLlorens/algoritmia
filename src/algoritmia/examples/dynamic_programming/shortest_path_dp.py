from algoritmia.datastructures.graphs import Digraph, WeightingFunction
from algoritmia.utils import infinity


def solve(g: Digraph, d: WeightingFunction, s, t) -> tuple[int, list[int]]:
    def L(v) -> int:
        if v == s:
            return 0
        if v not in mem:
            mem[v] = min((L(u) + d(u, v), u) for u in g.preds(v))
        return mem[v][0]

    mem = {}
    score = L(t)
    v = t
    sol = [v]
    while v != s:
        _, v = mem[v]
        sol.append(v)
    sol.reverse()
    return score, sol


def solve2(g: Digraph, d: WeightingFunction, s, t) -> tuple[int, list[int]]:
    def L(v, n) -> int:
        if v == s:
            return 0
        if n == 0:
            return infinity
        if (v, n) not in mem:
            mem[v, n] = min((L(u, n - 1) + d(u, v), (u, n - 1)) for u in g.preds(v))
        return mem[v, n][0]

    mem = {}
    score = L(t, len(g.V) - 1)
    if score == infinity:
        return score, []
    v = t
    n = len(g.V) - 1
    sol = [v]
    while v != s:
        _, (v, n) = mem[v, n]
        sol.append(v)
    sol.reverse()
    return score, sol


if __name__ == '__main__':
    d = {(0, 1): 1, (0, 3): 50, (1, 2): 10, (2, 0): 2, (2, 3): -3, (3, 1): -2, (3, 2): 100, (3, 4): 4}
    my_edges = d.keys()
    g = Digraph(E=my_edges)
    wf = WeightingFunction((e for e in d.items()))

    print(solve2(g, wf, 3, 2))
