from __future__ import annotations

from collections.abc import Iterator

from algoritmia.schemes.dac_scheme import IDivideAndConquerProblem, div_solve


class MergesortProblem(IDivideAndConquerProblem):
    def __init__(self, v: list[int]):
        self.v = v

    def is_simple(self) -> bool:
        return len(self.v) <= 1

    def trivial_solution(self) -> list[int]:
        return self.v

    def divide(self) -> Iterator[MergesortProblem]:
        half = len(self.v) // 2
        yield MergesortProblem(self.v[:half])
        yield MergesortProblem(self.v[half:])

    def combine(self, sols: Iterator[list[int]]) -> list[int]:
        left, right = sols
        c = [0] * (len(left) + len(right))  # Vector auxiliar
        i, j, k = 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                c[k] = left[i];  i += 1
            else:
                c[k] = right[j]; j += 1
            k += 1
        while i < len(left):  c[k] = left[i];  i += 1; k += 1
        while j < len(right): c[k] = right[j]; j += 1; k += 1
        return c


# Programa principal --------------------------------------
v0 = [11, 21, 3, 1, 98, 0, 12, 82, 29, 30, 11, 18, 43, 4, 75, 37]

# Creamos un problema que cumpla la interfaz IDivideAndConquerProblem
ms_problem0 = MergesortProblem(v0)

# Se lo pasamos a la función div_solve(...) que nos devuelve la solución
solution0 = div_solve(ms_problem0)
print(solution0)
