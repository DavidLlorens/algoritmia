from random import seed, randint

type Capacity = int
type Weight = int
type Value = int

type Decision = int  # 0 o 1
type Solution = list[Decision]

type Score = int
type Result = tuple[Score, Solution]  # Siempre habrá solución, no hace falta añadir None

type SParams = tuple[Capacity, int]


# Una solucion son len(v) valores (cada uno puede ser 0 o 1)
# C.E. = O(C N)
# C.T. = O(C N)
def solve(C: Capacity, w: list[Weight], v: list[Value]) -> Result:
    def S(c: Capacity, n: int) -> Score:
        # Caso base
        if n == 0: return 0
        # Recursividad memoizada
        if (c, n) not in mem:
            if w[n - 1] <= c:  # El objeto cabe
                mem[c, n] = max((S(c, n - 1),                       (c, n - 1),    0),
                                (S(c - w[n - 1], n - 1) + v[n - 1], (c - w[n - 1], n - 1), 1))
            else:  # El objeto no cabe
                mem[c, n] = S(c, n - 1), (c, n - 1), 0
        return mem[c, n][0]

    mem: dict[SParams, tuple[Score, SParams, Decision]] = {}
    score = S(C, len(v))
    # Recuperamos la solución de mem
    decisions = []
    c, n = C, len(v)
    while n > 0:
        _, (c, n), d = mem[c, n]
        decisions.append(d)
    decisions.reverse()
    return score, decisions


# Una solucion son K valores (los índices de los objetos que metemos en la mochila)
# C.E. = O(C N)
# C.T. = O(C N^2)
def solve2(C: Capacity, w: list[Weight], v: list[Value]) -> Result:
    def S(c: Capacity, n: int) -> Score:
        # Caso base
        if n == 0:
            return 0

        # Recursividad con memoización
        if (c, n) not in mem:
            mem[c, n] = 0, (c, 0), -1  # S no cabe ningún objeto más, quedará c espacio libre
            for d in range(n):
                c_prev, n_prev = c - w[d], d
                if w[d] <= c:
                    mem[c, n] = max(mem[c, n],
                                    (S(c_prev, n_prev) + v[d], (c_prev, n_prev), d))
        return mem[c, n][0]

    mem: dict[SParams, tuple[Score, SParams, Decision]] = {}
    score = S(C, len(v))
    # Recuperación del camino
    c, n = C, len(v)
    decisions = []
    while n > 0:
        _, (c, n), d = mem[c, n]
        if d != -1:
            decisions.append(d)
    decisions.reverse()
    return score, decisions


def sorted_by_dec_ratio(w_old, v_old):
    idxs = sorted(range(len(w_old)), key=lambda i: -v_old[i] / w_old[i])
    w_new = [w_old[i] for i in idxs]
    v_new = [v_old[i] for i in idxs]
    return w_new, v_new


def create_knapsack_problem(num_objects):
    seed(5)
    w_new = [randint(10, 100) for _ in range(num_objects)]
    v_new = [w_new[i] * randint(1, 4) for i in range(num_objects)]
    capacity = int(sum(w_new) * 0.3)
    weights, values = sorted_by_dec_ratio(w_new, v_new)
    return weights, values, capacity


if __name__ == '__main__':
    w0, v0, C0 = [4, 5, 3, 2, 6], [3, 2, 2, 3, 2], 9  # Solution: value = 8,weight = 9,decisions = (1, 0, 1, 1, 0))
    # w0, v0, C0 = create_knapsack_problem(20)  # Solution: value = 1118, weight = 344, decisions = (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
    # w0, v0, C0 = create_knapsack_problem(35)  # Solution: value = 1830, weight = 543, decisions = (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    print("Instance:", C0, w0, v0)
    print("Result (traditional X):", solve(C0, w0, v0))
    print("Result (alternative X):", solve2(C0, w0, v0))
