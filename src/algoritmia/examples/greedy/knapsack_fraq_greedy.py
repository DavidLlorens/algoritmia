# Dado el vector de valores y una solución, devuelve el valor de dicha solución
def beneficio(v: list[int], sol: list[float]) -> float:
    return sum([x_i * v[i] for i, x_i in enumerate(sol)])


def mochila_fraq0(C: int, v: list[int], w: list[int]) -> list[float]:
    x = [0.0] * len(w)
    for i in range(len(w)):
        x[i] = min(1.0, C / w[i])
        C -= x[i] * w[i]
    return x


def mochila_fraq(C: int, v: list[int], w: list[int]) -> list[float]:
    indices_ordenados = sorted(range(len(w)), key=lambda i: -v[i] / w[i])
    x = [0.0] * len(w)
    for i in indices_ordenados:
        x[i] = min(1.0, C / w[i])
        C -= x[i] * w[i]
    return x


if __name__ == '__main__':
    capacity, values, weights = 50, [60, 30, 40, 20, 75], [40, 30, 20, 10, 50]

    solution = mochila_fraq0(capacity, values, weights)
    print(solution, beneficio(values, solution))  # [1, 0.3333333, 0, 0, 0] 70.0

    solution = mochila_fraq(capacity, values, weights)
    print(solution, beneficio(values, solution))  # [0.5, 0, 1, 1, 0] 90.0
