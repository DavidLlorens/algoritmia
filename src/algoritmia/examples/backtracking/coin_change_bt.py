from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional, Self

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, bt_vc_solutions, min_solution

# Tipos  --------------------------------------------------------------------------

type Decision = int  # Número de monedas del tipo actual
type Score = int  # Total de monedas utilizado

# 'bt_solutions' y 'bt_vc_solutions' devuelven un Iterator del tipo devuelto por el método 'solution' de
# la clase 'DecisionSequence', cuya implementación por defecto devuelve una tupla con las decisiones:
type Solution = tuple[Decision, ...]


# --------------------------------------------------------------------------------

def coin_change_solutions_naif(v: tuple[int, ...], Q: int) -> Iterator[Solution]:
    class CoinChangeDS(DecisionSequence[Decision, None]):
        def is_solution(self) -> bool:
            pending = calc_pending(self)  # O(n)
            return len(self) == len(v) and pending == 0

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(v):
                pending = calc_pending(self)  # O(n)
                for num_coins in range(pending // v[n] + 1):
                    yield self.add_decision(num_coins)

    def calc_pending(ds: CoinChangeDS) -> int:
        # Se calcula a partir del problema original y la secuencia de decisiones actual
        return Q - sum(d * v[i] for i, d in enumerate(ds.decisions()))

    initial_ds = CoinChangeDS()
    return bt_solutions(initial_ds)


# --------------------------------------------------------------------------------

def coin_change_solutions(v: tuple[int, ...], Q: int) -> Iterator[Solution]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(DecisionSequence[Decision, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    pending2 = self.extra.pending - num_coins * v[n]
                    yield self.add_decision(num_coins, Extra(pending2))

    initial_ds = CoinChangeDS(Extra(Q))
    return bt_solutions(initial_ds)


ScoredSolution = tuple[int, Solution]


def coin_change_best_solution(v: tuple[int, ...], Q: int) -> Optional[ScoredSolution]:
    def f(solution: Solution) -> int:
        return sum(solution)

    return min_solution(coin_change_solutions(v, Q), f)


# --------------------------------------------------------------------------------


def coin_change_vc_solutions(v: tuple[int, ...], Q: int) -> Iterator[Solution]:
    @dataclass
    class Extra:
        pending: int

    class CoinChangeDS(DecisionSequence[Decision, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(v) and self.extra.pending == 0

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(v):
                for num_coins in range(self.extra.pending // v[n] + 1):
                    pending2 = self.extra.pending - num_coins * v[n]
                    yield self.add_decision(num_coins, Extra(pending2))

        def state(self) -> tuple[int, int]:
            return len(self), self.extra.pending

    initial_ds = CoinChangeDS(Extra(Q))
    return bt_vc_solutions(initial_ds)


# Programa principal --------------------------------------------------------------------------------


if __name__ == "__main__":
    v0, Q0 = (1, 2, 5, 10), 11
    print(f"Coins: {v0}")
    print(f"Quantity: {Q0}\n")

    # Naif version
    print("Basic versión (all solutions):")
    sol0 = None
    for sol0 in coin_change_solutions_naif(v0, Q0):
        print(f"\tSolution: {sol0}")
    if sol0 is None:
        print("\tThere are no solutions")

    # Basic version
    print("Basic versión (all solutions):")
    sol0 = None
    for sol0 in coin_change_solutions(v0, Q0):
        print(f"\tSolution: {sol0}")
    if sol0 is None:
        print("\tThere are no solutions")

    print('Basic versión (best solution from all solutions):')
    print(f"\tBest solution: {coin_change_best_solution(v0, Q0)}")

    # Visited control version
    print("Visited control version:")
    sol0 = None
    for sol0 in coin_change_vc_solutions(v0, Q0):
        print(f"\tSolution: {sol0}")
    if sol0 is None:
        print("\tThere are no solutions")

