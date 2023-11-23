from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from math import ceil
from typing import Optional

from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_min_solve
from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

Decision = int  # Número de monedas del tipo actual
Solution = tuple[Decision, ...]

# 'bab_min_solve' devuelve Optional[ScoredSolution]
Score = int  # Total de monedas utilizado
ScoredSolution = tuple[Score, Solution]


# --------------------------------------------------------------------------------

def coin_change_bab_solve(v: tuple[int, ...], Q: int) -> Optional[ScoredSolution]:
    @dataclass
    class Extra:
        pending: int
        used_coins: int

    class CoinChangeDS(BabDecisionSequence[Decision, Extra]):
        def calculate_opt_bound(self) -> Score:
            s = self.extra.used_coins
            if self.extra.pending > 0:
                if len(self) == len(v):
                    return infinity
                s += ceil(self.extra.pending / max(v[len(self):]))
            return s

        def calculate_pes_bound(self) -> Score:
            if self.is_solution():
                return self.extra.used_coins
            return infinity  # Mejorable

        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterator[CoinChangeDS]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    new_pending = self.extra.pending - num_coins * v[n]
                    new_used_coins = self.extra.used_coins + num_coins
                    yield self.add_decision(num_coins, Extra(new_pending, new_used_coins))

        def state(self) -> tuple[int, int]:
            return len(self), self.extra.pending

    initial_ds = CoinChangeDS(Extra(Q, 0))
    return bab_min_solve(initial_ds)


# Programa principal --------------------------------------------------------------------------------

if __name__ == "__main__":
    v0, Q0 = (1, 2, 5), 7
    print(f"Coins: {v0}")
    print(f"Quantity: {Q0}\n")

    sol0 = coin_change_bab_solve(v0, Q0)
    if sol0 is not None:
        print(f"Best coin change solution: {sol0}")
    else:
        print("There are no solutions")
