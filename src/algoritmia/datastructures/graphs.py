import sys
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import Generic, TypeVar, Optional, Union

TVertex = TypeVar("TVertex")        # Generic Vertex
TEdge = tuple[TVertex, TVertex]     # Generic Edge
Weight = Union[int, float]

# Crea grafos con las siguientes características:
# 1. Una arista como máximo entre vértices:
#    - Si el grafo es dirigido, (u,v) y (v,u) se consideran aristas distintas.
#    - Si el grafo es no dirigido, (u,v) y (v,u) se consideran la misma arista y solo se almacena la primera
#      en la lista de aristas.
# 2. Se descartan las auto aristas (v, v)

# TODO: Pasar el atributo self._e de list[TEdge] a set[TEdge]. Ventajas:
#   - remove_edge()   podría implementarse O(1)*   -  Ahora es O(|E|)
#   - remove_vertex() podría implementarse O(|V|)  -  Ahora es O(|V| + |E|)

# UndirectedGraph, Digraph -----------------------------------------------------


# Abstract class (no instances)
class IGraph(ABC, Generic[TVertex]):
    @abstractmethod
    def is_directed(self) -> bool:
        pass

    @property
    def V(self) -> set[TVertex]:
        return self._v

    @property
    def E(self) -> list[TEdge]:
        return self._e

    # O(|V| + |E|)
    def __init__(self, V: Optional[Iterable[TVertex]] = None, E: Iterable[TEdge] = ()):
        # Crea el conjunto de vértices self._v
        if V is None:
            self._v: set[TVertex] = set(v for e in iter(E) for v in e)
        else:
            self._v: set[TVertex] = set(V)

        # Crea la lista de aristas self._e y los diccionarios self._s y self._p
        self._e: list[TEdge] = []
        self._s: dict[TVertex, set[TVertex]] = dict((v, set()) for v in self._v)
        self._p: dict[TVertex, set[TVertex]] = dict((v, set()) for v in self._v) if self.is_directed() else self._s
        for e in iter(E):
            u, v = e
            if u not in self._v:
                raise TypeError(f"{self.__class__.__name__} - Vertex {u} from edge {e} is not in the vertex set")
            if v not in self._v:
                raise TypeError(f"{self.__class__.__name__} - Vertex {v} from edge {e} is not in the vertex set")
            if u == v:
                sys.stderr.write(f"{self.__class__.__name__} - WARNING: Discarded auto edge {e}\n")
                continue
            if v in self._s[u]:
                sys.stderr.write(f"{self.__class__.__name__} - WARNING: Discarded repeated edge {e}\n")
                continue

            self._s[u].add(v)
            self._p[v].add(u)
            self._e.append(e)

    # O(1)*
    def succs(self, v: TVertex) -> set[TVertex]:
        return self._s[v]

    # O(1)*
    def preds(self, v: TVertex) -> set[TVertex]:
        return self._p[v]

    # O(1)*
    def out_degree(self, u: TVertex) -> int:
        return len(self._s[u])

    # O(1)*
    def in_degree(self, v: TVertex) -> int:
        return len(self._p[v])

    # O(1)*
    def add_vertex(self, v: TVertex):
        if v in self._v: return
        if v in self._s: raise Exception('Impossible 1')
        if v in self._p: raise Exception('Impossible 2')
        self._v.add(v)
        self._s[v] = set()
        self._p[v] = set()

    # O(|V| + |E|)
    def remove_vertex(self, v: TVertex):
        if v not in self._v: return
        if v not in self._s: raise Exception('Impossible 3')
        if v not in self._p: raise Exception('Impossible 4')
        self._v.remove(v)

        for suc in self._s[v]:
            self._p[suc].remove(v)  # O(1)*, |V| veces: O(|V|)
        del self._s[v]
        if self.is_directed():
            for pred in self._p[v]:
                self._s[pred].remove(v)  # O(1)*, |V| veces: O(|V|)
            del self._p[v]

        edges = [(u, w) for (u, w) in self._e if u != v and w != v]  # O(|E|)
        self._e = edges

    # O(1)*
    def add_edge(self, e: TEdge):
        u, v = e
        self.add_vertex(u)
        self.add_vertex(v)

        self._e.append(e)

        self._s[u].add(v)
        self._p[v].add(u)

    # O(|E|)
    def remove_edge(self, e: TEdge):
        u, v = e
        if u in self._s: self._s[u].discard(v)
        if v in self._p: self._p[v].discard(u)
        if e in self._e: self._e.remove(e)                  # O(|E|)
        if not self.is_directed() and (v, u) in self._e:    # O(|E|)
            self._e.remove((v, u))                          # O(|E|)

    # O(1)*
    def contains_vertex(self, v: TVertex) -> bool:
        return v in self._v

    # O(1)*
    def contains_edge(self, e: TEdge) -> bool:
        u, v = e
        if self.is_directed():
            return u in self._s and v in self._s[u]
        return u in self._s and v in self._s[u] or v in self._s and u in self._s[v]

    # O(|V| + |E|)
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(V={list(self.V)}, E={list(self.E)})"


class UndirectedGraph(IGraph[TVertex]):
    # O(1)
    def is_directed(self) -> bool:
        return False


class Digraph(IGraph[TVertex]):
    # O(1)
    def is_directed(self) -> bool:
        return True


# WeightingFunction -----------------------------------------------------------------


class WeightingFunction(Generic[TVertex], dict[TEdge, Weight], Callable[[TVertex, TVertex], Weight]):
    # O(|data|) = O(|E|)
    def __init__(self, data: Union[Iterable[tuple[TEdge, Weight]], dict[TEdge, Weight]], symmetrical: bool = False):
        super().__init__(data)
        self.symmetrical = symmetrical
        to_delete: list[TEdge] = []
        edges: set[TEdge] = set()
        for e in self.keys():
            u, v = e
            if u == v:
                sys.stderr.write(
                    f"WeightingFunction - WARNING: Discarded auto edge {e} (with weight {self[e]}).\n")
                continue
            if symmetrical:
                e2 = v, u
                if e2 in edges:
                    if self[e2] != self[e]:
                        m = f"Weights are symmetrical but {e2} and {e} have differents weights: {self[e2]} != {self[e]}"
                        raise ValueError(m)
                    sys.stderr.write(
                        f"WeightingFunction - WARNING: Discarded repeated edge {e} (with weight {self[e]}).\n")
                    to_delete.append(e)  # dejar solo una arista en grafos no dirigidos
                else:
                    edges.add(e)
        for e in to_delete:
            del self[e]

    # O(1)*
    def __call__(self, u: Union[TVertex, TEdge], v: Optional[TVertex] = None) -> Weight:
        if v is None:
            u, v = u
        # if u == v:
        #    return 0
        if (u, v) in self:
            return self[u, v]
        if self.symmetrical:
            if (v, u) in self:
                return self[v, u]
            raise KeyError(repr((u, v)) + " nor " + repr((v, u)))
        raise KeyError(repr((u, v)))


if __name__ == '__main__':
    g = Digraph(E=[(1, 2)])
    print(g)
    print(isinstance(g, IGraph))
    print(isinstance(g, Digraph))
    print(isinstance(g, UndirectedGraph))
