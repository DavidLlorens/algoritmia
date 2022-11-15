def convex_min(v: list[int]) -> int:
    def _min(begin: int, end: int) -> int:
        if end - begin == 1:
            return v[begin]
        elif end - begin == 2:
            return min(v[begin], v[begin + 1])
        else:
            half = (begin + end) // 2
            if v[half - 1] < v[half]:
                return _min(begin, half)
            else:
                return _min(half, end)

    return _min(0, len(v))


if __name__ == '__main__':
    v0 = [9, 8, 6, 5, 4, 4, 3, 2, 5, 6, 8]
    print(convex_min(v0))
