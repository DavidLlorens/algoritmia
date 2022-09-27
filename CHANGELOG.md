# Changelog

## [2.0.4] - 2022-09-27

- Las funciones con `yield` ahora devuelven un `Iterator[T]` (antes era `Iterable[T]`). Ahora podemos usar `next()` sin que haya un error de tipo. El cambio no supone ningún problema, pues `Iterator` hereda de `Iterable`. 
  
  La alternativa era utilizar `Generator[T, None, None]`, que hereda de `Iterator[T]`, pero añade métodos que no utilizamos (p.e. para comunicación bidireccional).

- Las clases `Callable`, `Collection`, `Iterable`, `Iterator`, `Sequence` y `Sized`  se importan de `collection.abc` (antes se importaban de `typing`).
- Reemplazados todos los `from typing import *` para que solo se importe lo utilizado.
- Para evitar los anotaciones de tipo como texto en los métodos que nombran el tipo de su clase, utilizamos `from __future__ import annotations`.
- Se han añadido las anotaciones de tipo a los métodos `succs` y `preds` de `IGraph`.
## [2.0.3] - 2022-09-01

Version inicial
