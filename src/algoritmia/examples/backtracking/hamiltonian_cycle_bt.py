from dataclasses import dataclass
from typing import *

from algoritmia.datastructures.graphs import UndirectedGraph, WeightingFunction
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve
from algoritmia.schemes.bt_scheme import ScoredDecisionSequence, bt_min_solve

Decision = TypeVar('Decision')
Solution = tuple[Decision, ...]


def hamiltoniancycle_solve(graph: UndirectedGraph) -> Iterable[Solution]:
    class HamiltonianCycleDS(DecisionSequence):
        def is_solution(self):
            ds = self.decisions()
            return len(ds) == len(graph.V) and ds[0] in graph.succs(ds[-1])

        def successors(self) -> Iterable['HamiltonianCycleDS']:
            ds = self.decisions()
            if len(ds) < len(graph.V):
                for v in graph.succs(ds[-1]):
                    if v not in ds:
                        yield self.add_decision(v)

    v_initial = next(iter(graph.V))  # Para coger un elemento de un conjunto sin sacarlo
    initial_ds = HamiltonianCycleDS().add_decision(v_initial)
    return bt_solve(initial_ds)


Solution = tuple[float, tuple[Decision, ...]]
State = tuple[int, tuple[int, ...]]
Score = float


def hamiltoniancycle_opt_solve(graph: UndirectedGraph, wf: WeightingFunction):
    @dataclass
    class Extra:
        ls: int = 0

    class HamiltonianCycleDS(ScoredDecisionSequence):
        def is_solution(self):
            ds = self.decisions()
            return len(ds) == len(graph.V) and (ds[-1], ds[0]) in graph.E

        def solution(self) -> Solution:
            return self.score(), self.decisions()

        def successors(self) -> Iterable['HamiltonianCycleDS']:
            ds = self.decisions()
            if len(ds) < len(graph.V):
                for v in graph.succs(ds[-1]):
                    if v not in ds:
                        new_extra = Extra(self.extra.ls + wf(ds[-1], v))
                        yield self.add_decision(v, new_extra)

        def state(self) -> State:
            ds = list(self.decisions())
            return ds[-1], tuple(sorted(ds))

        def score(self) -> Score:
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
    G = UndirectedGraph(E=[(0, 2), (0, 3), (0, 9), (1, 3), (1, 4), (1, 8), (2, 3), (2, 5), (3, 4),
                           (3, 6), (4, 7), (5, 6), (5, 8), (6, 7), (6, 8), (6, 9)])
    d: dict[tuple[int, int], int] = {}
    for (u, v) in G.E:
        d[u, v] = abs(u - v)
    wf = WeightingFunction((e for e in d.items()), symmetrical=True)

    print("hamiltoniancycle_solve:")
    for solution in hamiltoniancycle_solve(G):
        print(solution)
    print()
    print("hamiltoniancycle_opt_solve:")
    for solution in hamiltoniancycle_opt_solve(G, wf):
        print(solution)
