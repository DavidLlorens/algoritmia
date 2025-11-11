import unittest
from dataclasses import dataclass
from typing import Iterator, Self

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, min_solution


class TestBT_SOLUTIONS(unittest.TestCase):

    def test_4queens_bt_solutions(self):
        class NQueensDS(DecisionSequence[int, None]):
            def is_solution(self) -> bool:
                return len(self) == board_size

            def successors(self) -> Iterator[Self]:
                n = len(self)
                if n < board_size:
                    for row in range(board_size):
                        if all(r != row and n - j != abs(row -r)
                               for j, r in enumerate(self.decisions())):
                            yield self.add_decision(row)

        board_size = 4
        initial_ds = NQueensDS()
        solutions = tuple(tuple(s) for s in bt_solutions(initial_ds))
        self.assertEqual(((1, 3, 0, 2), (2, 0, 3, 1)), solutions)

    def test_coinchange_min_solution(self):
        @dataclass
        class Extra:
            pending: int

        class CoinChangeDS(DecisionSequence[int, Extra]):
            def is_solution(self) -> bool:
                return len(self) == len(v) and self.extra.pending == 0

            def successors(self) -> Iterator[Self]:
                n = len(self)
                if n < len(v):
                    for num_coins in range(self.extra.pending // v[n] + 1):
                        pending2 = self.extra.pending - num_coins * v[n]
                        yield self.add_decision(num_coins, Extra(pending2))

        v, Q = (1, 2, 5, 10), 4
        initial_ds = CoinChangeDS(Extra(Q))
        solutions = bt_solutions(initial_ds)
        solution = min_solution(solutions, sum)
        solution = (solution[0], tuple(solution[1]))
        self.assertEqual((2, (0, 2, 0, 0)), solution)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
