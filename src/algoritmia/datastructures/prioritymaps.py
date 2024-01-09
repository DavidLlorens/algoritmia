from abc import abstractmethod, ABC
from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import repeat
from typing import Optional

from math import log, sqrt


class IPriorityMap[K, T](ABC, dict[K, T]):
    @abstractmethod
    def opt(self) -> K: pass

    @abstractmethod
    def opt_item(self) -> tuple[K, T]: pass

    @abstractmethod
    def opt_value(self) -> T: pass

    @abstractmethod
    def extract_opt(self) -> K: pass

    @abstractmethod
    def extract_opt_item(self) -> tuple[K, T]: pass


# -------------------------------------------------------------------------

class MinHeapMap[K, T](IPriorityMap[K, T]):
    _opt: Callable[[T, T], T] = min

    def __init__(self, data: Iterable[tuple[K, T]] | dict[K, T] = (), capacity: int = 0):
        super().__init__()
        # self._opt = opt
        self._index = {}
        if isinstance(data, dict):
            data = data.items()
        elif not isinstance(data, Sequence):
            data = tuple(data)
        for (i, (key, _)) in enumerate(data):
            self._index[key] = i + 1
        self._size = len(data)
        self._heap: list[Optional[tuple[T, K]]] = [None]
        self._heap.extend((v, k) for (k, v) in data)
        self._heap.extend(repeat(None, max(0, capacity - self._size)))
        for i in range(self._size // 2, 0, -1):
            self._heapify(i)

    def _heapify(self, i: int):
        while True:
            left: int = 2 * i
            right: int = 2 * i + 1
            if left <= self._size and self._opt(self._heap[left], self._heap[i]) != self._heap[i]:
                best = left
            else:
                best = i
            if right <= self._size and self._opt(self._heap[right], self._heap[best]) != self._heap[best]:
                best = right
            if best == i:
                break
            self._index[self._heap[i][1]], self._index[self._heap[best][1]] = best, i
            self._heap[i], self._heap[best] = self._heap[best], self._heap[i]
            i = best

    def _bubble_up(self, i: int):
        p = i // 2
        while i > 1 and self._opt(self._heap[i], self._heap[p]) != self._heap[p]:
            self._index[self._heap[i][1]], self._index[self._heap[p][1]] = p, i
            self._heap[i], self._heap[p] = self._heap[p], self._heap[i]
            i, p = p, p // 2

    def opt(self) -> K:
        if self._size == 0:
            raise IndexError('opt from an empty priority dict')
        return self._heap[1][1]

    def opt_item(self) -> tuple[K, T]:
        if self._size == 0:
            raise IndexError('opt from an empty priority dict')
        return self._heap[1][1], self._heap[1][0]

    def opt_value(self) -> T:
        if self._size == 0:
            raise IndexError('opt from an empty priority dict')
        return self._heap[1][0]

    def extract_opt(self) -> K:
        return self.extract_opt_item()[0]

    def extract_opt_item(self) -> tuple[K, T]:
        m = self.opt_item()
        if self._size > 1:
            self._heap[1], self._index[self._heap[self._size][1]] = self._heap[self._size], 1
            self._heap[self._size] = None
        self._size -= 1
        if self._size > 1:
            self._heapify(1)
        del self._index[m[0]]
        return m

    def __contains__(self, key: K) -> bool:
        return key in self._index

    def __getitem__(self, key: K) -> T:
        return self._heap[self._index[key]][0]

    def __setitem__(self, key: K, score: T) -> T:
        if key in self._index:
            i = self._index[key]
            if score == self._heap[i][0]:
                return score
            if self._opt(score, self._heap[i][0]) != score:
                self._heap[i] = (score, key)
                self._heapify(i)
                return score
        else:
            if self._size + 1 >= len(self._heap):
                self._heap.append(None)
            self._index[key] = i = self._size = self._size + 1
        self._heap[i] = (score, key)
        self._bubble_up(i)
        return score

    def __delitem__(self, key: K):
        if key not in self._index:
            raise KeyError(key)
        i = self._index[key]
        self._heap[i], self._index[self._heap[self._size][1]] = self._heap[self._size], i
        self._size -= 1
        self._heapify(i)
        if i > 1 and self._heap[i] < self._heap[i // 2]:
            p = i // 2
            while i > 1 and self._heap[i] < self._heap[p]:
                self._index[self._heap[i][1]], self._index[self._heap[p][1]] = p, i
                self._heap[i], self._heap[p] = self._heap[p], self._heap[i]
                i, p = p, p // 2
        else:
            self._heapify(i)
        del self._index[key]

    def keys(self) -> Iterator[K]:
        for key in self._index:
            yield key

    def values(self) -> Iterator[T]:
        for key in self._index:
            yield self._heap[self._index[key]][0]

    def items(self) -> Iterator[tuple[K, T]]:
        for key in self._index:
            yield self._heap[self._index[key]][1], self._heap[self._index[key]][0]

    def get(self, key: K, default: T = None) -> T:
        if key in self._index:
            return self[key]
        return default

    def setdefault(self, key: K, default: T = None) -> T:
        if key in self._index:
            return self[key]
        self[key] = default
        return default

    def __iter__(self) -> Iterator[K]:
        for key in self._index:
            yield key

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        if self.__class__.__name__ == 'HeapMap':
            b = 'min' if self._opt == min else 'max'
            return 'HeapMap({}, {!r})'.format(b, [(k, self[k]) for k in self])
        return '{}({!r})'.format(self.__class__.__name__, [(k, self[k]) for k in self])


class MaxHeapMap(MinHeapMap):
    _opt = max


# -------------------------------------------------------------------------

class FibNode[K, T]:
    def __init__(self, key: K, value: T):
        self.parent = self.child = None
        self.left = self.right = self
        self.key = key
        self.value = value
        self.degree = 0
        self.mark = False


class MinFibonacciHeap[K, T](IPriorityMap[K, T]):
    _opt: Callable[[T, T], T] = min

    def __init__(self, data: Iterable[tuple[K, T]] = ()):
        super().__init__()
        self._size = 0
        self._minroot: Optional[FibNode[K, T]] = None
        self._map = dict()
        self._opt2 = lambda a, b: None if a is None or b is None else self._opt(a, b)
        for key, value in data:
            self.add(key, value)

    def __getitem__(self, key: K) -> T:
        return self._map[key].value

    def opt_item(self) -> tuple[K, T]:
        return self._minroot.key, self._minroot.value

    def opt(self) -> K:
        return self._minroot.key

    def opt_value(self) -> T:
        return self._minroot.value

    def add(self, key: K, value: T):
        node = self._map[key] = FibNode(key, value)
        if self._minroot is None:
            self._minroot = node
        else:
            node.left, node.right = self._minroot, self._minroot.right
            self._minroot.right = node.right.left = node
            if self._opt2(node.value, self._minroot.value) != self._minroot.value:
                self._minroot = node
        self._size += 1

    def extract_opt(self) -> K:
        opt = self.opt()
        self._remove_opt()
        return opt

    def extract_opt_item(self) -> tuple[K, T]:
        item = (self._minroot.key, self._minroot.value)
        self._remove_opt()
        return item

    def _remove_opt(self):
        z = self._minroot
        del self._map[z.key]
        if z is not None:
            nchildren = z.degree
            x = z.child
            while nchildren > 0:
                t = x.right
                x.left.right, x.right.left = x.right, x.left
                x.left, x.right = self._minroot, self._minroot.right
                self._minroot.right = x.right.left = x
                x.parent = None
                x = t
                nchildren -= 1
            z.left.right, z.right.left = z.right, z.left
            if z == z.right:
                self._minroot = None
            else:
                self._minroot = z.right
                self._consolidate()
            self._size -= 1

    _philog = log((1 + sqrt(5)) / 2)

    def _consolidate(self):
        a: list[Optional[FibNode[K, T]]] = [None] * int(log(self._size) / self._philog)
        n_roots = self._count_roots()
        x = self._minroot
        while n_roots > 0:
            d = x.degree
            next0 = x.right
            while a[d] is not None:
                y = a[d]
                if self._opt2(x.value, y.value) != x.value: x, y = y, x
                self._link(y, x)
                a[d] = None
                d += 1
            a[d] = x
            x = next0
            n_roots -= 1

        self._minroot = None
        for x in a:
            if x is not None:
                if self._minroot is not None:
                    x.left.right, x.right.left = x.right, x.left
                    x.left, x.right = self._minroot, self._minroot.right
                    self._minroot.right = x
                    x.right.left = x
                    if self._opt2(x.value, self._minroot.value) != self._minroot.value:
                        self._minroot = x
                else:
                    self._minroot = x

    def _count_roots(self) -> int:
        n_roots = 0
        x = self._minroot
        if x is not None:
            n_roots += 1
            x = x.right
            while x != self._minroot:
                n_roots += 1
                x = x.right
        return n_roots

    @staticmethod
    def _link(y: FibNode[K, T], x: FibNode[K, T]):
        y.left.right, y.right.left = y.right, y.left
        y.parent = x
        if x.child is None:
            x.child = y.right = y.left = y
        else:
            y.left, y.right = x.child, x.child.right
            x.child.right = y.right.left = y
        x.degree += 1
        y.mark = False

    def __setitem__(self, key: K, value: T):
        if key not in self._map:
            self.add(key, value)
        else:
            self._improve_value(key, value)

    def _improve_value(self, key: K, value: T):
        node = self._map[key]
        if self._opt2(value, node.value) != value:
            raise ValueError("{} at {} does not improve {}".format(value, key, node.value))
        node.value = value
        parent = node.parent
        if parent is not None and self._opt2(node.value, parent.value) != parent.value:
            self._cut(node, parent)
            self._cascading_cut(parent)
        if self._opt2(node.value, self._minroot.value) != self._minroot.value:
            self._minroot = node

    def _cut(self, x: FibNode[K, T], y: FibNode[K, T]):
        x.left.right, x.right.left = x.right, x.left
        y.degree -= 1
        if y.child == x: y.child = x.right
        if y.degree == 0: y.child = None
        x.left, x.right = self._minroot, self._minroot.right
        self._minroot.right = x
        x.right.left = x
        x.parent = None
        x.mark = False

    def _cascading_cut(self, node: FibNode[K, T]):
        parent = node.parent
        if parent is not None:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def __delitem__(self, key: K):
        self._improve_value(key, None)
        self._remove_opt()

    def keys(self) -> Iterable[K]:
        return self._map.keys()

    def values(self) -> Iterator[T]:
        for key in self._map: yield self._map[key].value

    def items(self) -> Iterator[tuple[K, T]]:
        for key in self._map:
            yield key, self._map[key].value

    def get(self, key: K, default: T = None) -> T:
        if key in self._map: return self[key]
        return default

    def setdefault(self, key: K, default: T = None):
        if key in self._map: return self[key]
        self[key] = default
        return default

    def __contains__(self, key: K) -> bool:
        return key in self._map

    def __len__(self) -> "int":
        return self._size

    def __iter__(self) -> Iterator[K]:
        for key in self._map: yield key

    def __repr__(self) -> str:
        if self.__class__.__name__ == 'FibonacciHeap':
            b = 'min' if self._opt2 == min else 'max'
            return 'FibonacciHeap({}, {!r})'.format(b, [(k, self[k]) for k in list(self)])
        return '{}({!r})'.format(self.__class__.__name__, [(k, self[k]) for k in list(self)])


class MaxFibonacciHeap(MinFibonacciHeap):
    _opt = max

# -------------------------------------------------------------------------
