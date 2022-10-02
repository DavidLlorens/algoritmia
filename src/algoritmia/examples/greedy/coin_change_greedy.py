from typing import Optional


def coin_change_solve_naif(v: tuple[int, ...], Q: int) -> Optional[list[int]]:
    res: list[int] = []
    for i in range(len(v)):
        res.append(Q // v[i])
        Q = Q % v[i]
    if Q == 0:
        return res
    return None


def coin_change_solve(v: tuple[int, ...], Q: int) -> Optional[list[int]]:
    # Los índices para recorrer la lista v son la lista [0, 1, 3, ...]
    indices = list(range(len(v)))
    # Podemos ordenarlos para recorrer v de mayor a menor valor
    sorted_indices: list[int] = sorted(indices, key=lambda i: -v[i])

    res: list[int] = [0] * len(v)
    for i in sorted_indices:  # Si usamos 'indices' recorreremos v en orden
        res[i] = Q // v[i]
        Q = Q % v[i]
    if Q == 0:
        return res
    return None


if __name__ == '__main__':
    print(coin_change_solve((1, 2, 5, 10), 6))  # Ok: [1, 0, 1, 0]
    print(coin_change_solve((1, 9, 15), 19))  # Mal: [4, 0, 1]
    print(coin_change_solve((2, 9, 15), 10))  # Mal: None


if __name__ == '__main__':
    print(coin_change_solve_naif((1, 2, 5, 10), 6))  # [6, 0, 0, 0]
    print(coin_change_solve_naif((2, 5, 10), 7))  # None
    print(coin_change_solve_naif((1, 9, 15), 19))  # [19, 0, 0]
    print(coin_change_solve_naif((2, 9, 15), 10))  # [5, 0, 0]
    print()
    print(coin_change_solve((1, 2, 5, 10), 6))  # [1, 0, 1, 0]
    print(coin_change_solve((2, 5, 10), 7))  # [1, 1, 0]]
    print(coin_change_solve((1, 9, 15), 19))  # [4, 0, 1]
    print(coin_change_solve((2, 9, 15), 10))  # None
