from typing import *

from algoritmia.datastructures.graphs import UndirectedGraph

T = TypeVar('T')


# agrupa los vertices que pueden compartir color
def coloring_solve(g: UndirectedGraph) -> list[set[T]]:
    solution = []

    # Creamos un nuevo conjunto con todos los vértices del grafo
    vertex_set = set(g.V)

    # Mientras queden vértices en el conjunto que no tengan grupo
    while len(vertex_set) > 0:
        # Creamos un nuevo grupo
        grupo = set()
        # Recorremos todos los vertices sin grupo
        for v in vertex_set:
            if not any(suc in grupo for suc in g.succs(v)):
                grupo.add(v)
        # Cerramos el grupo, lo añadimos a la solución y
        # quitamos de vertex_set los vértices que hemos metido en el nuevo grupo
        solution.append(grupo)
        vertex_set -= grupo

    return solution


if __name__ == '__main__':
    graph = UndirectedGraph(E=[(0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 3), (2, 5),
                               (3, 4), (3, 5), (3, 6), (4, 7), (5, 6), (5, 8), (6, 7),
                               (6, 8), (6, 9), (7, 9), (8, 9)])
    print(coloring_solve(graph))
