from abc import abstractmethod, ABC
from collections.abc import Iterable, Sized

from algoritmia.datastructures.linkedlists import LinkedList


# Fifo() utiliza una lista LinkedList para tener coste O(1) en el pop()
# Lifo() utiliza una lista normal de Python


class IQueue[T](ABC, Sized):
    def __init__(self, mylist: list):
        self._list = mylist

    @abstractmethod
    def push(self, item: T): pass

    @abstractmethod
    def pop(self) -> T: pass

    @abstractmethod
    def top(self) -> T: pass

    def __len__(self) -> int:
        return len(self._list)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({list(self._list)})'


class Fifo[T](IQueue[T]):
    def __init__(self, data: Iterable[T] = ()):
        super().__init__(LinkedList(data))

    def push(self, item: T):
        self._list.append(item)

    def pop(self) -> T:
        v = self._list[0]
        del self._list[0]
        return v

    def top(self) -> T:
        return self._list[0]


class Lifo[T](IQueue[T]):
    def __init__(self, data: Iterable[T] = ()):
        super().__init__(list(data))

    def push(self, item: T):
        self._list.append(item)

    def pop(self) -> T:
        return self._list.pop()

    def top(self) -> T:
        return self._list[-1]


if __name__ == '__main__':
    for q in [Fifo(), Lifo()]:
        for i in range(3):
            q.push(i)
        print(q)
        for i in range(3):
            print(q.pop())
