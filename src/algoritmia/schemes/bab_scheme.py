"""
Version: 5.1 (23-nov-2023)
         5.0 (31-oct-2023)
         4.1 (29-sep-2022)
         4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2023
@license: GPL3
"""
from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterator
from functools import total_ordering
from typing import final, Optional

from algoritmia.datastructures.priorityqueues import MaxHeap, MinHeap
from algoritmia.schemes.bt_scheme import DecisionSequence, TDecision, TExtra, Score, ScoredSolution
from algoritmia.utils import infinity

# ACERCA DEL TIPO ScoredSolution (importado de bt_scheme)
# Las funciones bab_min_solve y bab_max_solve devuelven Optional[ScoredSolution]:
#   - Devuelven None si no hay solución.
#   - Devuelven la tupla (Score, self.solution()) si hay solución.

# ACERCA DEL CÁLCULO EFICIENTE DE LAS COTAS
# Dado que las cotas son inmutables solo deberían calcularse una vez:
# - Los métodos calculate_opt_bound() y calculate_pes_bound() se llaman sólo en el constructor
#   y sus resultados se guardan en los atributos self._opt y self._pes.
# - Los métodos opt() y pes() sólo devuelven el valor de estos atributos.

# La clase BabDecisionSequence -------------------------------------------------------


@total_ordering  # Implementando < y ==, el resto de operadores de comparación se generan automáticamente
class BabDecisionSequence(DecisionSequence[TDecision, TExtra]):
    def __init__(self,  extra: Optional[TExtra] = None, parent: BabDecisionSequence = None, decision: TDecision = None):
        DecisionSequence.__init__(self, extra, parent, decision)
        self._pes = self.calculate_pes_bound()
        self._opt = self.calculate_opt_bound()

    # --- Métodos abstractos ---

    @abstractmethod
    def calculate_opt_bound(self) -> Score:  # Calcula y devuelve la cota optimista
        pass

    @abstractmethod
    def calculate_pes_bound(self) -> Score:  # Calcula y devuelve la cota pesimista
        pass

    # --- Métodos abstractos heredados  ---

    @abstractmethod
    def successors(self) -> Iterator[BabDecisionSequence]:  # Ha cambiado el tipo devuelto
        pass

    # @abstractmethod
    # def is_solution(self) -> bool:
    #     pass

    # --- Métodos heredados que se puede sobreescribir en las clases hijas: solution() y state() ---

    # def solution(self) -> Solution:
    #    return self.decisions()

    # def state(self) -> State:
    #    return self.decisions()

    # -- Métodos finales que NO se pueden sobreescribir en las clases hijas ---

    # Cota optimista. Para las soluciones su valor debe coincidir con la puntuación real
    @final
    def opt(self) -> Score:
        return self._opt

    # Cota pesimista. Para las soluciones su valor debe coincidir con la puntuación real
    @final
    def pes(self) -> Score:
        return self._pes

    # Comparar dos BabDecisionSequence es comparar sus cotas optimistas
    @final
    def __lt__(self, other: BabDecisionSequence) -> bool:
        return self._opt < other._opt

    @final
    def __eq__(self, other: BabDecisionSequence) -> bool:
        return self._opt == other._opt


# Esquemas para BaB --------------------------------------------------------------------------

def bab_min_solve(initial_ds: BabDecisionSequence) -> Optional[ScoredSolution]:
    bps = initial_ds.pes()
    heap = MinHeap([initial_ds])                                    # máx: MaxHeap
    best_seen = {initial_ds.state(): initial_ds.opt()}
    while len(heap) > 0:
        best_ds = heap.extract_opt()
        if best_ds.is_solution():
            return best_ds.opt(), best_ds.solution()
        for new_ds in best_ds.successors():
            if new_ds.opt() <= bps:                                 # máx: >=
                bps = min(bps, new_ds.pes())                        # máx: max
                new_state = new_ds.state()
                if new_ds.opt() < best_seen.get(new_state, infinity):  # máx: >, -inf
                    best_seen[new_state] = new_ds.opt()
                    heap.add(new_ds)


def bab_max_solve(initial_ds: BabDecisionSequence) -> Optional[ScoredSolution]:
    bps = initial_ds.pes()
    heap = MaxHeap([initial_ds])                                     # mín: MinHeap
    best_seen = {initial_ds.state(): initial_ds.opt()}
    while len(heap) > 0:
        best_ds = heap.extract_opt()
        if best_ds.is_solution():
            return best_ds.opt(), best_ds.solution()
        for new_ds in best_ds.successors():
            if new_ds.opt() >= bps:                                  # mín: <=
                bps = max(bps, new_ds.pes())                         # mín: min
                new_state = new_ds.state()
                if new_ds.opt() > best_seen.get(new_state, -infinity):  # mín: <, inf
                    best_seen[new_state] = new_ds.opt()
                    heap.add(new_ds)
