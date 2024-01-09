#
# Problema del cambio generalizado
#  - Las monedas tiene peso
#  - La solución óptima es la de menor peso
#

from algoritmia.utils import infinity

type Decision = int  # Un número de de monedas
type Solution = list[Decision]

type Score = int | float  # La puntuación es el número de monedas utilizadas o, si no hay solución, infinity
type ScoredSolution = tuple[Score, Solution]

type SParams = tuple[int, int]  # Una tupla con los parámetros de S: (q, n)


def coin_change_no_mem(v: list[int], w: list[int], Q: int) -> Score:
    def S(q: int, n: int) -> Score:
        # Casos base
        if n == 0 and q == 0: return 0
        if n == 0 and q > 0: return infinity

        # Recursividad
        best_score = infinity
        for d in range(q // v[n - 1] + 1):
            q_previo, n_previo = q - d * v[n - 1], n - 1
            current_score = S(q_previo, n_previo) + d * w[n - 1]
            if current_score < best_score:  # Minimización
                best_score = current_score
        return best_score

    return S(Q, len(v))


def coin_change_mem(v: list[int], w: list[int], Q: int) -> Score:
    def S(q: int, n: int) -> Score:
        # Casos base
        if q == 0 and n == 0: return 0
        if q > 0 and n == 0: return infinity

        # Recursividad con memoización
        if (q, n) not in mem:
            mem[q, n] = infinity
            for d in range(q // v[n - 1] + 1):
                q_previo, n_previo = q - d * v[n - 1], n - 1
                current_score = S(q_previo, n_previo) + d * w[n - 1]
                if current_score < mem[q, n]:  # Minimización
                    mem[q, n] = current_score
        return mem[q, n]

    mem: dict[SParams, Score] = {}
    return S(Q, len(v))


def coin_change_rec(v: list[int], w: list[int], Q: int) -> ScoredSolution:
    def S(q: int, n: int) -> Score:
        # Casos base
        if q == 0 and n == 0: return 0
        if q > 0 and n == 0: return infinity

        # Recursividad con memoización
        if (q, n) not in mem:
            mem[q, n] = infinity, (-1, -1), -1
            for d in range(q // v[n - 1] + 1):
                q_previo, n_previo = q - d * v[n - 1], n - 1
                current_score = S(q_previo, n_previo) + d * w[n - 1]
                if current_score < mem[q, n][0]:  # Minimización
                    mem[q, n] = current_score, (q_previo, n_previo), d
        return mem[q, n][0]

    mem: dict[SParams, tuple[Score, SParams, Decision]] = {}

    # La puntuación (peso) de la solución óptima
    score = S(Q, len(v))

    # Recupera las decisiones
    decisions: list[Decision] = []
    if score != infinity:
        q, n = Q, len(v)
        while (q, n) != (0, 0):
            _, (q, n), d = mem[q, n]
            decisions.append(d)
        decisions.reverse()

    return score, decisions


def coin_change_iter(v: list[int], w: list[int], Q: int) -> ScoredSolution:
    mem: dict[SParams, tuple[Score, SParams, Decision]] = {}

    # Rellena mem[., 0]
    mem[0, 0] = 0, (-1, -1), -1
    for q in range(1, Q + 1):
        mem[q, 0] = infinity, (-1, -1), -1

    for n in range(1, len(v) + 1):
        # Rellena mem[., n]
        for q in range(0, Q + 1):
            mem[q, n] = infinity, (-1, -1), -1
            for d in range(q // v[n - 1] + 1):
                q_previo, n_previo = q - d * v[n - 1], n - 1
                current_score = mem[q_previo, n_previo][0] + d * w[n - 1]
                if current_score < mem[q, n][0]:  # Minimización
                    mem[q, n] = current_score, (q_previo, n_previo), d

    # La puntuación (peso) de la solución óptima
    score = mem[Q, len(v)][0]

    # Recupera las decisiones
    decisions: list[Decision] = []
    if score != infinity:
        q, n = Q, len(v)
        while (q, n) != (0, 0):
            _, (q, n), d = mem[q, n]
            decisions.append(d)
        decisions.reverse()

    return score, decisions


def coin_change_iter_score(v: list[int], w: list[int], Q: int) -> Score:
    previous: list[Score] = [infinity] * (Q + 1)  # n = -1 (reserva memoria)
    current: list[Score] = [0] + [infinity] * Q   # n = 0
    for n in range(1, len(v) + 1):
        current, previous = previous, current
        for q in range(0, Q + 1):
            current[q] = infinity
            for d in range(q // v[n - 1] + 1):
                current_score = previous[q - d * v[n - 1]] + d * w[n - 1]
                if current_score < current[q]:
                    current[q] = current_score
    return current[Q]


if __name__ == '__main__':
    Q0, v0, w0 = 7, [1, 2, 4], [2, 3, 9]
    print(f"Instance:\n  Q = {Q0}\n  v = {v0}\n  w = {w0}\n")
    print("coin_change_no_mem:", coin_change_no_mem(v0, w0, Q0))
    print("coin_change_mem:", coin_change_mem(v0, w0, Q0))
    print("coin_change_rec:", coin_change_rec(v0, w0, Q0))
    print("coin_change_iter:", coin_change_iter(v0, w0, Q0))
    print("coin_change_iter_score:", coin_change_iter_score(v0, w0, Q0))
