from dataclasses import dataclass
from random import seed, randint
from typing import *

from algoritmia.schemes.bab_scheme import BoundedDecisionSequence, bab_max_solve

Decision = int  # 0 o 1
Solution = tuple[int, int, tuple[Decision,...]]  # (value, weight, decisions)


def knapsack_bab_solve(weights: list[int], values: list[int], capacity: int) -> Solution:
    @dataclass
    class Extra:
        weight: int = 0
        value: int = 0

    class KnapsackBabDS(BoundedDecisionSequence):
        # Coge TODOS los objetos pendientes
        def calculate_opt_bound(self) -> int:
            return self.extra.value + sum(values[len(self):])

        # No coge NINGUNO de los objetos pendientes
        def calculate_pes_bound(self) -> int:
            return self.extra.value

        def is_solution(self) -> bool:
            return len(self) == len(values)

        def solution(self) -> Solution:
            return self.extra.value, self.extra.weight, self.decisions()

        def successors(self) -> Iterable["KnapsackBabDS"]:
            n = len(self)
            if n < len(values):
                if weights[n] <= capacity - self.extra.weight:
                    new_extra = Extra(self.extra.weight + weights[n], self.extra.value + values[n])
                    yield self.add_decision(1, new_extra)
                yield self.add_decision(0, self.extra)

    initial_ds = KnapsackBabDS(Extra())
    return bab_max_solve(initial_ds)


def knapsack_bab_solve2(weights: list[int], values: list[int], capacity: int):
    @dataclass
    class Extra:
        weight: int = 0
        value: int = 0

    class KnapsackBabDS(BoundedDecisionSequence):
        # IMPLEMENTAR: resolver mochila continua para los objetos que quedan (tema 3)
        def calculate_opt_bound(self) -> int:
            value = self.extra.value
            weight = self.extra.weight
            for i in range(len(self), len(weights)):
                f = min(1, (capacity - weight) / weights[i])
                weight += f * weights[i]
                value += f * values[i]
                if f < 1:
                    break
            return value

        # IMPLEMENTAR: modificación del optimista sin fraccionar
        def calculate_pes_bound(self) -> int:
            value = self.extra.value
            weight = self.extra.weight
            for i in range(len(self), len(weights)):
                if (capacity - weight) >= weights[i]:
                    weight += weights[i]
                    value += values[i]
            return value

        def is_solution(self) -> bool:
            return len(self) == len(values)

        def solution(self) -> Solution:
            return self.extra.value, self.extra.weight, self.decisions()

        def successors(self) -> Iterable["KnapsackBabDS"]:
            n = len(self)
            if n < len(values):
                if weights[n] <= capacity - self.extra.weight:
                    new_extra = Extra(self.extra.weight + weights[n], self.extra.value + values[n])
                    yield self.add_decision(1, new_extra)
                yield self.add_decision(0, self.extra)

    initial_ps = KnapsackBabDS(Extra())
    return bab_max_solve(initial_ps)


def sorted_by_dec_ratio(w_old, v_old):
    idxs = sorted(range(len(w_old)), key=lambda i: -v_old[i] / w_old[i])
    w_new = [w_old[i] for i in idxs]
    v_new = [v_old[i] for i in idxs]
    return w_new, v_new


def create_knapsack_problem(num_objects):
    seed(5)
    w_new = [randint(10, 100) for _ in range(num_objects)]
    v_new = [w_new[i] * randint(1, 4) for i in range(num_objects)]
    capacity = int(sum(w_new) * 0.3)
    weights, values = sorted_by_dec_ratio(w_new, v_new)
    return weights, values, capacity


# Main program -------------------------------------------------------
if __name__ == "__main__":
    # W, V, C = [1, 5, 6, 2, 6], [1, 2, 3, 4, 2], 10  # Solution: value = 8,    weight = 9,   decisions = (1, 0, 1, 1, 0))
    # W, V, C = create_knapsack_problem(20)           # Solution: value = 1118, weight = 344, decisions = (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
    W, V, C = create_knapsack_problem(
        35)  # Solution: value = 1830, weight = 543, decisions = (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    print("Solution: ", knapsack_bab_solve2(W, V, C))  # Solution:  (8, 9, (1, 0, 1, 1, 0))
