from collections.abc import Iterator
from typing import Self

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions

# Tipos  --------------------------------------------------------------------------

type Decision = int  # Número de fila donde colocar la reina

# 'bt_solutions' devuelve un Iterator del tipo devuelto por el método 'solution' de
# la clase 'DecisionSequence', cuya implementación por defecto devuelve una tupla con las decisiones:
type Solution = tuple[Decision, ...]


# --------------------------------------------------------------------------------


def nqueens_solutions(board_size: int) -> Iterator[Solution]:
    class NQueensDS(DecisionSequence[Decision, None]):  # Como no hay Extra -> ponemos None
        def is_solution(self) -> bool:
            return len(self) == board_size

        def successors(self) -> Iterator[Self]:
            n = len(self)  # Número de decisiones ya tomadas (reinas colocadas)
            if n < board_size:  # Si quedan decisiones por tomar (reinas por colocar)
                for row in range(board_size):
                    if all(r != row and n - j != abs(row - r)
                           for j, r in enumerate(self.decisions())):
                        yield self.add_decision(row)

    initial_ds = NQueensDS()
    return bt_solutions(initial_ds)


# Programa principal -----------------------------------
if __name__ == "__main__":
    board_size0 = 4

    print('n-queens solutions for n=4:')
    has_solutions = False
    for sol in nqueens_solutions(board_size0):
        has_solutions = True
        print(f'\tSolution: {sol}')
    if not has_solutions:
        print('\tThere are no solutions')
