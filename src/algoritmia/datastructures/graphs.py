import sys
from abc import ABC, abstractmethod
from typing import *

Vertex = TypeVar("Vertex")
Edge = tuple[Vertex, Vertex]
Weight = Union[int, float]


# UndirectedGraph, Digraph -----------------------------------------------------


# Abstract class (no instances)
class IGraph(ABC, Generic[Vertex]):
    @abstractmethod
    def is_directed(self) -> bool:
        pass

    def __init__(self, V: Iterable[Vertex] = None, E: Iterable[Edge] = ()):
        self._e: list[Edge] = list(E)
        if V is None:
            self._v: set[Vertex] = set(v for e in self._e for v in e)
        else:
            self._v: set[Vertex] = set(V)

        self._s: dict[Vertex, set[Vertex]] = dict((v, set()) for v in self._v)
        self._p: dict[Vertex, set[Vertex]] = dict((v, set()) for v in self._v) if self.is_directed() else self._s

        to_delete = []
        # Crea los diccionarioos self._s y self._p
        for (u, v) in self._e:
            if u == v:
                sys.stderr.write(f"WARNING: Discarted edge from a vertex to itself {(u, u)}\n")
                continue

            if u not in self._v:
                raise TypeError(f"Vertex {u} from edge {(u, v)} not in vertex set")
            if v not in self._v:
                raise TypeError(f"Vertex {v} from edge {(u, v)} not in vertex set")

            if v in self._s[u]:
                sys.stderr.write(f"WARNING: Discarted repeated edge from {u} to {v}\n")
                to_delete.append((u, v))
            else:
                self._s[u].add(v)
                self._p[v].add(u)

        for e in to_delete:
            self._e.remove(e)

    def succs(self, v: Vertex):
        return self._s[v]

    def preds(self, v: Vertex):
        return self._p[v]

    def out_degree(self, u: Vertex) -> int:
        return len(self._s[u])

    def in_degree(self, v: Vertex) -> int:
        return len(self._p[v])

    @property
    def V(self) -> set[Vertex]:
        return self._v

    @property
    def E(self) -> list[Edge]:
        return self._e

    def add_vertex(self, v: Vertex):
        if v in self._v: return
        if v in self._s: raise Exception('Impossible 1')
        if v in self._p: raise Exception('Impossible 2')
        self._v.add(v)
        self._s[v] = set()
        self._p[v] = set()

    def remove_vertex(self, v: Vertex):
        if v not in self._v: return
        if v not in self._s: raise Exception('Impossible 3')
        if v not in self._p: raise Exception('Impossible 4')
        self._v.remove(v)

        for suc in self._s[v]:
            self._p[suc].remove(v)
        del self._s[v]

        e = [(u, w) for (u, w) in self._e if u != v and w != v]
        self._e = e

    def add_edge(self, e: Edge):
        u, v = e
        self.add_vertex(u)
        self.add_vertex(v)

        self._e.append(e)

        self._s[u].add(v)
        self._p[v].add(u)

    def remove_edge(self, e: Edge):
        u, v = e
        if u in self._s: self._s[u].discard(v)
        if v in self._p: self._p[v].discard(u)
        if e in self._e: self._e.remove(e)
        if not self.is_directed() and (v, u) in self._e:
            self._e.remove((v, u))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(V={list(self.V)}, E={list(self.E)})"


class UndirectedGraph(IGraph[Vertex]):
    def is_directed(self) -> bool:
        return False


class Digraph(IGraph[Vertex]):
    def is_directed(self) -> bool:
        return True


# WeightingFunction -----------------------------------------------------------------


class WeightingFunction(Generic[Vertex], dict[Edge, Weight], Callable[[Vertex, Vertex], Weight]):
    def __init__(self, data: Union[Iterable[tuple[Edge, Weight]], dict[Edge, Weight]], symmetrical: bool = False):
        super().__init__(data)
        self.symmetrical = symmetrical
        to_delete = []
        for (u, v) in self.keys():
            if u == v:
                sys.stderr.write(
                    f"WARNING - WeightingFunction: Edge from a vertex to itself {(u, u)} with weight {self[u, u]}.\n")
            elif symmetrical and (v, u) in self:
                if self[u, v] != self[v, u]:
                    raise ValueError("{!r} is different from {!r}".format((u, v), (v, u)))
                sys.stderr.write(
                    f"WARNING - WeightingFunction: simetrical with repeated edge: {(u, v)} and {(v, u)}. Discarted {(v, u)}.\n")
                to_delete.append((v, u))  # dejar solo una arista en grafos no dirigidos
        for (v, u) in to_delete:
            del self[v, u]

    def __call__(self, u: Union[Vertex, Edge], v: Optional[Vertex] = None) -> Weight:
        if v is None:
            u, v = u
        # if u == v:
        #    return 0
        if (u, v) in self:
            return self[u, v]
        elif self.symmetrical:
            if (v, u) in self:
                return self[v, u]
            raise KeyError(repr((u, v)) + " nor " + repr((v, u)))
        raise KeyError(repr((u, v)))


if __name__ == '__main__':
    g = Digraph[int](E=[(1, 2)])
    print(g)
    print(isinstance(g, IGraph))
    print(isinstance(g, Digraph))
    print(isinstance(g, UndirectedGraph))
