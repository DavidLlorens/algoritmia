from __future__ import annotations

from typing import Optional

from algoritmia.schemes.dac_scheme import IDecreaseAndConquerProblem, dec_solve, iter_dec_solve


class BinarySearchProblem(IDecreaseAndConquerProblem):
    def __init__(self, v: list[int], elem: int, start: int, end: int):
        self.v, self.elem, self.start, self.end = v, elem, start, end

    def is_simple(self) -> bool:
        return self.end - self.start <= 1

    def trivial_solution(self) -> Optional[int]:
        if self.start == self.end or self.elem != self.v[self.start]:
            return None
        return self.start

    def decrease(self) -> BinarySearchProblem:
        h = (self.start + self.end) // 2
        if self.elem < self.v[h]:
            return BinarySearchProblem(self.v, self.elem, self.start, h)
        elif self.elem > self.v[h]:
            return BinarySearchProblem(self.v, self.elem, h + 1, self.end)
        else:  # self.elem == self.v[h]:
            return BinarySearchProblem(self.v, self.elem, h, h + 1)


if __name__ == "__main__":
    my_sorted_list = [2, 3, 3, 11, 12, 18, 21, 29, 30, 37, 43, 75, 82, 98]
    num = 30
    print('list:', my_sorted_list)
    print('number to find:', num)
    problem = BinarySearchProblem(my_sorted_list, num, 0, len(my_sorted_list))

    pos = dec_solve(problem)

    print(f'dec_solve: number found at index {pos}')
    pos = iter_dec_solve(problem)
    print(f'iter_dec_solve: number found at index {pos}')
