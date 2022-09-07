from abc import abstractmethod, ABC
from typing import *

T = TypeVar('T')


class IMergeFindSet(ABC, Generic[T], Iterable, Sized):
    @abstractmethod
    def add(self, x: T): pass

    @abstractmethod
    def find(self, x: T) -> T: pass

    @abstractmethod
    def merge(self, x: T, y: T): pass


class MergeFindSet(IMergeFindSet):
    def __init__(self, sets: Iterable[Sequence[T]] = ()):
        self._parent: dict[T, T] = {}
        self._rank: dict[T, int] = {}
        self._length = 0
        first = None
        for s in sets:
            if len(s) > 0:
                self._length += 1
                for item in s:
                    if first is None:
                        first = item
                    self._parent[item] = first
                    self._rank[item] = self._rank.get(item, 0) + 1
                first = None

    def add(self, x: T):
        self._parent[x] = x
        self._rank[x] = 1
        self._length += 1

    def merge(self, x: T, y: T):
        u = self.find(x)
        v = self.find(y)
        if u != v:
            self._length -= 1
            if self._rank[u] < self._rank[v]:
                self._parent[u] = v
            elif self._rank[u] > self._rank[v]:
                self._parent[v] = u
            else:
                self._parent[v] = u
                self._rank[u] += 1

    def find(self, x: T) -> T:
        r = x
        while r != self._parent[r]:
            r = self._parent[r]
        while x != self._parent[x]:
            self._parent[x], x = r, self._parent[x]
        return r

    def __iter__(self) -> Iterable[Iterable[T]]:
        aux = {}
        for key in self._parent:
            aux.setdefault(self.find(key), []).append(key)
        for s in aux.values():
            yield s

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        return '{}({!r})'.format(self.__class__.__name__, tuple(self))
