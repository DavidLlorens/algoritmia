def mergesort_basic(v: list[int]) -> list[int]:
    def merge(left: list[int], right: list[int]) -> list[int]:
        c = [0] * (len(left) + len(right))
        i, j, k = 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                c[k] = left[i]
                i += 1
            else:
                c[k] = right[j]
                j += 1
            k += 1
        while i < len(left): c[k] = left[i]; i += 1; k += 1
        while j < len(right): c[k] = right[j]; j += 1; k += 1
        return c

    if len(v) <= 1:
        return v
    else:
        h = len(v) // 2
        return merge(mergesort_basic(v[:h]), mergesort_basic(v[h:]))


def mergesort(v: list[int]):
    def merge(begin: int, end: int, c: list[int]):
        half = (begin + end) // 2
        i, j, k = begin, half, begin
        while i < half and j < end:
            if v[i] < v[j]:
                c[k] = v[i]
                i += 1
            else:
                c[k] = v[j]
                j += 1
            k += 1
        while i < half: c[k] = v[i]; i += 1; k += 1
        while j < end: c[k] = v[j]; j += 1; k += 1
        for k in range(begin, end): v[k] = c[k]

    def rec(begin: int, end: int, c: list[int]):
        if end - begin > 1:
            half = (begin + end) // 2
            rec(begin, half, c)
            rec(half, end, c)
            merge(begin, end, c)

    rec(0, len(v), [0] * len(v))


if __name__ == "__main__":
    v0 = [11, 21, 3, 1, 98, 0, 12, 82, 29, 30, 11, 18, 43, 4, 75, 37]
    v1 = v0[:]
    print(mergesort_basic(v0))

    mergesort(v1)
    print(v1)
