from typing import *

infinity = float("+inf")

T = TypeVar('T')
S = TypeVar('S')


def argmin(iterable: Iterable[T], fn: Callable[[T], S], ifempty: Optional[T] = None) -> T:
    try:
        return min((fn(x), x) for x in iterable)[1]
    except ValueError:
        return ifempty


def argmax(iterable: Iterable[T], fn: Callable[[T], S], ifempty: Optional[T] = None) -> T:
    try:
        return max((fn(x), x) for x in iterable)[1]
    except ValueError:
        return ifempty
