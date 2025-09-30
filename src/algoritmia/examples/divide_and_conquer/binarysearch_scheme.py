from typing import Self

from algoritmia.schemes.dac_scheme import IDecreaseAndConquerProblem, dec_solve, iter_dec_solve

type Solution = int  # La posición del elemento buscado

class BinarySearchProblem(IDecreaseAndConquerProblem[Solution]):
    def __init__(self, v: list[int], elem: int, start: int, end: int):
        self.v, self.elem, self.start, self.end = v, elem, start, end
        self.mid = (self.start + self.end) // 2

    def is_simple(self) -> bool:
        return self.end - self.start <= 1 or self.elem == self.v[self.mid]

    def trivial_solution(self) -> Solution | None:
        if self.elem == self.v[self.mid]:
            return self.mid
        if self.start == self.end or self.elem != self.v[self.start]:
            return None
        return self.start

    def decrease(self) -> Self:
        if self.elem < self.v[self.mid]:
            return BinarySearchProblem(self.v, self.elem, self.start, self.mid)
        else:
            return BinarySearchProblem(self.v, self.elem, self.mid + 1, self.end)


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
