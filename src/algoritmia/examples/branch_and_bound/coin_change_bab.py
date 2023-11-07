from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from math import ceil
from typing import Optional

from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_min_solve
from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

Decision = int  # Número de monedas del tipo actual
Score = int  # Total de monedas utilizado

# 'bt_solutions' y 'bt_vc_solutions' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'DecisionSequence', cuya implementación por defecto devuelve una tupla con las decisiones:
ScoredSolution = tuple[Score, tuple[Decision, ...]]


# --------------------------------------------------------------------------------

def coin_change_bab_solve(v: tuple[int, ...], Q: int) -> Optional[ScoredSolution]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(BabDecisionSequence[Decision, Extra]):
        def f(self) -> int:
            return sum(self.decisions())

        def calculate_opt_bound(self) -> Score:
            if len(self) == len(v):
                return self.f()
            return self.f() + ceil(self.extra.pending / max(v[len(self):]))

        def calculate_pes_bound(self) -> Score:
            return infinity  # Mejorable

        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterator[CoinChangeDS]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    pending2 = self.extra.pending - num_coins * v[n]
                    yield self.add_decision(num_coins, Extra(pending2))

        def state(self) -> tuple[int, int]:
            return len(self), self.extra.pending

    initial_ds = CoinChangeDS(Extra(Q))
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
