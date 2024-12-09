"""
Version:  5.3 (09-ene-2024)
          5.2 (01-dic-2023)
          5.0 (31-oct-2023)
          4.1 (29-sep-2022)
          4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2024
@license: GPL3
"""
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterator, Callable, Sized
from typing import Any, final, Optional, Self

# Tipos  --------------------------------------------------------------------------

# ACERCA DEL TIPO State
# La implementación por defecto devuelve la tupla de decisiones.
# Podemos sobreescribir state() en la clase hija para devolver otra cosa.
type State = Any

# El tipo para guardar las secuencias de decisiones en forma de árbol para
# ahorrar espacio. Cada nodo es una tupla con la decisión y el padre. La raíz
# tiene la tupla vacía.
type DecisionTree[TDecision] = tuple[()] | tuple[TDecision, DecisionTree[TDecision]]

# La clase DecisionSequence -------------------------------------------------------

class DecisionSequence[TDecision, TExtra](ABC, Sized):
    def __init__(self,
                 extra: Optional[TExtra] = None,
                 decisions: DecisionTree[TDecision] = (),
                 length: int = 0):
        self.extra = extra
        self._decisions = decisions
        self._len = length

    # --- Métodos abstractos que hay que implementar en las clases hijas ---

    @abstractmethod
    def is_solution(self) -> bool:
        pass

    @abstractmethod
    def successors(self) -> Iterator[Self]:
        pass

    # --- Métodos que se pueden sobreescribir en las clases hijas: solution() y state() ---

    # Debe devolver siempre un objeto inmutable
    # Por defecto se devuelve la tupla de decisiones
    def state(self) -> State:
        return self.decisions()

    # -- Métodos finales que NO se pueden sobreescribir en las clases hijas ---

    @final
    def add_decision(self, decision: TDecision, extra: TExtra = None) -> Self:
        return self.__class__(extra, (decision, self._decisions), self._len + 1)

    @final
    def decisions(self) -> tuple[TDecision, ...]:  # Es O(n)
        ds = deque()
        p = self._decisions
        while p != ():
            ds.appendleft(p[0])
            p = p[1]
        return tuple(ds)

    @final
    def __len__(self) -> int:  # len(objeto) devuelve el número de decisiones del objeto
        return self._len


# Esquema para BT básico --------------------------------------------------------------------------

def bt_solutions[TDecision, TExtra](ds: DecisionSequence[TDecision, TExtra])\
        -> Iterator[DecisionSequence[TDecision, TExtra]]:
    if ds.is_solution():
        yield ds
    for new_ds in ds.successors():
        yield from bt_solutions(new_ds)


#  Esquema para BT con control de visitados --------------------------------------------------------

def bt_vc_solutions[TDecision, TExtra](initial_ds: DecisionSequence[TDecision, TExtra])\
        -> Iterator[DecisionSequence[TDecision, TExtra]]:
    def bt(ds: DecisionSequence[TDecision, TExtra]) -> Iterator[DecisionSequence[TDecision, TExtra]]:
        if ds.is_solution():
            yield ds
        for new_ds in ds.successors():
            new_state = new_ds.state()
            if new_state not in seen:
                seen.add(new_state)
                yield from bt(new_ds)

    seen = {initial_ds.state()}  # marcamos initial_ds como visto
    return bt(initial_ds)  # Devuelve un iterador de soluciones


#  Mejor solución --------------------------------------------------------


def min_solution[TSolution, TScore](solutions: Iterator[TSolution],
                                    f: Callable[[TSolution], TScore]) -> Optional[tuple[TScore, TSolution]]:
    return min(((f(sol), sol) for sol in solutions), default=None)


def max_solution[TSolution, TScore](solutions: Iterator[TSolution],
                                    f: Callable[[TSolution], TScore]) -> Optional[tuple[TScore, TSolution]]:
    return max(((f(sol), sol) for sol in solutions), default=None)
