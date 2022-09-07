from random import seed, randint


def solve(c: int, w: list[int], v: list[int]) -> tuple[int, list[int]]:
    def L(n: int, c: int) -> int:
        if n == 0:
            return 0
        if (n, c) not in mem:
            mem[n, c] = (L(n - 1, c), (n - 1, c, 0))
            if w[n - 1] <= c:
                mem[n, c] = max(mem[n, c],
                                (L(n - 1, c - w[n - 1]) + v[n - 1], (n - 1, c - w[n - 1], 1)))
        return mem[n, c][0]

    mem = {}
    score = L(len(v), c)
    n = len(v)
    sol = []
    while n > 0:
        _, (n, c, d) = mem[n, c]
        sol.append(d)
    sol.reverse()
    return score, sol


def solve2(c: int, w: list[int], v: list[int]) -> tuple[int, list[int]]:
    def L(n: int, c: int) -> int:
        if n == 0:
            return 0
        if (n, c) not in mem:
            res = []
            for d in range(n):
                if w[d] <= c:
                    res.append((L(d, c - w[d]) + v[d], (d, c - w[d], d)))
            if len(res) == 0:
                mem[n, c] = 0, (0, c, None)
            else:
                mem[n, c] = max(res)
        return mem[n, c][0]

    mem = {}
    score = L(len(v), c)
    n = len(v)
    sol = []
    while n > 0:
        _, (n, c, d) = mem[n, c]
        if d is None: break
        sol.append(d)
    sol.reverse()
    return score, sol


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
    w, v, c = [1, 5, 6, 2, 6], [1, 2, 3, 4, 2], 10  # Solution: value = 8,weight = 9,decisions = (1, 0, 1, 1, 0))
    # w, v, c = create_knapsack_problem(20)  # Solution: value = 1118, weight = 344, decisions = (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
    # w, v, c = create_knapsack_problem(35)  # Solution: value = 1830, weight = 543, decisions = (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    print("Instance:", c, w, v)
    print("Solution1:", solve(c, w, v))
    print("Solution2:", solve2(c, w, v))
