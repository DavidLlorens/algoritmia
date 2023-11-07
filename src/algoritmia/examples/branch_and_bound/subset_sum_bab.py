from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from random import random, seed
from typing import Optional

from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_min_solve
from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

Decision = int
Score = int
ScoredSolution = tuple[Score, tuple[Decision, ...]]

# --------------------------------------------------------------------------------

def sumset_bab_solve(e: tuple[int, ...], s: int) -> Optional[ScoredSolution]:
    @dataclass
    class Extra:
        acc_sum: int = 0  # accumulated sum
        used_nums: int = 0

    class SumSetDS(BabDecisionSequence[Decision, Extra]):
        def f(self) -> Score:
            return self.extra.used_nums

        def calculate_opt_bound(self) -> Score:
            return self.f() + 0 if self.extra.acc_sum == s else 1

        def calculate_pes_bound(self) -> Score:
            if self.extra.acc_sum == s:
                return self.f()
            return infinity  # Mejorable

        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.acc_sum == s

        def successors(self) -> Iterator[SumSetDS]:
            if len(self) < len(e):
                yield self.add_decision(0, self.extra)
                if self.extra.acc_sum + e[len(self)] <= s:
                    acc_sum2 = self.extra.acc_sum + e[len(self)]
                    used_nums2 = self.extra.used_nums + 1
                    yield self.add_decision(1, Extra(acc_sum2, used_nums2))

        # Sobreescribimos 'state()'
        def state(self) -> tuple[int, int]:
            return len(self), self.extra.acc_sum

    initial_ds = SumSetDS(Extra())
    return bab_min_solve(initial_ds)


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
