"""
Version: 4.1 (29-sep-2022)
         4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2022
@license: GPL3
"""
from __future__ import annotations

from abc import abstractmethod
from functools import total_ordering
from typing import Optional, Generic, Union, Any

from algoritmia.datastructures.priorityqueues import MaxHeap, MinHeap
from algoritmia.schemes.bt_scheme import DecisionSequence, TDecision

Score = Union[int, float]

# 'bab_max_solve' y 'bab_min_solve' devuelven un Iterator del tipo devuelto por el método 'solution()' de
# la clase 'BoundedDecisionSequence', cuya implementación por defecto devuelve una tupla de dos elementos:
# el Score y una tupla con las decisiones:
# tuple[Score, tuple[TDecision, ...]]
Solution = Any

@total_ordering  # Implementando  < y ==, genera el resto
class BoundedDecisionSequence(Generic[TDecision],
                              DecisionSequence[TDecision]):
    __slots__ = ("_pes", "_opt")

    def __init__(self, extra_fields=None, decisions: tuple[TDecision, ...] = ()):
        super().__init__(extra_fields, decisions)
        self._pes: Score = self.calculate_pes_bound()
        self._opt: Score = self.calculate_opt_bound()

    # Nota: Para no repetir cálculos, y dado que son inmutables, las cotas se
    # deberían calcular sólo una vez. Los métodos calculate_opt_bound u calculate_pes_bound
    # se calculan solo una vez y se guarda en self._opt y self._pes.
    # - Los métodos opt() y pes() sólo devuelven el valor de estos atributos.
    @abstractmethod
    def calculate_opt_bound(self) -> Score:
        pass

    @abstractmethod
    def calculate_pes_bound(self) -> Score:
        pass

    # Optimistic bound. Must be equal to score() for full solutions
    def opt(self) -> Score:
        return self._opt

    # Pessimistic bound. Must be equal to score() for full solutions
    def pes(self) -> Score:
        return self._pes

    def solution(self) -> Solution:
        return self._pes, self.decisions()

    # Comparar dos BabDecisionSequence es comparar sus cotas optimistas
    def __lt__(self, other: BoundedDecisionSequence[TDecision]) -> bool:
        return self._opt < other._opt

    def __eq__(self, other: BoundedDecisionSequence[TDecision]) -> bool:
        return self._opt == other._opt



def bab_max_solve(initial_ds: BoundedDecisionSequence[TDecision]) -> Optional[Solution]:
    heap = MaxHeap()
    heap.add(initial_ds)
    bps = initial_ds.pes()
    while len(heap) > 0:
        best_ps = heap.extract_opt()
        if best_ps.is_solution():
            return best_ps.solution()
        for new_ps in best_ps.successors():
            bps = max(bps, new_ps.pes())
            if new_ps.opt() >= bps:
                heap.add(new_ps)


def bab_min_solve(initial_ds: BoundedDecisionSequence[TDecision]) -> Optional[Solution]:
    heap = MinHeap()
    heap.add(initial_ds)
    bps = initial_ds.pes()
    while len(heap) > 0:
        best_ps = heap.extract_opt()
        if best_ps.is_solution():
            return best_ps.solution()
        for new_ps in best_ps.successors():
            bps = min(bps, new_ps.pes())
            if new_ps.opt() <= bps:
                heap.add(new_ps)
