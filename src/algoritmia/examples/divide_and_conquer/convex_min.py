def convex_min(v: list[int]) -> int:
    def _min(start: int, end: int) -> int:
        if end - start == 1:
            return v[start]
        elif end - start == 2:
            return min(v[start], v[start + 1])
        else:
            half = (start + end) // 2
            if v[half - 1] < v[half]:
                return _min(start, half)
            else:
                return _min(half, end)

    return _min(0, len(v))


if __name__ == '__main__':
    v0 = [9, 8, 6, 5, 4, 4, 3, 2, 5, 6, 8]
    print(convex_min(v0))
