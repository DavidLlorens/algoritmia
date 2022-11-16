# Changelog

## [2.0.9] - 2022-11-16
  - `algoritmia/schemes/bt_scheme.py`. Tipo devuelto por successors más específico.
  - `algoritmia/schemes/bab_scheme.py`. Corregido tipo de BoundedDecisionDequence. Tipo devuelto por successors más específico. 
  - Cambios menores (para quitar warnings de PyCharm):
    - `algoritmia/examples/backtracking/coin_change_bt.py` 
    - `algoritmia/examples/backtracking/nqueens_bt.py`
    - `algoritmia/examples/branch_and_bound/knapsack_bab.py`

## [2.0.8] - 2022-11-15
  - `algoritmia/schemes/bt_scheme.py`. Añadido State como sinónimo de Any.
  - `algoritmia/algorithms/traversers.py`. Cambios en dos comentarios.
  - `algoritmia/schemes/dac_scheme.py`. Cambiado Iterable por Iterator.
  - `algoritmia/examples/divide_and_conquer/*`. Añadir varios ejemplos.

## [2.0.7] - 2022-10-06
  - `algoritmia/schemes/bt_scheme.py`. El método abstracto `successors()` de la clase `DecisionsSequence` ahora devuelve 
    `Iterator` en lugar de `Iterable`. Afectados:
    - `algoritmia/examples/branch_and_bound/*.py` 
    - `algoritmia/examples/backtracking/*.py` 
  - Bug corregidos:
    - `algoritmia/algorithms/topological_sort.py` (no afectaba a su funcionamiento).
  - Añadidos comentarios al código:
    - `algoritmia/datastructures/graphs.py`

## [2.0.6] - 2022-10-02

- Añadidos algunos tipos que faltaban: 
  - `algoritmia/examples/greedy/coin_change_greedy.py`
  - `algoritmia/examples/greedy/knapsack_fraq_greedy.py`
  - `algoritmia/algorithms/mst.py`
- Cambios estéticos:
  - `algoritmia/examples/greedy/coin_change_greedy.py`
  - `algoritmia/examples/greedy/knapsack_fraq_greedy.py`
- Añadido nuevo ejemplo: 
  - `algoritmia/examples/greedy/activities_selector_greedy.py`
- `algoritmia/algorithms/shortest_path.py`: 
  - Anadidos dos algoritmos de programación dinámica
  - Añadidos comentarios adicionales

## [2.0.5] - 2022-10-01

- Los tipos genericos de la bilioteca se han renombrado añadiendo una 'T' como prefijo:
  - `algoritmia.schemes`: `TDecision`
  - `algoritmia.datastructures.graphs`: `TVertex`, `TEdge`
  - `algoritmia.algorithms.traversers`: `TVertexTraverser`, `TEdgeTraverser`
  - `algoritmia.algorithms.connected_components`: `TCC`
  - `algoritmia.algorithms.shortest_path`: `TPath`

- Añadidos tipos y comentarios:
  - `algoritmia/examples/backtracking/*.py` 
  - `algoritmia/examples/branch_and_bound/*.py`
  - `algoritmia/examples/dynamic_programming/*.py`
  
- Modificaciones:
  - `algoritmia/schemes/bt_scheme.py`: Añadido `StateDecisionSequence(DecisionSequence)` para `bt_vc_solve()`.

- Bugs corregidos:
  - `algoritmia/examples/dynamic_programming/edit_distance.py`

- Cambios de nombre de archivo:
  - `algoritmia/examples/dynamic_programming/shortest_path_dp.py` a
    `algoritmia/examples/dynamic_programming/shortest_path_graph.py`

## [2.0.4] - 2022-09-27

- Las funciones con `yield` ahora devuelven un `Iterator[T]` (antes era `Iterable[T]`). Ahora podemos usar `next()` sin que haya un error de tipo. El cambio no supone ningún problema, pues `Iterator` hereda de `Iterable`. 
  
  La alternativa era utilizar `Generator[T, None, None]`, que hereda de `Iterator[T]`, pero añade métodos que no utilizamos (p.e. para comunicación bidireccional).

- Las clases `Callable`, `Collection`, `Iterable`, `Iterator`, `Sequence` y `Sized`  se importan de `collection.abc` (antes se importaban de `typing`).
- Reemplazados todos los `from typing import *` para que solo se importe lo utilizado.
- Para evitar los anotaciones de tipo como texto en los métodos que nombran el tipo de su clase, utilizamos `from __future__ import annotations`.
- Se han añadido las anotaciones de tipo a los métodos `succs` y `preds` de `IGraph`.
## [2.0.3] - 2022-09-01

Version inicial
