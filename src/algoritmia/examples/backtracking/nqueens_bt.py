from __future__ import annotations  # Permite utilizar el tipo NQueensDS
                                    # dentro de la clase NQueensDS.

from collections.abc import Iterator

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve

Decision = int  # Número de fila donde colocar la reina

# 'bt_solve' devuelve un Iterator del tipo devuelto por el método 'solution' de
# la clase 'DecisionSequence', cuya implementación por defecto devuelve una tupla con las decisiones:
SolutionDS = tuple[Decision, ...]


def nqueens_solve(board_size: int) -> Iterator[SolutionDS]:
    class NQueensDS(DecisionSequence[Decision]):
        def is_solution(self) -> bool:
            return len(self) == board_size

        def successors(self) -> Iterator[NQueensDS]:
            n = len(self) # Número de decisiones ya tomadas (reinas colocadas)
            if n < board_size:  # Si quedan decisiones por tomar (reinas por colocar)
                for row in range(board_size):
                    if all(r != row and n - j != abs(row - r)
                           for j, r in enumerate(self.decisions())):
                        yield self.add_decision(row)

    initial_ds = NQueensDS()
    return bt_solve(initial_ds)


# Programa principal -----------------------------------
if __name__ == "__main__":
    board_size0 = 4

    print('Basic versión (all solutions):')
    has_solutions = False
    for sol in nqueens_solve(board_size0):
        has_solutions = True
        print(f'\tSolution: {sol}')
    if not has_solutions:
        print('\tThere are no solutions')
