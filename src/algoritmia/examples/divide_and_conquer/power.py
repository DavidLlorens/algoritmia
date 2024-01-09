def power_naif(a: float, n: int) -> float:
    if n == 0:
        return 1
    elif n == 1:
        return a
    elif n % 2 == 0:
        return power_naif(a, n // 2) * power_naif(a, n // 2)
    else:
        return power_naif(a, n // 2) * power_naif(a, n // 2 + 1)


def power(a: float, n: int) -> float:
    if n == 0:
        return 1
    elif n == 1:
        return a
    elif n % 2 == 0:
        return power(a, n // 2) ** 2
    else:
        return a * power(a, n // 2) ** 2


if __name__ == '__main__':
    print(power_naif(45, 16))
    print(power(45, 16))
