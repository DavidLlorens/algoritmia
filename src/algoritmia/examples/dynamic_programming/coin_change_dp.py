from algoritmia.utils import infinity


def solve(q: int, v: list[int]) -> tuple[int, list[int]]:
    def L(n, q):
        if n == 0:
            return 0 if q == 0 else infinity
        if (n, q) not in mem:
            mem[n, q] = min(
                [(L(n - 1, q - d * v[n - 1]) + d, (n - 1, q - d * v[n - 1], d)) for d in range(q // v[n - 1] + 1)])
        return mem[n, q][0]

    mem = {}
    score = L(len(v), q)
    n = len(v)
    sol = []
    while n > 0:
        _, (n, q, d) = mem[n, q]
        sol.append(d)
    sol.reverse()
    return score, sol


if __name__ == '__main__':
    v, q = [1, 2, 5, 10], 11
    print("Instance:", q, v)
    print("Solution:", solve(q, v))
