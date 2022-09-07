from dataclasses import dataclass
from random import random, seed
from typing import *

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve, bt_vc_solve
from algoritmia.schemes.bt_scheme import ScoredDecisionSequence, bt_min_solve

Decision = int
Solution = tuple[int, tuple[Decision]]
State = tuple[int, int]


def sumset_solve(e: tuple[int, ...], S: int) -> Iterable[Solution]:
    @dataclass
    class Extra:
        acc_sum: int  # acumulated sum

    class SumSetDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == S

        def successors(self) -> Iterable["SumSetDS"]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= S:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))

    initial_ds = SumSetDS(Extra(0))
    return bt_solve(initial_ds)


def sumset_vc_solve(e: tuple[int, ...], S: int) -> Iterable[Solution]:
    @dataclass
    class Extra:
        acc_sum: int  # accumulated sum

    class SumSetDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == S

        def successors(self) -> Iterable["SumSetDS"]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= S:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))

        def state(self) -> State:
            return len(self), self.extra.acc_sum

    initial_ds = SumSetDS(Extra(0))
    return bt_vc_solve(initial_ds)


def sumset_opt_solve(e: tuple[int, ...], S: int) -> Iterable[Solution]:
    @dataclass
    class Extra:
        acc_sum: int = 0  # acumulated sum

    class SumSetDS(ScoredDecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == S

        def successors(self) -> Iterable["SumSetDS"]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= S:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    yield self.add_decision(1, Extra(acc_sum2))

        def state(self) -> State:
            return len(self), self.extra.acc_sum

        def score(self) -> int:
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

    # Visited control version
    try:
        first_sol = next(iter(sumset_vc_solve(elements, target_sum)))
        print(f'Visited control version - First solution: {first_sol}')
    except StopIteration:
        print(f'Visited control version - There is no solution.')

    # Optimization version
    sols_opt = list(sumset_opt_solve(elements, target_sum))
    if len(sols_opt) > 0:
        print(f'Optimization version    - Best solution:  {sols_opt[-1]}')
    else:
        print("Optimization version     - There is no solution.")
