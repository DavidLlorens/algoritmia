from collections.abc import Iterator
from dataclasses import dataclass
from random import seed, randint
from typing import Self

from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_max_solve
from algoritmia.schemes.bt_scheme import State

# Tipos  --------------------------------------------------------------------------

Decision = int  # 0 o 1 (coger o no un objeto)
Solution = tuple[Decision, ...]
# Podriamos sobrescribir el método 'solution()' en KnapsackBabDS para que devolviera también el peso.
# En ese caso el tipo de 'Solution' sería:
# Solution = tuple[int, tuple[Decision, ...]]  # (weight, decisions)

# 'bab_max_solve' devuelve Optional[ScoredSolution]
Score = int  # Valor de la mochila (suma del valor de los objetos que contiene)
ScoredSolution = tuple[Score, Solution]


# Versión naif (cotas poco informadas) --------------------------------------------------------------------------

def knapsack_bab_solve_naif(weights: list[int],
                            values: list[int],
                            capacity: int) -> ScoredSolution:
    @dataclass
    class Extra:
        weight: int = 0
        value: int = 0

    class KnapsackBabDS(BabDecisionSequence[Decision, Extra, Score]):
        # OPTIMISTA: Coge TODOS los objetos pendientes (cota poco informada)
        def calculate_opt_bound(self) -> Score:
            return self.extra.value + sum(values[len(self):])

        # PESIMISTA: No coge NINGUNO de los objetos pendientes (cota poco informada)
        def calculate_pes_bound(self) -> Score:
            return self.extra.value + 0

        def is_solution(self) -> bool:
            return len(self) == len(values)

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(values):
                new_weight = self.extra.weight + weights[n]
                if new_weight <= capacity:
                    new_value = self.extra.value + values[n]
                    yield self.add_decision(1, Extra(new_weight, new_value))
                yield self.add_decision(0, self.extra)

        def state(self) -> State:
            return len(self), self.extra.weight

    initial_ds = KnapsackBabDS(Extra())
    score, solution_ds = bab_max_solve(initial_ds)
    return score, solution_ds.decisions()


# Versión con cotas informadas --------------------------------------------------------------------------
c = 0


def knapsack_bab_solve(weights: list[int],
                       values: list[int],
                       capacity: int) -> ScoredSolution:
    @dataclass
    class Extra:
        weight: int = 0
        value: int = 0

    class KnapsackBabDS(BabDecisionSequence[Decision, Extra, Score]):
        # OPTIMISTA: resolver mochila fraccionaria para los objetos que quedan (tema Voraces)
        def calculate_opt_bound(self) -> int:
            value = self.extra.value
            weight = self.extra.weight
            for i in range(len(self), len(weights)):
                f = min(1.0, (capacity - weight) / weights[i])
                weight += f * weights[i]
                value += f * values[i]
                if f < 1:
                    break
            return value

        # PESIMISTA: modificación del optimista para que no fraccione
        def calculate_pes_bound(self) -> int:
            value = self.extra.value
            weight = self.extra.weight
            for i in range(len(self), len(weights)):
                if weight + weights[i] <= capacity:
                    weight += weights[i]
                    value += values[i]
            return value

        def is_solution(self) -> bool:
            return len(self) == len(values)

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(values):
                new_weight = self.extra.weight + weights[n]
                if new_weight <= capacity:
                    new_value = self.extra.value + values[n]
                    yield self.add_decision(1, Extra(new_weight, new_value))
                yield self.add_decision(0, self.extra)

        def state(self) -> State:
            return len(self), self.extra.weight

    initial_ds = KnapsackBabDS(Extra())
    score, solution_ds = bab_max_solve(initial_ds)
    return score, solution_ds.decisions()


# Funciones auxiliares para crear instancias  ----------------------------------------------

def sorted_by_dec_ratio(weights: list[int], values: list[int]) -> tuple[list[int], list[int]]:
    idxs: list[int] = sorted(range(len(weights)), key=lambda i: -values[i] / weights[i])
    w_new = [weights[i] for i in idxs]
    v_new = [values[i] for i in idxs]
    return w_new, v_new


# Crea los problemas con los objetos ordenados de mayor a menor beneficio por kilo
def create_knapsack_problem(num_objects: int) -> tuple[list[int], list[int], int]:
    seed(5)
    w_new = [randint(10, 100) for _ in range(num_objects)]
    v_new = [w_new[i] * randint(1, 4) for i in range(num_objects)]
    capacity = int(sum(w_new) * 0.3)
    weights, values = sorted_by_dec_ratio(w_new, v_new)
    return weights, values, capacity


# Programa principal -------------------------------------------------------------------------


if __name__ == "__main__":
    # Cada instancia es una tupla (pesos, valores, capacidad):

    # Solution: value = 354, decisions = (1, 0, 1, 0, 0, 0))
    i1 = create_knapsack_problem(6)

    # Solution: value = 1118, decisions = (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
    i2 = create_knapsack_problem(20)

    # Solution: value = 1830, decisions = (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0...0)
    i3 = create_knapsack_problem(35)

    for W, V, C in [i1, i2, i3]:
        print("-" * 80)
        print(f"Instancia:\n  Pesos = {W}\n  Valores = {V}\n  Capacidad = {C}\n")
        print(f"knapsack_bab_solve:\n  {knapsack_bab_solve(W, V, C)}")
    print("-" * 80)
