from __future__ import annotations

from typing import Optional

from algoritmia.schemes.dac_scheme import IDecreaseAndConquerProblem, dec_solve, iter_dec_solve


class BinarySearchProblem(IDecreaseAndConquerProblem):
    def __init__(self, v: list[int], elem: int, begin: int, end: int):
        self.v, self.elem, self.begin, self.end = v, elem, begin, end

    def is_simple(self) -> bool:
        return self.end - self.begin <= 1

    def trivial_solution(self) -> Optional[int]:
        if self.begin == self.end or self.elem != self.v[self.begin]:
            return None
        return self.begin

    def decrease(self) -> BinarySearchProblem:
        h = (self.begin + self.end) // 2
        if self.elem < self.v[h]:
            return BinarySearchProblem(self.v, self.elem, self.begin, h)
        elif self.elem > self.v[h]:
            return BinarySearchProblem(self.v, self.elem, h + 1, self.end)
        else:  # self.elem == self.v[h]:
            return BinarySearchProblem(self.v, self.elem, h, h + 1)


if __name__ == "__main__":
    my_sorted_list = [2, 3, 3, 11, 12, 18, 21, 29, 30, 37, 43, 75, 82, 98]
    num = 30
    problem = BinarySearchProblem(my_sorted_list, num, 0, len(my_sorted_list))
    pos = dec_solve(problem)
    print('dec_solve: Valor {} en {}.'.format(num, pos))
    pos = iter_dec_solve(problem)
    print('iter_dec_solve: Valor {} en {}.'.format(num, pos))