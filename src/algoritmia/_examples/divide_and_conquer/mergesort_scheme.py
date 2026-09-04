from collections.abc import Iterable

from algoritmia.schemes.dac_scheme import IDivideAndConquerProblem, div_solve

type Solution = list[int]  # la lista ordenada

class MergesortProblem(IDivideAndConquerProblem[Solution]):
    def __init__(self, v: list[int]):
        self.v = v

    def is_simple(self) -> bool:
        return len(self.v) <= 1

    def trivial_solution(self) -> Solution:
        return self.v

    def divide(self) -> Iterable[MergesortProblem]:
        mid = len(self.v) // 2
        yield MergesortProblem(self.v[:mid])  # left_problem
        yield MergesortProblem(self.v[mid:])  # right_problem

    def combine(self, solutions: Iterable[Solution]) -> Solution:
        left_sol, right_sol = solutions
        c = [0] * (len(left_sol) + len(right_sol))  # vector auxiliar
        i, j, k = 0, 0, 0
        while i < len(left_sol) and j < len(right_sol):
            if left_sol[i] < right_sol[j]:
                c[k] = left_sol[i]; i += 1
            else:
                c[k] = right_sol[j]; j += 1
            k += 1
        while i < len(left_sol):  c[k] = left_sol[i];  i += 1; k += 1
        while j < len(right_sol): c[k] = right_sol[j]; j += 1; k += 1
        return c


# Programa principal --------------------------------------
if __name__ == "__main__":
    v0 = [11, 21, 3, 1, 98, 0, 12, 82, 29, 30, 11, 18, 43, 4, 75, 37]

    # Creamos un problema que cumpla la interfaz IDivideAndConquerProblem
    ms_problem0 = MergesortProblem(v0)

    # Se lo pasamos a la función div_solve(...) que nos devuelve la solución
    solution0 = div_solve(ms_problem0)
    print(solution0)
