"""
Version: 4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2021
@license: GPL3
"""
from abc import ABC, abstractmethod
from typing import *

infinity = float("infinity")

Decision = TypeVar('Decision')
Solution = TypeVar('Solution')
State = TypeVar('State')
Score = TypeVar('Score', int, float)


# Esquema para BT básico --------------------------------------------------------------------------


class DecisionSequence(ABC):
    __slots__ = ("_decisions", "_extra_fields")

    def __init__(self, extra_fields=None, decisions: tuple[Decision, ...] = ()):
        self._decisions = decisions
        self._extra_fields = extra_fields

    @property
    def extra(self):
        return self._extra_fields

    def __len__(self):  # len(objeto) devuelve el número de decisiones del objeto
        return len(self._decisions)

    def add_decision(self, d: Decision, extra_fields=None) -> 'DecisionSequence':
        return self.__class__(extra_fields, self._decisions + (d,))

    def decisions(self) -> tuple[Decision, ...]:
        return self._decisions

    def state(self) -> State:
        # The returned object must be of an inmutable type
        return self._decisions

    def solution(self) -> Solution:
        return self._decisions

    @abstractmethod
    def is_solution(self) -> bool:
        pass

    @abstractmethod
    def successors(self) -> Iterable["DecisionSequence"]:
        pass


def bt_solve(initial_ds: DecisionSequence) -> Iterable[Solution]:
    def bt(ds: DecisionSequence) -> Iterable[Solution]:
        if ds.is_solution():
            yield ds.solution()
        for new_ds in ds.successors():
            yield from bt(new_ds)

    return bt(initial_ds)


#  Esquema para BT con control de visitados --------------------------------------------------------

def bt_vc_solve(initial_ds: DecisionSequence) -> Iterable[Solution]:
    def bt(ds: DecisionSequence) -> Iterable[Solution]:
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

class ScoredDecisionSequence(DecisionSequence):
    @abstractmethod
    def successors(self) -> Iterable["ScoredDecisionSequence"]:
        pass

    @abstractmethod
    def score(self) -> Score:
        # result of applying the objective function to the partial solution
        pass


# Solver de minimización (p.e. para el problema del cambio)
def bt_min_solve(initial_ds: ScoredDecisionSequence) -> Iterable[Solution]:
    def bt(ds: ScoredDecisionSequence) -> Iterable[Solution]:
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
def bt_max_solve(initial_ds: ScoredDecisionSequence) -> Iterable[Solution]:
    def bt(ds: ScoredDecisionSequence) -> Iterable[Solution]:
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
