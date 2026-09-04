# Dado el vector de valores y una solución, devuelve el valor de dicha solución
def total_value(v: list[int], sol: list[float]) -> float:
    return sum([x_i * v[i] for i, x_i in enumerate(sol)])


def frac_knapsack0(C: int, v: list[int], w: list[int]) -> list[float]:
    c: float = float(C)
    x: list[float] = [0.0] * len(w)
    for i in range(len(w)):
        x[i] = min(1.0, c / w[i])
        c -= x[i] * w[i]
    return x


def frac_knapsack(C: int, v: list[int], w: list[int]) -> list[float]:
    sorted_indices: list[int] = sorted(range(len(w)), key=lambda i: -v[i] / w[i])
    c: float = float(C)
    x: list[float] = [0.0] * len(w)
    for i in sorted_indices:
        x[i] = min(1.0, c / w[i])
        c -= x[i] * w[i]
    return x


if __name__ == '__main__':
    capacity, values, weights = 50, [60, 30, 40, 20, 75], [40, 30, 20, 10, 50]

    solution = frac_knapsack0(capacity, values, weights)
    print(solution, total_value(values, solution))  # Mal: [1, 0.3333333, 0, 0, 0] 70.0

    solution = frac_knapsack(capacity, values, weights)
    print(solution, total_value(values, solution))  # Ok: [0.5, 0, 1, 1, 0] 90.0
