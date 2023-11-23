from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional

from algoritmia.datastructures.graphs import UndirectedGraph, TVertex, WeightingFunction
from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_min_solve
from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

Decision = TVertex
Score = float

# 'bt_solutions' y 'bt_vc_solutions' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'DecisionSequence', cuya implementación por defecto devuelve una tupla con las decisiones:
Solution = tuple[Decision, ...]

# 'bt_min_solve' y 'bt_max_solve' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'ScoredDecisionSequence', cuya implementación por defecto devuelve una tupla de dos elementos:
# el Score y una tupla con las decisones:
ScoredSolution = tuple[Score, tuple[Decision, ...]]


# --------------------------------------------------------------------------------

def hamiltoniancycle_bab_solve(g: UndirectedGraph[TVertex],
                               wf: WeightingFunction[TVertex]) -> Optional[ScoredSolution]:
    @dataclass
    class Extra:
        weight: int = 0

    class HamiltonianCycleDS(BabDecisionSequence[TVertex, Extra]):
        def f(self) -> float:
            if len(self) < len(g.V): return self.extra.weight
            if v_initial in g.succs(self.decision):
                return self.extra.weight + wf(self.decision, v_initial)
            return infinity

        def calculate_opt_bound(self) -> Score:
            return self.f() + 0  # Mejorable (arista de menor peso de cada vértice pendiente)

        def calculate_pes_bound(self) -> Score:
            if self.is_solution():
                return self.f()
            return infinity  # Mejorable

        def is_solution(self) -> bool:
            return len(self) == len(g.V) and v_initial in g.succs(self.decision)

        def successors(self) -> Iterator[HamiltonianCycleDS]:
            if len(self) < len(g.V):
                ds_set = set(self.decisions())  # O(|V|)
                for v in g.succs(self.decision):
                    if v not in ds_set:  # O(1), |V| veces
                        new_weight = self.extra.weight + wf(self.decision, v)
                        yield self.add_decision(v, Extra(new_weight))

        # Sobreescribimos 'state()'
        def state(self) -> tuple[TVertex, tuple[Vertex, ...]]:
            return self.decision, tuple(sorted(self.decisions()))  # O(|V|)

    initial_ds = HamiltonianCycleDS(Extra(0))
    v_initial = next(iter(g0.V))  # Elegimos un vértice cualquiera como inicial
    initial_ds2 = initial_ds.add_decision(v_initial, Extra(0))  # Forzamos la primera decisión
    return bab_min_solve(initial_ds2)


# Programa principal ---------------------------
if __name__ == "__main__":
    Vertex = int
    Edge = tuple[Vertex, Vertex]
    edges: list[Edge] = [(0, 2), (0, 3), (0, 9), (1, 3), (1, 4), (1, 8), (2, 3), (2, 5), (3, 4),
                         (3, 6), (4, 7), (5, 6), (5, 8), (6, 7), (6, 8), (6, 9)]
    g0 = UndirectedGraph(E=edges)
    d0 = dict(((u2, v2), abs(u2 - v2)) for (u2, v2) in g0.E)
    wf0 = WeightingFunction(d0, symmetrical=True)

    sol0 = hamiltoniancycle_bab_solve(g0, wf0)
    if sol0 is not None:
        print(f'Best hamiltonian cycle solution: {sol0}')
    else:
        print('There are no solutions')
