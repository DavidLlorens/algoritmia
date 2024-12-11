import unittest
from dataclasses import dataclass
from typing import Iterator, Self

from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_max_solve


class TestBAB_SOLUTIONS(unittest.TestCase):

    def test_knapsack_bab_max_solve(self):
        Score = int
        State = tuple[int, int]

        @dataclass
        class Extra:
            weight: int
            value: int

        class KnapsackBabDS(BabDecisionSequence[int, Extra, Score]):
            def calculate_opt_bound(self) -> Score:
                return self.extra.value + sum(values[len(self):])

            def calculate_pes_bound(self) -> Score:
                return self.extra.value + 0  # No coge ninguno

            def is_solution(self) -> bool:
                return len(self) == len(values)

            def successors(self) -> Iterator[Self]:
                n = len(self)

                if n < len(values):
                    if self.extra.weight + weights[n] <= capacity:
                        new_weight = self.extra.weight + weights[n]
                        new_value = self.extra.value + values[n]
                        yield self.add_decision(1, Extra(new_weight, new_value))
                    yield self.add_decision(0, self.extra)

            def state(self) -> State:
                return len(self), self.extra.weight

        weights = [ 42,  55,  93, 89, 98, 77]
        values =  [168, 110, 186, 89, 98, 77]
        capacity = 136
        initial_ds = KnapsackBabDS(Extra(0, 0))
        score, solution_ds = bab_max_solve(initial_ds)
        solution = score, solution_ds.decisions()

        self.assertEqual((354, (1, 0, 1, 0, 0, 0)), solution)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
