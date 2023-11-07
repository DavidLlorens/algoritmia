"""
Version: 5.0 (31-oct-2023)
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
from typing import TypeVar, Any, final, Optional

from algoritmia.datastructures.priorityqueues import MaxHeap, MinHeap
from algoritmia.schemes.bt_scheme import DecisionSequence
from algoritmia.utils import infinity

# Tipos  --------------------------------------------------------------------------

TDecision = TypeVar("TDecision")
TExtra = TypeVar("TExtra")

# ACERCA DEL TIPO Score
# - Es el tipo que devuelven las cotas
Score = int | float

# ACERCA DEL TIPO Solution
# - La implementación por defecto del metodo solution() de BabDecisionSequence devuelve
#   el f y la tupla de decisiones: tuple[Score, tuple[TDecision, ...]]
# - Podemos sobreescribir solution() en la clase hija para devolver otra cosa.
Solution = Any

# ACERCA DEL TIPO State
# - La implementación por defecto del metodo state() de BabDecisionSequence (por herencia de
#   DecisionSequence) devuelve la tupla de decisiones: tuple[TDecision, ...]
# - Podemos sobreescribir state() en la clase hija para devolver otra cosa.
State = Any


# ACERCA DEL CÁLCULO EFICIENTE DE LAS COTAS
# Dado que las cotas son inmutables sólo deberían calcularse una vez:
# - Los métodos calculate_opt_bound() y calculate_pes_bound() se llaman sólo en el constructor)
#   y sus resultados se guardan en los atributos self._opt y self._pes.
# - Los métodos opt() y pes() sólo devuelven el valor de estos atributos.


# La clase BabDecisionSequence -------------------------------------------------------


@total_ordering  # Implementando < y ==, el resto de operadores de comparación se generan automáticamente
class BabDecisionSequence(DecisionSequence[TDecision, TExtra]):
    def __init__(self,  extra: Optional[TExtra] = None, parent: BabDecisionSequence = None, decision: TDecision = None):
        DecisionSequence.__init__(self, extra, parent, decision)
        self._pes = self.calculate_pes_bound()
        self._opt = self.calculate_opt_bound()

    # --- Métodos abstractos que hay que implementar en las clases hijas ---

    @abstractmethod
    def f(self) -> Score:  # Puntuación de la función objetivo
        pass

    @abstractmethod
    def calculate_opt_bound(self) -> Score:
        pass

    @abstractmethod
    def calculate_pes_bound(self) -> Score:
        pass

    @abstractmethod
    def successors(self) -> Iterator[BabDecisionSequence]:  # Cambia el tipo devuelto
        pass

    # --- Métodos que se puede sobreescribir en las clases hijas: solution() (y state(), que se hereda) ---

    # Por defecto se devuelve una tupla con el Score y las decisiones
    def solution(self) -> Solution:
        return self.f(), self.decisions()

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

def bab_min_solve(initial_ds: BabDecisionSequence) -> Optional[Solution]:
    best_solution, best_f = None, infinity                            # máx: -inf
    bps = initial_ds.pes()
    heap = MinHeap([initial_ds])                                      # máx: MaxHeap()
    best_seen = {initial_ds.state(): initial_ds.f()}
    while len(heap) > 0:
        top_ds = heap.extract_opt()
        if best_f <= top_ds.opt():                                    # máx: >=
            return best_solution
        if top_ds.is_solution():
            best_f = top_ds.f()
            best_solution = top_ds.solution()
        for new_ds in top_ds.successors():
            if new_ds.opt() <= bps:                                  # máx: >=
                bps = min(bps, new_ds.pes())                         # máx: max
                new_state = new_ds.state()
                if new_ds.f() < best_seen.get(new_state, infinity):  # máx: >, -infintiy
                    best_seen[new_state] = new_ds.f()
                    heap.add(new_ds)
    return best_solution


def bab_max_solve(initial_ds: BabDecisionSequence) -> Optional[Solution]:
    best_solution, best_f = None, -infinity                           # mín: inf
    bps = initial_ds.pes()
    heap = MaxHeap([initial_ds])                                      # mín: MinHeap()
    best_seen = {initial_ds.state(): initial_ds.f()}
    while len(heap) > 0:
        top_ds = heap.extract_opt()
        if best_f >= top_ds.opt():                                    # mín: <=
            return best_solution
        if top_ds.is_solution():
            best_f = top_ds.f()
            best_solution = top_ds.solution()
        for new_ds in top_ds.successors():
            if new_ds.opt() >= bps:                                   # mín: <=
                bps = max(bps, new_ds.pes())                          # mín: min
                new_state = new_ds.state()
                if new_ds.f() > best_seen.get(new_state, -infinity):  # mín: <, infintiy
                    best_seen[new_state] = new_ds.f()
                    heap.add(new_ds)
    return best_solution
