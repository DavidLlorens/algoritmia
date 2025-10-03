from typing import Optional


def binarysearch_tail_rec(v: list[int], elem: int) -> Optional[int]:
    def rec(start: int, end: int):
        if end - start == 0:
            return None
        mid = (start + end) // 2
        if elem < v[mid]:
            return rec(start, mid)
        elif elem > v[mid]:
            return rec(mid + 1, end)
        else:  # elem == v[mid]:
            return mid

    return rec(0, len(v))


def binarysearch_iter(v: list[int], elem: int) -> Optional[int]:
    start, end = 0, len(v)
    while end - start > 0:
        mid = (start + end) // 2
        if elem < v[mid]:
            end = mid
        elif elem > v[mid]:
            start = mid + 1
        else:  # elem == v[mid]:
            return mid


if __name__ == "__main__":
    my_sorted_list = [2, 3, 3, 11, 12, 18, 21, 29, 30, 37, 43, 75, 82, 98]
    num = 30
    print('list:', my_sorted_list)
    print('number to find:', num)

    pos = binarysearch_tail_rec(my_sorted_list, num)
    print(f'binarysearch_tail_rec: number found at index {pos}')

    pos = binarysearch_iter(my_sorted_list, num)
    print(f'binarysearch_iter: number found at index {pos}')
