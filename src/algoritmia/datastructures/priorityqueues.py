from abc import abstractmethod, ABC
from itertools import chain, repeat
from typing import *

T = TypeVar('T')


class IPriorityQueue(ABC, Sized, Generic[T]):
    @abstractmethod
    def add(self, item: T): pass

    @abstractmethod
    def opt(self) -> T: pass

    @abstractmethod
    def extract_opt(self) -> T: pass


class MinHeap(IPriorityQueue[T]):
    _opt: Callable[[T, T], T] = min

    def __init__(self, data: Sequence[T] = (), capacity: int = 0):
        # self._opt = self.opt
        self._size = len(data)
        self._heap: list[T] = list(chain((None,), data, repeat(None, max(0, capacity - self._size))))
        for i in range(self._size // 2, 0, -1):
            self._heapify(i)

    def _heapify(self, i: int):
        while True:
            left: int = 2 * i
            right: int = left + 1
            if left <= self._size and self._opt(self._heap[left], self._heap[i]) != self._heap[i]:
                best = left
            else:
                best = i
            if right <= self._size and self._opt(self._heap[right], self._heap[best]) != self._heap[best]:
                best = right
            if best == i:
                break
            self._heap[i], self._heap[best] = self._heap[best], self._heap[i]
            i = best

    def opt(self) -> T:
        if self._size == 0:
            raise IndexError('opt from an empty heap')
        return self._heap[1]

    def extract_opt(self) -> T:
        if self._size == 0:
            raise IndexError('extract opt from an empty heap')
        m = self._heap[1]
        if self._size > 1:
            self._heap[1], self._heap[self._size] = self._heap[self._size], None
        self._size -= 1
        if self._size > 1:
            self._heapify(1)
        return m

    def add(self, item: T):
        if self._size + 1 == len(self._heap):
            self._heap.append(None)
        i = self._size = self._size + 1
        self._heap[i] = item
        self._bubble_up(i)

    def _bubble_up(self, i: int):
        parent = i // 2
        while i > 1 and self._opt(self._heap[i], self._heap[parent]) != self._heap[parent]:
            self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
            i, parent = parent, parent // 2

    def __iter__(self) -> Iterable[T]:
        for i in range(1, self._size + 1): yield self._heap[i]

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        if self.__class__.__name__ == 'Heap':
            b = 'min' if self._opt == min else 'max'
            return 'Heap({}, {!r})'.format(b, self._heap[1:self._size + 1])
        return '{}({!r})'.format(self.__class__.__name__, self._heap[1:self._size + 1])


class MaxHeap(MinHeap):
    _opt = max
