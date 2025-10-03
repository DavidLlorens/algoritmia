def quicksort_basic(v: list[int]) -> list[int]:
    if len(v) <= 1:
        return v
    else:
        pivot = v[0]
        left = [x for x in v if x < pivot]
        right = [x for x in v[1:] if x >= pivot]
        return quicksort_basic(left) + [pivot] + quicksort_basic(right)


def quicksort(v: list[int]):
    def partition(p: int, r: int) -> int:
        pivot, i = v[r - 1], p - 1
        for j in range(p, r - 1):
            if v[j] <= pivot:
                i += 1
                v[i], v[j] = v[j], v[i]
        v[i + 1], v[r - 1] = v[r - 1], v[i + 1]
        return i + 1

    def rec(p: int, r: int):
        if r - p > 1:
            pivot_index = partition(p, r)
            rec(p, pivot_index)
            rec(pivot_index + 1, r)

    rec(0, len(v))


if __name__ == "__main__":
    v0 = [11, 21, 3, 1, 98, 0, 12, 82, 29, 30, 11, 18, 43, 4, 75, 37]
    v1 = v0[:]

    print('quicksort_basic:', quicksort_basic(v0))

    quicksort(v1)
    print('quicksort:', v1)
