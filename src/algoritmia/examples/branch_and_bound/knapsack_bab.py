from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from random import seed, randint
from typing import Optional

from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_max_solve
from algoritmia.schemes.bt_scheme import State

# Tipos  --------------------------------------------------------------------------

Decision = int  # 0 o 1 (coger o no un objeto)
Score = int  # Valor de la mochila (suma del valor de los objetos que contiene)

# 'bab_max_solve' devuelve un Iterator del tipo devuelto por el método 'solution' de
# la clase 'BoundedDecisionSequence', cuya implementación por defecto devuelve una tupla de dos elementos:
# el Score (el valor del contenido de la mochila) y una tupla con las decisones:
Solution = tuple[Score, tuple[Decision, ...]]


# Podriamos sobreescribir  el método 'solution()' en KnapsackBabDS para que devolviera también el peso.
# En ese caso el tipo de 'Solution' sería:
# Solution = tuple[Score, int, tuple[Decision, ...]]  # (value, weight, decisions)

# Versión naif (cotas poco informadas) --------------------------------------------------------------------------

def knapsack_bab_solve_naif(weights: list[int],
                            values: list[int],
                            capacity: int) -> Optional[Solution]:
    @dataclass
    class Extra:
        weight: int = 0
        value: int = 0

    class KnapsackBabDS(BabDecisionSequence):
        def f(self) -> int:
            return self.extra.value

        # OPTIMISTA: Coge TODOS los objetos pendientes
        def calculate_opt_bound(self) -> Score:
            return self.f() + sum(values[len(self):])

        # PESIMISTA: No coge NINGUNO de los objetos pendientes
        def calculate_pes_bound(self) -> Score:
            return self.f() + 0

        def is_solution(self) -> bool:
            return len(self) == len(values)

        def successors(self) -> Iterator[KnapsackBabDS]:
            n = len(self)
            if n < len(values):
                if weights[n] + self.extra.weight <= capacity:
                    new_weight = self.extra.weight + weights[n]
                    new_value = self.extra.value + values[n]
                    yield self.add_decision(1, Extra(new_weight, new_value))
                yield self.add_decision(0, self.extra)

        def state(self) -> State:
            return len(self), self.extra.weight

        # Podríamos sobreescribir 'solution()' para devolver también el peso:
        # def solution(self) -> Solution:
        #    return self.extra.value, self.extra.weight, self.decisions()

    initial_ds = KnapsackBabDS(Extra())
    return bab_max_solve(initial_ds)


# Versión con cotas informadas --------------------------------------------------------------------------
c = 0
def knapsack_bab_solve(weights: list[int],
                       values: list[int],
                       capacity: int) -> Optional[Solution]:
    @dataclass
    class Extra:
        weight: int = 0
        value: int = 0

    class KnapsackBabDS(BabDecisionSequence):
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

        # PESISMISTA: modificación del optimista para que no fraccione
        def calculate_pes_bound(self) -> int:
            value = self.extra.value
            weight = self.extra.weight
            for i in range(len(self), len(weights)):
                if weight + weights[i] <= capacity:
                    weight += weights[i]
                    value += values[i]
            return value

        def f(self) -> int:
            return self.extra.value

        def is_solution(self) -> bool:
            return len(self) == len(values)

        def successors(self) -> Iterator[KnapsackBabDS]:
            n = len(self)
            if n < len(values):
                if weights[n] + self.extra.weight <= capacity:
                    new_weight = self.extra.weight + weights[n]
                    new_value = self.extra.value + values[n]
                    yield self.add_decision(1, Extra(new_weight, new_value))
                yield self.add_decision(0, self.extra)

        def state(self) -> State:
            return len(self), self.extra.weight

        # Podríamos sobreescribir 'solution()' para devolver también el peso:
        # def solution(self) -> Solution:
        #    return self.extra.value, self.extra.weight, self.decisions()

    initial_ps = KnapsackBabDS(Extra())
    return bab_max_solve(initial_ps)


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
        print("-"*80)
        print(f"Instancia:\n  Pesos = {W}\n  Valores = {V}\n  Capacidad = {C}\n")
        print(f"knapsack_bab_solve:\n  {knapsack_bab_solve(W, V, C)}")
    print("-"*80)