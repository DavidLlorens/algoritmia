from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from random import random, seed

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve
from algoritmia.schemes.bt_scheme import ScoredDecisionSequence, bt_min_solve
from algoritmia.schemes.bt_scheme import StateDecisionSequence, bt_vc_solve

Decision = int
Score = int

# 'bt_solve' y 'bt_vc_solve' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'DecisionSequence', cuya implementación por defecto devuelve una tupla con las decisiones:
SolutionDS = tuple[Decision, ...]

# 'bt_min_solve' y 'bt_max_solve' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'ScoredDecisionSequence', cuya implementación por defecto devuelve una tupla de dos elementos:
# el Score y una tupla con las decisones:
SolutionSDS = tuple[Score, tuple[Decision, ...]]


def sumset_solve(e: tuple[int, ...], s: int) -> Iterator[SolutionDS]:
    @dataclass
    class Extra:
        acc_sum: int  # acumulated sum

    class SumSetDS(DecisionSequence[Decision]):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == s

        def successors(self) -> Iterator[SumSetDS]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= s:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))

    initial_ds = SumSetDS(Extra(0))
    return bt_solve(initial_ds)


def sumset_vc_solve(e: tuple[int, ...], s: int) -> Iterator[SolutionDS]:
    @dataclass
    class Extra:
        acc_sum: int  # accumulated sum

    class SumSetDS(StateDecisionSequence[Decision]):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == s

        def successors(self) -> Iterator[SumSetDS]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= s:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))

        # Sobreescribimos 'state()'
        def state(self) -> tuple[int, int]:
            return len(self), self.extra.acc_sum

    initial_ds = SumSetDS(Extra(0))
    return bt_vc_solve(initial_ds)


def sumset_opt_solve(e: tuple[int, ...], s: int) -> Iterator[SolutionSDS]:
    @dataclass
    class Extra:
        acc_sum: int = 0  # acumulated sum

    class SumSetDS(ScoredDecisionSequence[Decision]):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == s

        def successors(self) -> Iterator[SumSetDS]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= s:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))

        # Sobreescribimos 'state()'
        def state(self) -> tuple[int, int]:
            return len(self), self.extra.acc_sum

        def score(self) -> Score:
            return sum(self.decisions())

    initial_ds = SumSetDS(Extra())
    return bt_min_solve(initial_ds)


def subsetsum_problem(num_elem):
    seed(42)
    elems = tuple(int(random() * 1000) + 1 for _ in range(num_elem))
    return elems, sum(elems) // 4  # sorted(elems, key=lambda x: -x), sum(elems) // 4


# Programa principal ---------------------------------
if __name__ == "__main__":
    # Instance
    elements, target_sum = (640, 777, 276, 224, 737, 677, 893, 87, 422, 30), 1199

    # Basic version
    print('Basic versión (all solutions):')
    has_solutions = False
    for i, sol in enumerate(sumset_solve(elements, target_sum)):
        has_solutions = True
        print(f'\tSolution {i+1}: {sol}')
    if not has_solutions:
        print('\tThere are no solutions')

    # Visited control version
    print('Visited control version:')
    try:
        first_sol = next(sumset_vc_solve(elements, target_sum))
        print(f'\tFirst solution: {first_sol}')
    except StopIteration:
        print('\tThere are no solutions')

    # Optimization version
    print('Optimization version:')
    sols_opt = list(sumset_opt_solve(elements, target_sum))
    if len(sols_opt) > 0:
        print(f'\tBest solution: {sols_opt[-1]}')
    else:
        print('\tThere are no solutions')
