from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

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


def coin_change_solve_naif(v: tuple[int, ...], Q: int) -> Iterator[SolutionDS]:
    def calc(ds: tuple[int, ...]) -> int:
        return sum(ds[i] * v[i] for i in range(len(ds)))

    class CoinChangeDS(DecisionSequence[Decision]):
        def is_solution(self) -> bool:
            q = calc(self.decisions())
            return len(self) == len(v) and q == Q

        def successors(self) -> Iterator[CoinChangeDS]:
            n = len(self)
            if n < len(v):
                q = calc(self.decisions())
                pending = Q - q
                for num_coins in range(pending // v[n] + 1):
                    yield self.add_decision(num_coins)

    initial_ds = CoinChangeDS()
    return bt_solve(initial_ds)


def coin_change_solve(v: tuple[int, ...], Q: int) -> Iterator[SolutionDS]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(DecisionSequence[Decision]):
        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterator[CoinChangeDS]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    pending2 = self.extra.pending - num_coins * v[n]
                    yield self.add_decision(num_coins, Extra(pending2))

    initial_ds = CoinChangeDS(Extra(Q))
    return bt_solve(initial_ds)


def coin_change_vc_solve(v: tuple[int, ...], Q: int) -> Iterator[SolutionDS]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(StateDecisionSequence[Decision]):
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
    return bt_vc_solve(initial_ds)


def coin_change_opt_solve(v: tuple[int, ...], Q: int) -> Iterator[SolutionSDS]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(ScoredDecisionSequence[Decision]):
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

        def score(self) -> int:
            return sum(self.decisions())

    initial_ds = CoinChangeDS(Extra(Q))
    return bt_min_solve(initial_ds)


# Programa principal ---------------------------------
if __name__ == "__main__":
    coins, quantity = (1, 2, 5), 7

    # Basic version
    print('Basic versión (all solutions):')
    has_solutions = False
    for i, sol in enumerate(coin_change_solve(coins, quantity)):
        has_solutions = True
        print(f'\tSolution {i+1}: {sol}')
    if not has_solutions:
        print('\tThere are no solutions')

    # Visited control version
    print('Visited control version:')
    try:
        first_sol = next(coin_change_vc_solve(coins, quantity))
        print(f'\tFirst solution: {first_sol}')
    except StopIteration:
        print('\tThere are no solutions')

    # Optimization version
    print('Optimization version:')
    sols_opt = list(coin_change_opt_solve(coins, quantity))
    if len(sols_opt) > 0:
        print(f'\tBest solution: {sols_opt[-1]}')
    else:
        print('\tThere are no solutions')
