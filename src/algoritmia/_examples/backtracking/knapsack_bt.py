from collections.abc import Iterator
from dataclasses import dataclass
from random import seed, randint
from typing import Self

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, bt_vc_solutions, max_solution

# Tipos  --------------------------------------------------------------------------

type Decision = int                     # 1 o 0, (coger o no, el objeto)
type Score = int                        # El valor de la mochila

# Queremos que una solución sea la secuencia de decisiones (1/0) en forma de tupla:
type Solution = tuple[Decision, ...]

# - 'bt_solutions' y 'bt_vc_solutions' devuelven un Iterator con las DecisionSequence que
#   llegan a una solución.
# - Pero un objeto DecisionSequence no es una tupla de decisiones: debemos utilizar el método
#   'decisions()' de la clase DecisionSequence para obtener la tupla.

# Esquema básico  --------------------------------------------------------------------------

def knapsack_solutions(weights: list[int],
                       values: list[int],
                       capacity: int) -> Iterator[Solution]:
    @dataclass
    class Extra:
        weight: int = 0

    class KnapsackDS(DecisionSequence[Decision, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(values)

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(values):
                new_weight = self.extra.weight + weights[n]
                if new_weight <= capacity:
                    yield self.add_decision(1, Extra(new_weight))
                yield self.add_decision(0, self.extra)

    initial_ds = KnapsackDS(Extra())
    for solution_ds in bt_solutions(initial_ds):
        yield solution_ds.decisions()  # Extraemos las decisiones del objeto solution_ds y las devolvemos


type ScoredSolution = tuple[int, Solution]


def knapsack_best_solution(weights: list[int],
                           values: list[int],
                           capacity: int) -> ScoredSolution | None:
    def f(solution: Solution) -> int:
        return sum(d * values[i] for i, d in enumerate(solution))

    all_solutions: Iterator[Solution] = knapsack_solutions(weights, values, capacity)
    return max_solution(all_solutions, f)


# Esquema con control de visitados  --------------------------------------------------------------------------

def knapsack_vc_solutions(weights: list[int],
                          values: list[int],
                          capacity: int) -> Iterator[Solution]:
    @dataclass
    class Extra:
        weight: int = 0

    class KnapsackDS(DecisionSequence[Decision, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(values)

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(values):
                new_weight = self.extra.weight + weights[n]
                if new_weight <= capacity:
                    yield self.add_decision(1, Extra(new_weight))
                yield self.add_decision(0, self.extra)

        def state(self):
            return len(self), self.extra.weight

    initial_ds = KnapsackDS(Extra())
    for solution_ds in bt_vc_solutions(initial_ds):
        yield solution_ds.decisions()


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

    for W, V, C in [i1, i2]:
        print("-" * 80)
        print(f"Instancia:\n  Pesos = {W}\n  Valores = {V}\n  Capacidad = {C}\n")
        print(f"knapsack_solutions    - Number of solutions: {len(list(knapsack_solutions(W, V, C)))}")
        print(f"knapsack_solutions    - Best solution: {knapsack_best_solution(W, V, C)}")
        print(f"knapsack_vc_solutions - Number of solutions: {len(list(knapsack_vc_solutions(W, V, C)))}")
    print("-" * 80)
