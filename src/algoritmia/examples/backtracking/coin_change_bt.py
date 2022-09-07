from dataclasses import dataclass
from typing import *

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve, bt_vc_solve
from algoritmia.schemes.bt_scheme import ScoredDecisionSequence, bt_min_solve

Decision = int
Solution = tuple[Decision, ...]
State = tuple[int, int]


def coin_change_solve_naif(v: tuple[int, ...], Q: int) -> Iterable[Solution]:
    def calc(ds: tuple[int, ...]) -> int:
        return sum(ds[i] * v[i] for i in range(len(ds)))

    class CoinChangeDS(DecisionSequence):
        def is_solution(self) -> bool:
            q = calc(self.decisions())
            return len(self) == len(v) and q == Q

        def successors(self) -> Iterable["CoinChangeDS"]:
            n = len(self)
            if n < len(v):
                q = calc(self.decisions())
                pending = Q - q
                for num_coins in range(pending // v[n] + 1):
                    yield self.add_decision(num_coins)

    initial_ds = CoinChangeDS()
    return bt_solve(initial_ds)


def coin_change_solve(v: tuple[int, ...], Q: int) -> Iterable[Solution]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterable["CoinChangeDS"]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    pending2 = self.extra.pending - num_coins * v[n]
                    yield self.add_decision(num_coins, Extra(pending2))

    initial_ds = CoinChangeDS(Extra(Q))
    return bt_solve(initial_ds)


def coin_change_vc_solve(v: tuple[int, ...], Q: int) -> Iterable[Solution]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterable["CoinChangeDS"]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    pending2 = self.extra.pending - num_coins * v[n]
                    yield self.add_decision(num_coins, Extra(pending2))

        def state(self):
            return len(self), self.extra.pending

    initial_ds = CoinChangeDS(Extra(Q))
    return bt_vc_solve(initial_ds)


def coin_change_opt_solve(v: tuple[int, ...], Q: int) -> Iterable[Solution]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(ScoredDecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterable["CoinChangeDS"]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    pending2 = self.extra.pending - num_coins * v[n]
                    yield self.add_decision(num_coins, Extra(pending2))

        def state(self):
            return len(self), self.extra.pending

        def score(self):
            return sum(self.decisions())

    initial_ds = CoinChangeDS(Extra(Q))
    return bt_min_solve(initial_ds)


# Programa principal ---------------------------------
if __name__ == "__main__":
    coins, quantity = (1, 2, 5), 7
    for solve in [coin_change_solve, coin_change_vc_solve, coin_change_opt_solve]:
        print(solve.__name__)
        for sol in solve(coins, quantity):
            print(sol)
        print()
