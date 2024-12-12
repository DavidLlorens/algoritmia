"""

Version: 6.0 (23-oct-2024) - Añade tipo genérico TSolution y cambia Iterator por Iterable
         5.2 (01-dic-2023)
         4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2024
@license: GPL3
"""
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Self


# Divide and conquer -----------------------------------------------------------

class IDivideAndConquerProblem[TSolution](ABC):
    @abstractmethod
    def is_simple(self) -> bool: pass

    @abstractmethod
    def trivial_solution(self) -> TSolution: pass

    @abstractmethod
    def divide(self) -> Iterable[Self]: pass

    @abstractmethod
    def combine(self, solutions: Iterable[TSolution]) -> TSolution: pass


def div_solve[TSolution](problem: IDivideAndConquerProblem[TSolution]) -> TSolution:
    if problem.is_simple():
        return problem.trivial_solution()
    else:
        subproblems = problem.divide()
        solutions = (div_solve(p) for p in subproblems)
        return problem.combine(solutions)


# Decrease and conquer -----------------------------------------------------------

class IDecreaseAndConquerProblem[TSolution](ABC):
    @abstractmethod
    def is_simple(self) -> bool: pass

    @abstractmethod
    def trivial_solution(self) -> TSolution: pass

    @abstractmethod
    def decrease(self) -> Self: pass

    def process(self, s: TSolution) -> TSolution:
        return s


def dec_solve[TSolution](problem: IDecreaseAndConquerProblem[TSolution]) -> TSolution:
    if problem.is_simple():
        return problem.trivial_solution()
    else:
        smaller_problem = problem.decrease()
        smaller_solution = dec_solve(smaller_problem)
        return problem.process(smaller_solution)


def tail_dec_solve[TSolution](problem: IDecreaseAndConquerProblem[TSolution]) -> TSolution:
    if problem.is_simple():
        return problem.trivial_solution()
    else:
        return tail_dec_solve(problem.decrease())


def iter_dec_solve[TSolution](problem: IDecreaseAndConquerProblem[TSolution]) -> TSolution:
    while not problem.is_simple():
        problem = problem.decrease()
    return problem.trivial_solution()
