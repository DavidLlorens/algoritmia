"""
Version:  5.0 (31-oct-2023)
          4.1 (29-sep-2022)
          4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2023
@license: GPL3
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterator, Callable
from typing import TypeVar, Generic, Any, final, Optional

from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

TDecision = TypeVar("TDecision")
TExtra = TypeVar("TExtra")

# ACERCA DEL TIPO Solution
# - La implementación por defecto del metodo solution() devuelve la tupla
#   de decisiones: tuple[TDecision, ...]
# - Podemos sobreescribir solution() en la clase hija para devolver otra cosa.
Solution = Any

# ACERCA DEL TIPO State
# - La implementación por defecto del metodo state() de DecisionSequence y de ScoredDecisionSequence
#   devuelve la tupla de decisiones: tuple[TDecision, ...]
# - Podemos sobreescribir state() en la clase hija para devolver otra cosa.
State = Any


# La clase DecisionSequence -------------------------------------------------------

class DecisionSequence(ABC, Generic[TDecision, TExtra]):
    def __init__(self, extra: Optional[TExtra] = None, parent: DecisionSequence = None, decision: TDecision = None):
        self.parent = parent
        self.decision = decision
        self.extra = extra
        self._len = 0 if parent is None else len(parent) + 1

    # --- Métodos abstractos que hay que implementar en las clases hijas ---

    @abstractmethod
    def is_solution(self) -> bool:
        pass

    @abstractmethod
    def successors(self) -> Iterator[DecisionSequence]:
        pass

    # --- Métodos que se pueden sobreescribir en las clases hijas: solution() y state() ---

    # Por defecto se devuelve la tupla de decisiones
    def solution(self) -> Solution:
        return self.decisions()

    # Debe devolver siempre un objeto inmutable
    # Por defecto se devuelve la tupla de decisiones
    def state(self) -> State:
        return self.decisions()

    # -- Métodos finales que NO se pueden sobreescribir en las clases hijas ---

    @final
    def add_decision(self, decision: TDecision, extra: TExtra = None) -> DecisionSequence:
        return self.__class__(extra, self, decision)

    @final
    def decisions(self) -> tuple[TDecision, ...]:  # Es O(n)
        ds = deque()
        p = self
        while p.parent is not None:
            ds.appendleft(p.decision)
            p = p.parent
        return tuple(ds)

    @final
    def __len__(self) -> int:  # len(objeto) devuelve el número de decisiones del objeto
        return self._len


# Esquema para BT básico --------------------------------------------------------------------------

def bt_solutions(ds: DecisionSequence[TDecision, TExtra]) -> Iterator[Solution]:
    if ds.is_solution():
        yield ds.solution()
    for new_ds in ds.successors():
        yield from bt_solutions(new_ds)


#  Esquema para BT con control de visitados --------------------------------------------------------

def bt_vc_solutions(initial_ds: DecisionSequence[TDecision, TExtra]) -> Iterator[Solution]:
    def bt(ds: DecisionSequence) -> Iterator[Solution]:
        if ds.is_solution():
            yield ds.solution()
        for new_ds in ds.successors():
            new_state = new_ds.state()
            if new_state not in seen:
                seen.add(new_state)
                yield from bt(new_ds)

    seen = {initial_ds.state()}  # marcamos initial_ds como visto
    return bt(initial_ds)  # Devuelve un iterador de soluciones


#  Mejor solución  --------------------------------------------------------


Score = int | float
ScoredSolution = tuple[Score, Solution]


def min_solution(solutions: Iterator[Solution],
                 f: Callable[[Solution], Score]) -> Optional[ScoredSolution]:
    return min(((f(sol), sol) for sol in solutions), default=None)


def max_solution(solutions: Iterator[Solution],
                 f: Callable[[Solution], Score]) -> Optional[ScoredSolution]:
    return max(((f(sol), sol) for sol in solutions), default=None)
