"""
Version: 6.2 (08-jun-2026) - Corrección de tipos para evitar warnings de mypy
         6.1 (12-oct-2025)
         6.0 (11-dic-2024)
         5.2 (01-dic-2023)
         5.1 (23-nov-2023)
         5.0 (31-oct-2023)
         4.1 (29-sep-2022)
         4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2026
@license: GPL3
"""
import operator
from abc import abstractmethod
from typing import final, Callable, cast

from algoritmia.datastructures.priorityqueues import MaxHeap, MinHeap, IPriorityQueue
from algoritmia.schemes.bt_scheme import DecisionSequence, DecisionPath


# --- Tipo Result[D, E, S] ---

type Result[D, E, S: int | float] = tuple[S, BabDecisionSequence[D, E, S]] | None

# Parámetros de tipo:
#   - D: el tipo de una decisión
#   - E: el tipo de la dataclass Extra
#   - S: el tipo de la puntuación (int o float)

# Un objeto de tipo Result[D, E, S] puede tomar los valores:
#   - (score, ds_sol): si hay solución, donde 'ds_sol' es la BabDecisionSequence que lleva
#     a la solución óptima y 'score', su puntuación.
#   - None: si no hay solución.


# --- Acerca del cálculo eficiente de las cotas ---

# Dado que las cotas son inmutables solo deberían calcularse una vez:
# - Los métodos calculate_opt_bound() y calculate_pes_bound() se llaman sólo en el constructor
#   y sus resultados se guardan en los atributos self._opt y self._pes.
# - Los métodos opt() y pes() sólo devuelven el valor de estos atributos.


# La clase BabDecisionSequence -------------------------------------------------------


class BabDecisionSequence[D, E, S: int | float](DecisionSequence[D, E]):
    def __init__(self,
                 extra: E = None,
                 decisions: DecisionPath[D] = (),
                 length: int = 0):
        DecisionSequence[D, E].__init__(self, extra, decisions, length)
        self._pes: S = self.calculate_pes_bound()
        self._opt: S = self.calculate_opt_bound()

    # --- Métodos abstractos nuevos ---

    @abstractmethod
    def calculate_opt_bound(self) -> S:  # Calcula y devuelve la cota optimista
        pass

    @abstractmethod
    def calculate_pes_bound(self) -> S:  # Calcula y devuelve la cota pesimista
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
    def opt(self) -> S:
        return self._opt

    # Cota pesimista. Para las soluciones su valor debe coincidir con la puntuación real
    @final
    def pes(self) -> S:
        return self._pes

    # Comparar dos BabDecisionSequence es comparar sus cotas optimistas
    @final
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BabDecisionSequence):
            return NotImplemented
        other_ds = cast(BabDecisionSequence[D, E, S], other)
        return self._opt < other_ds._opt

    @final
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BabDecisionSequence):
            return NotImplemented
        other_ds = cast(BabDecisionSequence[D, E, S], other)
        return self._opt == other_ds._opt

    @final
    def __le__(self, other: object) -> bool:
        if not isinstance(other, BabDecisionSequence):
            return NotImplemented
        other_ds = cast(BabDecisionSequence[D, E, S], other)
        return self._opt <= other_ds._opt

    @final
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, BabDecisionSequence):
            return NotImplemented
        other_ds = cast(BabDecisionSequence[D, E, S], other)
        return self._opt > other_ds._opt

    @final
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, BabDecisionSequence):
            return NotImplemented
        other_ds = cast(BabDecisionSequence[D, E, S], other)
        return self._opt >= other_ds._opt

    # -- Métodos finales heredados que NO pueden sobreescribirse en las clases hijas ---

    # @final
    # def add_decision(self, decision: D, extra: E = None) -> Self:    # O(1)

    # @final
    # def decisions(self) -> tuple[D, ...]:     # O(n)

    # @final
    # def last_decision(self) -> D:             # O(1)

    # @final
    # def __len__(self) -> int:                         # O(1)

# Esquemas para BaB --------------------------------------------------------------------------


def bab_solve[D, E, S: int | float](better: Callable[[S, S], bool],
                       heap: IPriorityQueue[BabDecisionSequence[D, E, S]],
                       initial_ds: BabDecisionSequence[D, E, S]
                      ) -> Result[D, E, S]:
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


def bab_min_solve[D, E, S: int | float](initial_ds: BabDecisionSequence[D, E, S]) -> Result[D, E, S]:
    return bab_solve(operator.lt, MinHeap[BabDecisionSequence[D, E, S]](), initial_ds)


def bab_max_solve[D, E, S: int | float](initial_ds: BabDecisionSequence[D, E, S]) -> Result[D, E, S]:
    return bab_solve(operator.gt, MaxHeap[BabDecisionSequence[D, E, S]](), initial_ds)