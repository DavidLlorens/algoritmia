from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

from algoritmia.datastructures.graphs import UndirectedGraph, WeightingFunction
from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_min_solve
from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

# En este problema, una decisión es un vértice, por lo tanto, su tipo es T (el genérico del grafo)
# Decision = T
type Solution[T] = tuple[T, ...]

# 'bab_min_solve' devuelve Optional[ScoredSolution]
type Score = float
type ScoredSolution[T] = tuple[Score, Solution[T]]


# --------------------------------------------------------------------------------

def hamiltoniancycle_bab_solve[T](g: UndirectedGraph[T],
                                  wf: WeightingFunction[T]) -> ScoredSolution[T] | None:
    @dataclass
    class Extra:
        weight: int = 0

    class HamiltonianCycleDS(BabDecisionSequence[T, Extra, Score]):
        def calculate_opt_bound(self) -> Score:
            if self.is_solution():
                return self.extra.weight + wf(self.last_decision(), v_initial)
            if len(self) < len(g.V):
                return self.extra.weight + 0  # Mejorable (arista de menor peso de cada vértice pendiente)
            return infinity

        def calculate_pes_bound(self) -> Score:
            if self.is_solution():
                return self.extra.weight + wf(self.last_decision(), v_initial)
            return infinity  # Mejorable

        def is_solution(self) -> bool:
            return len(self) == len(g.V) and v_initial in g.succs(self.last_decision())

        def successors(self) -> Iterator[Self]:
            if len(self) < len(g.V):
                ds_set = set(self.decisions())  # O(|V|)
                for v in g.succs(self.last_decision()):
                    if v not in ds_set:  # O(1), |V| veces
                        new_weight = self.extra.weight + wf(self.last_decision(), v)
                        yield self.add_decision(v, Extra(new_weight))
                        aa = self.add_decision(v_initial, Extra(0))
                        yield aa

        # Sobreescribimos 'state()'
        def state(self) -> tuple[T, tuple[T, ...]]:
            return self.last_decision(), tuple(sorted(self.decisions()))  # O(|V|)

    initial_ds = HamiltonianCycleDS(Extra(0))
    v_initial = next(iter(g0.V))  # Elegimos un vértice cualquiera como inicial
    one_vertex_ds = initial_ds.add_decision(v_initial, Extra(0))  # Forzamos la primera decisión

    result = bab_min_solve(one_vertex_ds)
    if result is None: return None
    score, solution_ds = result
    return score, solution_ds.decisions()


# Programa principal ---------------------------
if __name__ == "__main__":
    # En este ejemplo, los vértices son de tipo int

    # Por lo tanto, las aristas son tuple[int, int]
    edges = [(0, 2), (0, 3), (0, 9), (1, 3), (1, 4), (1, 8), (2, 3), (2, 5),
             (3, 4), (3, 6), (4, 7), (5, 6), (5, 8), (6, 7), (6, 8), (6, 9)]

    # Y el grafo, g0, es de tipo UndirectedGraph[int]
    g0 = UndirectedGraph(E=edges)

    d0 = dict(((u2, v2), abs(u2 - v2)) for (u2, v2) in g0.E)
    wf0 = WeightingFunction(d0, symmetrical=True)

    sol0 = hamiltoniancycle_bab_solve(g0, wf0)
    if sol0 is not None:
        print(f'Best hamiltonian cycle solution: {sol0}')
    else:
        print('There are no solutions')
