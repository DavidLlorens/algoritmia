from typing import Union

from algoritmia.utils import infinity

Quantity = int  # La cantidad a devolver
Decision = int  # Un número de de monedas
Score = Union[int, float]  # La puntuación es el número de monedas utilizadas o, si no hay solución, +infinito

LParams = tuple[int, Quantity]
Solution = tuple[Score, list[Decision]]


def solve(q: Quantity, v: list[int]) -> Solution:
    def L(n: int, q: Quantity) -> Score:
        if n == 0:
            return 0 if q == 0 else infinity
        if (n, q) not in mem:
            res: list[tuple[Score, LParams, Decision]] = []
            for d in range(q // v[n - 1] + 1):
                c_score = L(n - 1, q - d * v[n - 1]) + d
                previous = (n - 1, q - d * v[n - 1])
                res.append((c_score, previous, d))
            mem[n, q] = min(res)
        return mem[n, q][0]

    mem: dict[LParams, tuple[Score, LParams, Decision]] = {}
    score = L(len(v), q)
    n = len(v)
    sol = []
    while n > 0:
        _, (n, q), d = mem[n, q]
        sol.append(d)
    sol.reverse()
    return score, sol


if __name__ == '__main__':
    v: list[int] = [1, 2, 5, 10]
    q: Quantity = 11
    print("Instance:", q, v)
    print("Solution:", solve(q, v))
