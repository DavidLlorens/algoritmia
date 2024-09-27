from abc import abstractmethod, ABC
from collections.abc import Iterable, Sized
from collections import deque

# Fifo() utiliza una 'deque' de Python para tener coste O(1) en el pop()
# Lifo() utiliza una 'list' de Python


class IQueue[T](ABC, Sized):
    def __init__(self, data: deque[T] | list[T] = ()):
        self._list = data

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
        super().__init__(deque(data))

    def push(self, item: T):
        self._list.append(item)

    def pop(self) -> T:
        return self._list.popleft()

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
        print("q:", q)
        print("q.top():", q.top())
        print("len(q):", len(q))
        for i in range(3):
            print("q.pop():", q.pop())
