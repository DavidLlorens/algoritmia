"""
Version:  4.1 (29-sep-2022)
          4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2022
@license: GPL3
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TypeVar, Generic, Any, Union

infinity = float("infinity")

TDecision = TypeVar('TDecision', contravariant=True)
Solution = Any
State = Any


# Esquema para BT básico --------------------------------------------------------------------------

class DecisionSequence(ABC, Generic[TDecision]):
    __slots__ = ("_decisions", "_extra_fields")

    def __init__(self, extra_fields=None, decisions: tuple[TDecision, ...] = ()):
        self._decisions = decisions
        self._extra_fields: Any = extra_fields

    @property
    def extra(self) -> Any:
        return self._extra_fields

    def __len__(self) -> int:  # len(objeto) devuelve el número de decisiones del objeto
        return len(self._decisions)

    def add_decision(self, d: TDecision, extra_fields=None) -> DecisionSequence:
        return self.__class__(extra_fields, self._decisions + (d,))

    def decisions(self) -> tuple[TDecision, ...]:
        return self._decisions

    def solution(self) -> Solution:
        return self._decisions

    @abstractmethod
    def is_solution(self) -> bool:
        pass

    @abstractmethod
    def successors(self) -> Iterator[DecisionSequence]:
        pass


def bt_solve(initial_ds: DecisionSequence[TDecision]) -> Iterator[Solution]:
    def bt(ds: DecisionSequence[TDecision]) -> Iterator[Solution]:
        if ds.is_solution():
            yield ds.solution()
        for new_ds in ds.successors():
            yield from bt(new_ds)

    return bt(initial_ds)


#  Esquema para BT con control de visitados --------------------------------------------------------

class StateDecisionSequence(DecisionSequence[TDecision]):
    @abstractmethod
    def successors(self) -> Iterator[StateDecisionSequence]:
        pass

    def state(self) -> State:
        # The returned object must be of an inmutable type
        return self._decisions


def bt_vc_solve(initial_ds: StateDecisionSequence[TDecision]) -> Iterator[Solution]:
    def bt(ds: StateDecisionSequence[TDecision]) -> Iterator[Solution]:
        seen.add(ds.state())  # El método state debe devolver un objeto inmutable
        if ds.is_solution():
            yield ds.solution()
        for new_ds in ds.successors():
            state = new_ds.state()
            if state not in seen:
                yield from bt(new_ds)

    seen = set()
    return bt(initial_ds)


# Esquema para BT para optimización ----------------------------------------------------------------

class ScoredDecisionSequence(StateDecisionSequence[TDecision]):
    @abstractmethod
    def successors(self) -> Iterator[ScoredDecisionSequence]:
        pass

    @abstractmethod
    def score(self) -> Union[int, float]:
        # result of applying the objective function to the partial solution
        pass

    # Sobrescribimos 'solution()'
    def solution(self) -> Solution:
        return self.score(), self.decisions()


# Solver de minimización (p.e. para el problema del cambio)
def bt_min_solve(initial_ds: ScoredDecisionSequence[TDecision]) -> Iterator[Solution]:
    def bt(ds: ScoredDecisionSequence[TDecision]) -> Iterator[Solution]:
        nonlocal bs
        ds_score = ds.score()
        best_seen[ds.state()] = ds_score
        if ds.is_solution() and ds_score < bs:  # sólo muestra una solución si mejora la última mostrada
            bs = ds_score
            yield ds.solution()
        for new_ds in ds.successors():
            new_state = new_ds.state()
            if new_ds.score() < best_seen.get(new_state, infinity):
                yield from bt(new_ds)

    best_seen = {}
    bs = infinity  # score of the best solution found
    return bt(initial_ds)


# Solver de maximización (p.e. para el problema de la mochila)
def bt_max_solve(initial_ds: ScoredDecisionSequence[TDecision]) -> Iterator[Solution]:
    def bt(ds: ScoredDecisionSequence[TDecision]) -> Iterator[Solution]:
        nonlocal bs
        ds_score = ds.score()
        best_seen[ds.state()] = ds_score
        if ds.is_solution() and ds_score > bs:  # sólo muestra una solución si mejora la última mostrada
            bs = ds_score
            yield ds.solution()
        for new_ds in ds.successors():
            new_state = new_ds.state()
            if new_ds.score() > best_seen.get(new_state, -infinity):
                yield from bt(new_ds)

    best_seen = {}
    bs = -infinity
    return bt(initial_ds)
