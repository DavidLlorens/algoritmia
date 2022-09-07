from typing import *

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve, Solution


def nqueens_solve(n: int) -> Iterable[Solution]:
    class NQueensDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(self) == n

        def successors(self) -> Iterable["NQueensDS"]:
            t = len(self)
            if t < n:
                decisions = self.decisions()
                for row in range(n):
                    if all(r != row and t - j != abs(row - r)
                           for j, r in enumerate(decisions)):
                        yield self.add_decision(row)

    initial_ds = NQueensDS()
    return bt_solve(initial_ds)


# Programa principal
if __name__ == "__main__":
    board_size = 4
    for sol in nqueens_solve(board_size):
        print(sol)
