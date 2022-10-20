from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from algoritmia.datastructures.graphs import UndirectedGraph, TVertex, WeightingFunction
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve
from algoritmia.schemes.bt_scheme import ScoredDecisionSequence, bt_min_solve

Decision = TVertex
Score = float

# 'bt_solve' y 'bt_vc_solve' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'DecisionSequence', cuya implementación por defecto devuelve una tupla con las decisiones:
SolutionDS = tuple[Decision, ...]

# 'bt_min_solve' y 'bt_max_solve' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'ScoredDecisionSequence', cuya implementación por defecto devuelve una tupla de dos elementos:
# el Score y una tupla con las decisones:
SolutionSDS = tuple[Score, tuple[Decision, ...]]


def hamiltoniancycle_solve(graph: UndirectedGraph[TVertex]) -> Iterator[SolutionDS]:
    class HamiltonianCycleDS(DecisionSequence[TVertex]):
        def is_solution(self) -> bool:
            ds = self.decisions()
            return len(ds) == len(graph.V) and ds[0] in graph.succs(ds[-1])

        def successors(self) -> Iterator[HamiltonianCycleDS]:
            ds = self.decisions()
            if len(ds) < len(graph.V):
                for v in graph.succs(ds[-1]):
                    if v not in ds:
                        yield self.add_decision(v)

    v_initial = next(iter(graph.V))  # Para coger un elemento de un conjunto sin sacarlo
    initial_ds = HamiltonianCycleDS().add_decision(v_initial)
    return bt_solve(initial_ds)


def hamiltoniancycle_opt_solve(graph: UndirectedGraph[TVertex],
                               wf: WeightingFunction[TVertex]) -> Iterator[SolutionSDS]:
    @dataclass
    class Extra:
        ls: int = 0

    class HamiltonianCycleDS(ScoredDecisionSequence[TVertex]):
        def is_solution(self) -> bool:
            ds = self.decisions()
            return len(ds) == len(graph.V) and ds[0] in graph.succs(ds[-1])

        def successors(self) -> Iterator[HamiltonianCycleDS]:
            ds = self.decisions()
            if len(ds) < len(graph.V):
                for v in graph.succs(ds[-1]):
                    if v not in ds:
                        new_extra = Extra(self.extra.ls + wf(ds[-1], v))
                        yield self.add_decision(v, new_extra)

        # Sobreescribimos 'state()'
        def state(self) -> tuple[TVertex, tuple[Vertex, ...]]:
            ds = list(self.decisions())
            return ds[-1], tuple(sorted(ds))

        def score(self) -> float:
            if len(self) < len(graph.V): return self.extra.ls
            ds = self.decisions()
            if ds[0] in graph.succs(ds[-1]):
                return self.extra.ls + wf(ds[0], ds[-1])
            return float('infinity')

    v_initial = next(iter(graph.V))  # Para coger un elemento de un conjunto sin sacarlo
    initial_ds = HamiltonianCycleDS(Extra()).add_decision(v_initial, Extra())
    return bt_min_solve(initial_ds)


# Programa principal ---------------------------
if __name__ == "__main__":
    Vertex = int
    Edge = tuple[Vertex, Vertex]
    edges: list[Edge] = [(0, 2), (0, 3), (0, 9), (1, 3), (1, 4), (1, 8), (2, 3), (2, 5), (3, 4),
                         (3, 6), (4, 7), (5, 6), (5, 8), (6, 7), (6, 8), (6, 9)]
    g = UndirectedGraph(E=edges)

    print('Basic versión (all solutions):')
    has_solutions = False
    for sol in hamiltoniancycle_solve(g):
        has_solutions = True
        print(f'\tSolution: {sol}')
    if not has_solutions:
        print('\tThere are no solutions')

    # Optimization version
    print('Optimization version:')
    d: dict[tuple[int, int], int] = {}
    for (u2, v2) in g.E:
        d[u2, v2] = abs(u2 - v2)
    wf2 = WeightingFunction((e for e in d.items()), symmetrical=True)
    sols_opt = list(hamiltoniancycle_opt_solve(g, wf2))
    if len(sols_opt) > 0:
        print(f'\tBest solution: {sols_opt[-1]}')
    else:
        print('\tThere are no solutions')
