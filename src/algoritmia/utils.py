from collections.abc import Callable, Iterable
from typing import Optional

infinity = float("infinity")


def argmin[T, S](iterable: Iterable[T], fn: Callable[[T], S], ifempty: Optional[T] = None) -> Optional[T]:
    try:
        return min((fn(x), x) for x in iterable)[1]
    except ValueError:
        return ifempty


def argmax[T, S](iterable: Iterable[T], fn: Callable[[T], S], ifempty: Optional[T] = None) -> Optional[T]:
    try:
        return max((fn(x), x) for x in iterable)[1]
    except ValueError:
        return ifempty
