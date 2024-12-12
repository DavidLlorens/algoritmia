from collections.abc import Iterator
from dataclasses import dataclass
from random import random, seed
from typing import Self

from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_min_solve
from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

Decision = int
Solution = tuple[Decision, ...]

# 'bab_min_solve' devuelve Optional[ScoredSolution]
Score = int
ScoredSolution = tuple[Score, Solution]


# --------------------------------------------------------------------------------

def sumset_bab_solve(e: tuple[int, ...], s: int) -> ScoredSolution | None:
    @dataclass
    class Extra:
        acc_sum: int = 0  # accumulated sum
        used_nums: int = 0

    class SumSetDS(BabDecisionSequence[Decision, Extra, Score]):
        def calculate_opt_bound(self) -> Score:
            if self.extra.acc_sum == s:
                return self.extra.used_nums
            return self.extra.used_nums + 1  # Mejorable

        def calculate_pes_bound(self) -> Score:
            if self.extra.acc_sum == s:
                return self.extra.used_nums
            return infinity  # Mejorable

        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == s

        def successors(self) -> Iterator[Self]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                new_acc = self.extra.acc_sum + e[len(self)]
                if new_acc <= s:
                    new_used_nums = self.extra.used_nums + 1
                    yield self.add_decision(1, Extra(new_acc, new_used_nums))

        # Sobreescribimos 'state()'
        def state(self) -> tuple[int, int]:
            return len(self), self.extra.acc_sum

    initial_ds = SumSetDS(Extra())
    result = bab_min_solve(initial_ds)
    if result is None: return None
    score, solution_ds = result
    return score, solution_ds.decisions()


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

    sol0 = sumset_bab_solve(elements0, target0)
    if sol0 is not None:
        print(f"Best coin change solution: {sol0}")
    else:
        print("There are no solutions")
