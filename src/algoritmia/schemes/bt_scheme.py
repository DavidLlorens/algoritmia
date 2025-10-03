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
from typing import Any, final, Self

# Tipos  --------------------------------------------------------------------------

# El tipo para guardar las secuencias de decisiones (self._decisions) como caminos en el árbol
# de todas las posibles secuencias. Dos secuencias que compartan un prefijo comparten
# la memoria correspondiente a ese prefijo.
type DecisionPath[TDecision] = tuple[TDecision, DecisionPath[TDecision]] | tuple[()]

# ACERCA DEL TIPO State
# La implementación por defecto devuelve self._decisions.
# Podemos sobreescribir state() en la clase hija para devolver otra cosa.
type State = Any

# La clase DecisionSequence -------------------------------------------------------

class DecisionSequence[TDecision, TExtra](ABC, Sized):
    def __init__(self,
                 extra: TExtra | None = None,
                 decisions: DecisionPath[TDecision] = (),
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

    # --- Método que se puede sobreescribir en las clases hijas: state() ---

    # Debe devolver siempre un objeto inmutable
    # Por defecto se devuelve el contenido de _decisions
    def state(self) -> State:
        return self._decisions

    # -- Métodos finales que NO se pueden sobreescribir en las clases hijas ---

    @final
    def add_decision(self, decision: TDecision, extra: TExtra = None) -> Self:
        return self.__class__(extra, (decision, self._decisions), self._len + 1)

    @final
    def last_decision(self) -> TDecision:  # Es O(1)
        if len(self._decisions) > 0:
            return self._decisions[0]
        raise RuntimeError(f'last_decision() used on an empty {self.__class__.__name__} object')

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

type Result[TScore, TSolution] = tuple[TScore, TSolution] | None  # None si no hay solución

def min_solution[TSolution, TScore](solutions: Iterator[TSolution],
                                    f: Callable[[TSolution], TScore]) -> Result[TScore, TSolution]:
    return min(((f(sol), sol) for sol in solutions), default=None)


def max_solution[TSolution, TScore](solutions: Iterator[TSolution],
                                    f: Callable[[TSolution], TScore]) -> Result[TScore, TSolution]:
    return max(((f(sol), sol) for sol in solutions), default=None)
