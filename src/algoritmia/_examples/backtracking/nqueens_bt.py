from collections.abc import Iterator
from typing import Self

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions

# Tipos  --------------------------------------------------------------------------

type Decision = int  # Número de fila donde colocar la reina
type Extra = None    # Este problema no necesita almacenar información adicional junto a la decisión

# Queremos que una solución sea la secuencia de decisiones (números de fila) en forma de tupla:
type Solution = tuple[Decision, ...]

# - 'bt_solutions' y 'bt_vc_solutions' devuelven un Iterator con las DecisionSequence que
#   llegan a una solución.
# - Pero un objeto DecisionSequence no es una tupla de decisiones: debemos utilizar el método
#   'decisions()' de la clase DecisionSequence para obtener la tupla.

# --------------------------------------------------------------------------------


def nqueens_solutions(board_size: int) -> Iterator[Solution]:
    class NQueensDS(DecisionSequence[Decision, Extra]):  # Hemos definido Extra como None
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
    for solution_ds in bt_solutions(initial_ds):
        yield solution_ds.decisions()  # Extraemos las decisiones del objeto solution_ds y las devolvemos


# Programa principal -----------------------------------
if __name__ == "__main__":
    board_size0 = 8

    print(f'n-queens solutions for n={board_size0}:')
    has_solutions = False
    for sol in nqueens_solutions(board_size0):
        has_solutions = True
        print(f'\tSolution: {sol}')
    if not has_solutions:
        print('\tThere are no solutions')
