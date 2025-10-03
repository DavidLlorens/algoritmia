#
# Problema del cambio
#  - La solución óptima es la que utiliza menos monedas
#

from algoritmia.utils import infinity

# ------------------------------------------------------------------------------------------

type Quantity = int  # La cantidad a devolver

type Decision = int  # Un número de de monedas
type Solution = list[Decision]

type Score = int | float  # La puntuación es el número de monedas utilizadas o, si no hay solución, +infinito
type Result = tuple[Score, Solution] | None

type SParams = tuple[Quantity, int]

# ------------------------------------------------------------------------------------------

def solve(Q: Quantity, v: list[int]) -> Result:
    def S(q: Quantity, n: int) -> Score:
        # Casos base
        if n == 0 and q == 0: return 0
        if n == 0 and q > 0: return infinity
        # Recursividad memoizada
        if (q, n) not in mem:
            #mem[q, n] = min(((S(q - d * v[n - 1], n - 1) + d, (q - d * v[n - 1], n - 1), d)
            #                for d in range(q // v[n - 1] + 1)), default=infinity)
            mem[q, n] = infinity, (-1, -1), -1
            for d in range(q // v[n - 1] + 1):
               q_prev, n_prev = q - d * v[n - 1], n - 1
               current_score = S(q_prev, n_prev) + d
               mem[q, n] = min(mem[q, n], (current_score, (q_prev, n_prev), d))
        return mem[q, n][0]

    mem: dict[SParams, tuple[Score, SParams, Decision]] = {}
    score = S(Q, len(v))
    if score == infinity: return None
    # Si hay solución, la recuperamos de mem
    decisions = []
    q, n = Q, len(v)
    while n > 0:
        _, (q, n), d = mem[q, n]
        decisions.append(d)
    decisions.reverse()
    return score, decisions

# ------------------------------------------------------------------------------------------

if __name__ == '__main__':
    Q0, v0 = 11, [1, 2, 5, 10]
    print("Instance:")
    print(f"  Q: {Q0}")
    print(f"  v: {v0}\n")

    print("Result:", solve(Q0, v0))
