"""
Version: 4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2021
@license: GPL3
"""
from abc import ABC, abstractmethod
from typing import *

Solution = TypeVar('Solution')


# Divide and conquer -----------------------------------------------------------


class IDivideAndConquerProblem(ABC):
    @abstractmethod
    def is_simple(self) -> bool: pass

    @abstractmethod
    def trivial_solution(self) -> Solution: pass

    @abstractmethod
    def divide(self) -> Iterable["IDivideAndConquerProblem"]: pass

    @abstractmethod
    def combine(self, solutions: Iterable[Solution]) -> Solution: pass


def div_solve(problem: IDivideAndConquerProblem) -> Solution:
    if problem.is_simple():
        return problem.trivial_solution()
    else:
        subproblems = problem.divide()
        solutions = (div_solve(p) for p in subproblems)
        return problem.combine(solutions)


# Decrease and conquer -----------------------------------------------------------

class IDecreaseAndConquerProblem(ABC):
    @abstractmethod
    def is_simple(self) -> bool: pass

    @abstractmethod
    def trivial_solution(self) -> Solution: pass

    @abstractmethod
    def decrease(self) -> "IDecreaseAndConquerProblem": pass

    def process(self, s: Solution) -> Solution:
        return s


def dec_solve(problem: IDecreaseAndConquerProblem) -> Solution:
    if problem.is_simple():
        return problem.trivial_solution()
    else:
        smallerproblem = problem.decrease()
        return problem.process(dec_solve(smallerproblem))


def tail_dec_solve(problem: IDecreaseAndConquerProblem) -> Solution:
    if problem.is_simple():
        return problem.trivial_solution()
    else:
        return tail_dec_solve(problem.decrease())


def iter_dec_solve(problem: IDecreaseAndConquerProblem) -> Solution:
    while not problem.is_simple():
        problem = problem.decrease()
    return problem.trivial_solution()
