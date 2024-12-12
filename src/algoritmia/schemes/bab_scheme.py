"""
Version: 6.0 (11-dic-2024)
         5.2 (01-dic-2023)
         5.1 (23-nov-2023)
         5.0 (31-oct-2023)
         4.1 (29-sep-2022)
         4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2023
@license: GPL3
"""
import operator
from abc import abstractmethod
from functools import total_ordering
from typing import final, Self, Callable

from algoritmia.datastructures.priorityqueues import MaxHeap, MinHeap, IPriorityQueue
from algoritmia.schemes.bt_scheme import DecisionSequence, DecisionPath


# ACERCA DEL TIPO ScoredSolution (importado de bt_scheme)
# Las funciones bab_min_solve y bab_max_solve devuelven Optional[ScoredSolution]:
#   - Devuelven 'None' si no hay solución.
#   - Devuelven la tupla '(score, ds_sol)' si hay solución: donde 'ds_sol' es la
#     BabDecisionSequence que lleva a la solución óptima y 'score', su puntuación.

# ACERCA DEL CÁLCULO EFICIENTE DE LAS COTAS
# Dado que las cotas son inmutables solo deberían calcularse una vez:
# - Los métodos calculate_opt_bound() y calculate_pes_bound() se llaman sólo en el constructor
#   y sus resultados se guardan en los atributos self._opt y self._pes.
# - Los métodos opt() y pes() sólo devuelven el valor de estos atributos.

# La clase BabDecisionSequence -------------------------------------------------------


@total_ordering  # Implementando < y ==, el resto de operadores de comparación se generan automáticamente
class BabDecisionSequence[TDecision, TExtra, TScore](DecisionSequence[TDecision, TExtra]):
    def __init__(self,
                 extra: TExtra | None = None,
                 decisions: DecisionPath[TDecision] = (),
                 length: int = 0):
        DecisionSequence.__init__(self, extra, decisions, length)
        self._pes = self.calculate_pes_bound()
        self._opt = self.calculate_opt_bound()

    # --- Métodos abstractos nuevos ---

    @abstractmethod
    def calculate_opt_bound(self) -> TScore:  # Calcula y devuelve la cota optimista
        pass

    @abstractmethod
    def calculate_pes_bound(self) -> TScore:  # Calcula y devuelve la cota pesimista
        pass

    # --- Métodos abstractos heredados  ---

    # @abstractmethod
    # def successors(self) -> Iterator[Self]:
    #     pass

    # @abstractmethod
    # def is_solution(self) -> bool:
    #     pass

    # --- Método heredado que puede sobreescribirse en las clases hijas ---

    # def state(self) -> State:     # La implementación por defecto es O(n)

    # -- Métodos finales que NO se pueden sobreescribir en las clases hijas ---

    # Cota optimista. Para las soluciones su valor debe coincidir con la puntuación real
    @final
    def opt(self) -> TScore:
        return self._opt

    # Cota pesimista. Para las soluciones su valor debe coincidir con la puntuación real
    @final
    def pes(self) -> TScore:
        return self._pes

    # Comparar dos BabDecisionSequence es comparar sus cotas optimistas
    @final
    def __lt__(self, other: Self) -> bool:
        return self._opt < other._opt

    @final
    def __eq__(self, other: Self) -> bool:
        return self._opt == other._opt

    # -- Métodos finales heredados que NO pueden sobreescribirse en las clases hijas ---

    # @final
    # def add_decision(self, decision: TDecision, extra: TExtra = None) -> Self:    # O(1)

    # @final
    # def decisions(self) -> tuple[TDecision, ...]:     # O(n)

    # @final
    # def last_decision(self) -> TDecision:             # O(1)

    # @final
    # def __len__(self) -> int:                         # O(1)

# Esquemas para BaB --------------------------------------------------------------------------

def bab_solve[TDecision, TExtra, TScore](better: Callable[[TScore, TScore], bool],
                                         heap: IPriorityQueue[TScore],
                                         initial_ds: BabDecisionSequence[TDecision, TExtra, TScore]
                                         ) -> tuple[TScore, BabDecisionSequence[TDecision, TExtra, TScore]] | None:
    bps = initial_ds.pes()
    heap.add(initial_ds)
    best_seen = {initial_ds.state(): initial_ds.opt()}
    while len(heap) > 0:
        best_ds = heap.extract_opt()
        if best_ds.is_solution():
            return best_ds.opt(), best_ds
        for new_ds in best_ds.successors():
            new_opt = new_ds.opt()
            if not better(bps, new_opt):
                if better(new_ds.pes(), bps):
                    bps = new_ds.pes()
                new_state = new_ds.state()
                bs = best_seen.get(new_state, None)
                if bs is None or better(new_opt, bs):
                    best_seen[new_state] = new_opt
                    heap.add(new_ds)


def bab_min_solve[TDecision, TExtra, TScore](initial_ds: BabDecisionSequence[TDecision, TExtra, TScore])\
        -> tuple[TScore, BabDecisionSequence[TDecision, TExtra, TScore]] | None:
    return bab_solve(operator.lt, MinHeap(), initial_ds)


def bab_max_solve[TDecision, TExtra, TScore](initial_ds: BabDecisionSequence[TDecision, TExtra, TScore])\
        -> tuple[TScore, BabDecisionSequence[TDecision, TExtra, TScore]] | None:
    return bab_solve(operator.gt, MaxHeap(), initial_ds)