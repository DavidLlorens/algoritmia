"""
Version:  5.8 (08-jun-2026) - Corrección de tipos para evitar warnings de mypy
          5.7 (11-nov-2025) - DecisionSequence ahora es Iterable.
          5.6 (14-oct-2025) - Acortados nombres parámetros tipo. Quitado tipo ScoredSolution.
          5.5 (12-oct-2025) - Corregido bug en min_solution y max_solution
          5.4 (11-oct-2025)
          5.3 (09-ene-2024)
          5.2 (01-dic-2023)
          5.0 (31-oct-2023)
          4.1 (29-sep-2022)
          4.0 (23-oct-2021)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2026
@license: GPL3
"""
from abc import ABC, abstractmethod
from collections.abc import Iterator, Reversible, Callable, Sized
from typing import Any, final, Self

# Tipos  --------------------------------------------------------------------------

# El tipo para guardar las secuencias de decisiones (self._decisions) como caminos en el árbol
# de todas las posibles secuencias. Dos secuencias que compartan un prefijo comparten
# la memoria correspondiente a ese prefijo.
type DecisionPath[D] = tuple[D, DecisionPath[D]] | tuple[()]

# D (tipo de una decisión) y State deben ser tipos inmutables.

# ACERCA DEL TIPO State
# La implementación por defecto devuelve self._decisions (la secuencia de decisiones)
# Podemos sobreescribir state() en la clase hija para devolver otra cosa.
type State = Any

# La clase DecisionSequence -------------------------------------------------------

class DecisionSequence[D, E](ABC, Sized, Reversible[D]):
    def __init__(self,
                 extra: E = None,
                 decisions: DecisionPath[D] = (),
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
    # Por defecto se devuelve el atributo self._decisions
    def state(self) -> State:
        return self._decisions

    # -- Métodos finales que NO se pueden sobreescribir en las clases hijas ---

    @final
    def add_decision(self, decision: D, extra: E = None) -> Self:
        return self.__class__(extra, (decision, self._decisions), self._len + 1)

    @final
    def last_decision(self) -> D:  # Es O(1)
        if len(self._decisions) > 0:
            return self._decisions[0]
        raise RuntimeError(f'last_decision() used on an empty {self.__class__.__name__} object')

    @final
    def decisions(self) -> tuple[D, ...]:  # Es O(n)
        return tuple(iter(self))

    @final
    def __len__(self) -> int:  # len(objeto) devuelve el número de decisiones del objeto
        return self._len

    @final
    def __iter__(self) -> Iterator[D]: 
        return reversed(list(reversed(self)))  # Iterador sobre las decisiones en orden normal

    @final
    def __reversed__(self) -> Iterator[D]:  # Iterador sobre las decisiones en orden inverso
        p: DecisionPath[D] = self._decisions
        while True:
            match p:
                case ():
                    break
                case (head, tail):
                    p = tail
                    yield head



# Esquema para BT básico --------------------------------------------------------------------------

# Un generador de soluciones sin control de visitados. Una solución es una DecisionSequence
# para la que el método is_solution() devuelve True

def bt_solutions[D, E](ds: DecisionSequence[D, E]) -> Iterator[DecisionSequence[D, E]]:
    if ds.is_solution():
        yield ds
    for new_ds in ds.successors():
        yield from bt_solutions(new_ds)


#  Esquema para BT con control de visitados --------------------------------------------------------

# Un generador de soluciones con control de visitados. Una solución es una DecisionSequence
# para la que el método is_solution() devuelve True

def bt_vc_solutions[D, E](initial_ds: DecisionSequence[D, E]) -> Iterator[DecisionSequence[D, E]]:
    def bt(ds: DecisionSequence[D, E]) -> Iterator[DecisionSequence[D, E]]:
        if ds.is_solution():
            yield ds
        for new_ds in ds.successors():
            new_state = new_ds.state()
            if new_state not in seen:
                seen.add(new_state)
                yield from bt(new_ds)

    seen = {initial_ds.state()}  # Marca initial_ds como visto
    return bt(initial_ds)        # Devuelve un iterador de soluciones


#  Encontrar la mejor solución --------------------------------------------------------

# --- Tipo Result[Sol, S] ---

type Result[Sco, Sol] = tuple[Sco, Sol] | None

# Parámetros de tipo:
#   - Sol: el tipo de una solución
#   - S: el tipo de la puntuación (int o float)

# Un objeto de tipo Result[Sol, S] puede tomar los valores:
#   - (score, solution), si hay solución.
#   - None, si no hay solución.

# --- Funciones min_solution y max_solution ---

def min_solution[Sco: int | float, Sol](solutions: Iterator[Sol],
                         f: Callable[[Sol], Sco]) -> Result[Sco, Sol]:
    best: Result[Sco, Sol] = None
    for sol in solutions:
        score = f(sol)
        if best is None or score < best[0]:
            best = score, sol
    return best


def max_solution[Sco: int | float, Sol](solutions: Iterator[Sol],
                         f: Callable[[Sol], Sco]) -> Result[Sco, Sol]:
    best: Result[Sco, Sol] = None
    for sol in solutions:
        score = f(sol)
        if best is None or score > best[0]:
            best = score, sol
    return best
