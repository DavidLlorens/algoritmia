from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from random import random, seed
from typing import Optional

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, bt_vc_solutions, min_solution

# Tipos  --------------------------------------------------------------------------

Decision = int
Score = int
Solution = tuple[Decision, ...]


# --------------------------------------------------------------------------------

def subsetsum_solutions(e: tuple[int, ...], s: int) -> Iterator[Solution]:
    @dataclass
    class Extra:
        acc_sum: int  # acumulated sum

    class SumSetDS(DecisionSequence[Decision, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == s

        def successors(self) -> Iterator[SumSetDS]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= s:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))

    initial_ds = SumSetDS(Extra(0))
    return bt_solutions(initial_ds)


ScoredSolution = tuple[int, Solution]


def subsetsum_best_solution(e: tuple[int, ...], s: int) -> Optional[ScoredSolution]:
    def f(solution: Solution) -> int:
        return sum(solution)

    return min_solution(subsetsum_solutions(e, s), f)


# --------------------------------------------------------------------------------

def subsetsum_vc_solutions(e: tuple[int, ...], s: int) -> Iterator[Solution]:
    @dataclass
    class Extra:
        acc_sum: int  # accumulated sum

    class SumSetDS(DecisionSequence[Decision, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == s

        def successors(self) -> Iterator[SumSetDS]:
            if len(self) < len(e):
                if self.extra.acc_sum + e[len(self)] <= s:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))
                yield self.add_decision(0, self.extra)

        # Sobreescribimos 'state()'
        def state(self) -> tuple[int, int]:
            return len(self), self.extra.acc_sum

    initial_ds = SumSetDS(Extra(0))
    return bt_vc_solutions(initial_ds)


# --------------------------------------------------------------------------------

def subsetsum_problem(num_elem):
    seed(42)
    elems = tuple(int(random() * 1000) + 1 for _ in range(num_elem))
    return elems, sum(elems) // 4  # sorted(elems, key=lambda x: -x), sum(elems) // 4


# --------------------------------------------------------------------------------

if __name__ == "__main__":
    # Instance
    elements0, target0 = (640, 777, 276, 224, 677, 893, 87, 422, 30, 306), 393
    print(f"Elements: {elements0}")
    print(f"Target: {target0}\n")

    # Basic version
    print("Basic versión (all solutions):")
    sol0 = None
    for sol0 in subsetsum_solutions(elements0, target0):
        print(f"\tSolution: {sol0}")
    if sol0 is None:
        print("\tThere are no solutions")

    print('Basic versión (best solution from all solutions):')
    print(f"\tBest solution: {subsetsum_best_solution(elements0, target0)}")

    # Visited control version
    print('Visited control version:')
    sol0 = None
    for sol0 in subsetsum_vc_solutions(elements0, target0):
        print(f"\tSolution: {sol0}")
    if sol0 is None:
        print("\tThere are no solutions")
