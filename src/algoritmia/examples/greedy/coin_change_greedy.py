from typing import *


def coin_change_solve_naif(v: tuple[int, ...], Q: int) -> Optional[list[int]]:
    res = []
    for v_i in v:
        res.append(Q // v_i)
        Q = Q % v_i
    if Q == 0:
        return res
    return None


def coin_change_solve(v: tuple[int, ...], Q: int) -> Optional[list[int]]:
    # creamos vector de índices para recorrer 'valores' de mayor a menor valor
    indices_ordenados = sorted(range(len(v)), key=lambda i: -v[i])

    res = [0] * len(v)
    for i in indices_ordenados:
        res[i] = Q // v[i]
        Q = Q % v[i]
    if Q == 0:
        return res
    return None


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
