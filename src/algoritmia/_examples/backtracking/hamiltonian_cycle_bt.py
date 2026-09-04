from collections.abc import Iterator
from typing import Self

from algoritmia.datastructures.graphs import UndirectedGraph, WeightingFunction, IGraph, Edge, Weight
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, min_solution

# Tipos  --------------------------------------------------------------------------

# En este problema, una decisión es un vértice, por lo tanto, su tipo es TVertex (el genérico del grafo)
# TDecision = TVertex

# Una solución es una secuencia de decisiones (vértices) en forma de tupla:
type Solution[TDecision] = tuple[TDecision, ...]

# --------------------------------------------------------------------------------


def hamiltoniancycle_solutions[TVertex](g: IGraph[TVertex]) -> Iterator[Solution[TVertex]]:
    class HamiltonianCycleDS(DecisionSequence[TVertex, None]):  # Como no hay Extra -> ponemos None
        def is_solution(self) -> bool:
            return len(self) == len(g.V) and v_initial in g.succs(self.last_decision())

        def successors(self) -> Iterator[Self]:
            if len(self) == 0:                # Por eficiencia, fijamos el primer vértice
                yield self.add_decision(v_initial)
            elif len(self) < len(g.V):
                ds_set = set(self.decisions())  # O(|V|)
                for v in g.succs(self.last_decision()):
                    if v not in ds_set:  # O(1), |V| veces
                        yield self.add_decision(v)

    initial_ds = HamiltonianCycleDS()
    v_initial = next(iter(g.V))   # Cogemos uno cualquiera del set como vértice inicial
    for solution_ds in bt_solutions(initial_ds):
        yield solution_ds.decisions()


type Score = int | float    # La longitud (suma de pesos) del ciclo
type Result[TDecision] = tuple[Score, Solution[TDecision]] | None   # None si no hay solución


def hamiltoniancycle_best_solution[TVertex](g: IGraph[TVertex],
                                            wf: WeightingFunction[TVertex]) -> Result[TVertex]:
    def f(sol: Solution[TVertex]) -> Score:
        return sum(wf(sol[i - 1], sol[i]) for i in range(len(sol)))

    return min_solution(hamiltoniancycle_solutions(g), f)


# Programa principal --------------------------------------------------------------------------------

if __name__ == "__main__":
    edges = [(0, 2), (0, 3), (0, 9), (1, 3), (1, 4), (1, 8), (2, 3), (2, 5), (3, 4),
             (3, 6), (4, 7), (5, 6), (5, 8), (6, 7), (6, 8), (6, 9)]
    g0 = UndirectedGraph[int](E=edges)
    d0: dict[Edge[int], Weight] = dict(((u2, v2), abs(u2 - v2)) for (u2, v2) in g0.E)
    wf0 = WeightingFunction[int](d0, symmetrical=True)

    print('Basic versión (all solutions):')
    has_solutions = False
    for sol0 in hamiltoniancycle_solutions(g0):
        has_solutions = True
        print(f'\tSolution: {sol0}')
    if not has_solutions:
        print('\tThere are no solutions')

    print('Basic versión (best solution from all solutions):')
    print(f'\tBest solution: {hamiltoniancycle_best_solution(g0, wf0)}')
