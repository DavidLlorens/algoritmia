from abc import abstractmethod
from collections.abc import Sequence, Iterable, Iterator
from typing import Optional

from algoritmia.datastructures.prioritymaps import IPriorityMap


class IDoubleEndedPriorityDict[K, T](IPriorityMap[K, T]):
    @abstractmethod
    def worst(self) -> K: pass

    @abstractmethod
    def worst_value(self) -> T: pass

    @abstractmethod
    def worst_item(self) -> tuple[K, T]: pass

    @abstractmethod
    def extract_worst(self) -> K: pass

    @abstractmethod
    def extract_worst_item(self) -> tuple[K, T]: pass


class MinMaxIntervalHeapMap[K, T](IDoubleEndedPriorityDict[K, T]):
    def __init__(self, data: Iterable[tuple[K, T]] | dict[K, T] = (), capacity: int = 0):
        super().__init__()
        if isinstance(data, dict):
            data = data.items()
        elif not isinstance(data, Sequence):
            data = tuple(data)

        self._size = len(data)
        capacity = max(capacity, self._size)
        self._heap: list[Optional[tuple[K, T]]] = [(v, k) for (k, v) in data]
        self._heap.extend([None] * (capacity - self._size))
        self._index = {}
        for i in range(self._size): self._index[self._heap[i][1]] = i
        for v in range(0, self._size, 2):
            if v + 1 < self._size: self._swap(v)
        last_parent = self._parent(self._size - 1)
        for v in range(last_parent, -1, -2):
            self._heapify_min(v)
            self._heapify_max(v)

    def _children(self, i: int) -> Iterator[int]:
        j = 2 * (i + 1)
        if j < self._size: yield j
        j += 2
        if j < self._size: yield j

    @staticmethod
    def _parent(i: int) -> int:
        return ((i // 2 - 1) // 2) * 2

    def _swap(self, i: int) -> bool:
        if self._heap[i][0] > self._heap[i + 1][0]:
            self._heap[i], self._heap[i + 1] = self._heap[i + 1], self._heap[i]
            self._index[self._heap[i][1]] = i
            self._index[self._heap[i + 1][1]] = i + 1
            return True
        return False

    def __getitem__(self, key: K) -> T:
        if key not in self._index: raise KeyError(key)
        return self._heap[self._index[key]][0]

    def __delitem__(self, key: K):
        if key not in self._index: raise KeyError(key)
        (newvalue, newkey) = self._heap[self._size - 1]
        self._heap[self._size - 1] = None
        self._size -= 1
        i = self._index[key]
        del self._index[key]
        if i != self._size:
            self._heap[i] = (self._heap[i][0], newkey)
            self._index[newkey] = i
            self[newkey] = newvalue

    def __setitem__(self, key: K, v: T) -> T:
        if key in self._index:
            i = self._index[key]
            ii = i if i % 2 == 0 else i - 1
            oldvalue = self._heap[i][0]
            self._heap[i] = (v, key)
            if ii + 1 < self._size:
                if self._swap(ii):
                    oldvalue = self._heap[i][0]
                    if oldvalue < v:
                        self._bubble_up_max(ii)
                        self._heapify_min(ii)
                    elif oldvalue > v:
                        self._bubble_up_min(ii)
                        self._heapify_max(ii)
                else:
                    if oldvalue < v:
                        if ii == i:
                            self._heapify_min(ii)
                        else:
                            self._bubble_up_max(ii)
                    elif oldvalue > v:
                        if ii == i:
                            self._bubble_up_min(ii)
                        else:
                            self._heapify_max(ii)
            else:
                if v < oldvalue:
                    self._bubble_up_min(ii)
                elif v > oldvalue:
                    parent = self._parent(ii)
                    if parent >= 0:
                        if self._heap[parent + 1][0] < v:
                            self._heap[parent + 1], self._heap[ii] = \
                                self._heap[ii], self._heap[parent + 1]
                            self._index[self._heap[parent + 1][1]] = parent + 1
                            self._index[self._heap[ii][1]] = ii
                            self._bubble_up_max(parent)
        else:
            # self._index = self.redimMap(self._index, key) # TODO (XXX)
            if self._size == len(self._heap):
                self._heap.append(None)
            if self._size == 0:
                self._heap[0] = (v, key)
                self._index[key] = 0
                self._size += 1
            else:
                self._heap[self._size] = (v, key)
                self._index[key] = self._size
                self._size += 1
                if self._size % 2 == 0:
                    ii = self._size - 2
                    if self._swap(ii):
                        self._bubble_up_min(ii)
                    else:
                        self._bubble_up_max(ii)
                else:
                    ii = self._size - 1
                    parent = self._parent(ii)
                    if parent >= 0:
                        if self._heap[parent][0] <= v <= self._heap[parent + 1][0]: return v
                        if v > self._heap[parent + 1][0]:
                            self._heap[parent + 1], self._heap[ii] = self._heap[ii], self._heap[parent + 1]
                            self._index[self._heap[parent + 1][1]] = parent + 1
                            self._index[self._heap[ii][1]] = ii
                            self._bubble_up_max(parent)
                        elif v < self._heap[parent][0]:
                            self._heap[parent], self._heap[ii] = self._heap[ii], self._heap[parent]
                            self._index[self._heap[parent][1]] = parent
                            self._index[self._heap[ii][1]] = ii
                            self._bubble_up_min(parent)
        return v

    def min(self) -> K:
        if self._size == 0: raise IndexError("Empty Interval Heap")
        return self._heap[0][1]

    def min_value(self) -> T:
        if self._size == 0: raise IndexError("Empty Interval Heap")
        return self._heap[0][0]

    def min_item(self) -> tuple[K, T]:
        if self._size == 0: raise IndexError("Empty Interval Heap")
        return self._heap[0][1], self._heap[0][0]

    def max(self) -> K:
        if self._size == 0: raise IndexError("Empty Interval Heap")
        if self._size == 1: return self._heap[0][1]
        return self._heap[1][1]

    def max_value(self) -> T:
        if self._size == 0: raise IndexError("Empty Interval Heap")
        if self._size == 1: return self._heap[0][0]
        return self._heap[1][0]

    def max_item(self) -> tuple[K, T]:
        if self._size == 0: raise IndexError("Empty Interval Heap")
        if self._size == 1: return self._heap[0][1], self._heap[0][0]
        return self._heap[1][1], self._heap[1][0]

    def extract_min(self) -> K:
        return self.extract_min_item()[0]

    def extract_min_value(self) -> T:
        return self.extract_min_item()[1]

    def extract_min_item(self) -> tuple[K, T]:
        if self._size == 0: raise IndexError("Empty Interval Heap")
        retval = (self._heap[0][1], self._heap[0][0])
        if self._size <= 2:
            if self._size == 1:
                del self._index[self._heap[0][1]]
                self._heap[0] = None
            else:
                del self._index[self._heap[0][1]]
                self._heap[0], self._heap[1] = self._heap[1], None
                self._index[self._heap[0][1]] = 0
            self._size -= 1
            return retval
        del self._index[self._heap[0][1]]
        self._heap[0], self._heap[self._size - 1] = self._heap[self._size - 1], None
        self._index[self._heap[0][1]] = 0
        self._size -= 1
        self._heapify_min(0)
        return retval

    def extract_max(self) -> K:
        return self.extract_max_item()[0]

    def extract_max_value(self) -> T:
        return self.extract_max_item()[1]

    def extract_max_item(self) -> tuple[K, T]:
        if self._size == 0: raise Exception("Empty Interval Heap")
        if self._size == 1:
            retval = (self._heap[0][1], self._heap[0][0])
            del self._index[self._heap[0][1]]
            self._heap[0] = None
            self._size -= 1
            return retval
        retval = (self._heap[1][1], self._heap[1][0])
        if self._size == 2:
            del self._index[self._heap[1][1]]
            self._heap[1] = None
            self._size -= 1
            return retval
        del self._index[self._heap[1][1]]
        self._heap[1], self._heap[self._size - 1] = self._heap[self._size - 1], None
        self._index[self._heap[1][1]] = 1
        self._size -= 1
        self._heapify_max(0)
        return retval

    def _heapify_min(self, i: int):
        smallest = i
        while True:
            for j in self._children(i):
                if self._heap[j][0] < self._heap[smallest][0]: smallest = j
            if smallest == i: break
            self._heap[smallest], self._heap[i] = self._heap[i], self._heap[smallest]
            self._index[self._heap[smallest][1]] = smallest
            self._index[self._heap[i][1]] = i
            i = smallest
            if i + 1 < self._size:
                self._swap(i)

    def _heapify_max(self, i: int):
        largest = i + 1
        while True:
            for j in self._children(i):
                if j + 1 < self._size:
                    if self._heap[j + 1][0] > self._heap[largest][0]: largest = j + 1
                else:
                    if self._heap[j][0] > self._heap[largest][0]: largest = j
            if largest == i + 1: break
            self._heap[largest], self._heap[i + 1] = self._heap[i + 1], self._heap[largest]
            self._index[self._heap[largest][1]] = largest
            self._index[self._heap[i + 1][1]] = i + 1
            i = largest // 2 * 2
        if i + 1 < self._size:
            self._swap(i)

    def _bubble_up_max(self, i: int):
        while True:
            parent = self._parent(i)
            if parent < 0: return
            if self._heap[parent + 1][0] >= self._heap[i + 1][0]: return
            self._heap[parent + 1], self._heap[i + 1] = self._heap[i + 1], self._heap[parent + 1]
            self._index[self._heap[parent + 1][1]] = parent + 1
            self._index[self._heap[i + 1][1]] = i + 1
            i = parent

    def _bubble_up_min(self, i: int):
        while True:
            parent = self._parent(i)
            if parent < 0: return
            if self._heap[parent][0] <= self._heap[i][0]: return
            self._heap[parent], self._heap[i] = self._heap[i], self._heap[parent]
            self._index[self._heap[parent][1]] = parent
            self._index[self._heap[i][1]] = i
            i = parent

    def keys(self) -> Iterator[K]:
        for key in self._index: yield key

    def values(self) -> Iterator[T]:
        for key in self._index: yield self._heap[self._index[key]][0]

    def items(self) -> Iterator[tuple[K, T]]:
        for key in self._index:
            yield self._heap[self._index[key]][1], self._heap[self._index[key]][0]

    def get(self, key: K, default: T = None):
        if key in self._index: return self[key]
        return default

    def setdefault(self, key: K, default: T = None):
        if key in self._index: return self[key]
        self[key] = default
        return default

    def __contains__(self, key: K) -> bool:
        return key in self._index

    def __iter__(self) -> Iterator[K]:
        for key in self._index: yield key

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return '{}({!r})'.format(self.__class__.__name__,
                                 [(k, v) for (v, k) in self._heap[:self._size]])

    opt = min
    opt_value = min_value
    opt_item = min_item
    extract_opt = extract_min
    extract_opt_item = extract_min_item

    worst = max
    worst_value = max_value
    worst_item = max_item
    extract_worst = extract_max
    extract_worst_item = extract_max_item


class MaxMinIntervalHeapMap(MinMaxIntervalHeapMap):
    opt = MinMaxIntervalHeapMap.max
    opt_value = MinMaxIntervalHeapMap.max_value
    opt_item = MinMaxIntervalHeapMap.max_item
    extract_opt = MinMaxIntervalHeapMap.extract_max
    extract_opt_item = MinMaxIntervalHeapMap.extract_max_item

    worst = MinMaxIntervalHeapMap.min
    worst_value = MinMaxIntervalHeapMap.min_value
    worst_item = MinMaxIntervalHeapMap.min_item
    extract_worst = MinMaxIntervalHeapMap.extract_min
    extract_worst_item = MinMaxIntervalHeapMap.extract_min_item
