from algoritmia.datastructures.graphs import UndirectedGraph, TVertex


# agrupa los vertices que pueden compartir color
def coloring_solve(g: UndirectedGraph[TVertex]) -> list[set[TVertex]]:
    solution: list[set[TVertex]] = []
    vertex_set = set(g.V)  # Creamos una copia de los vértices

    while len(vertex_set) > 0:
        grupo = set()  # Creamos un nuevo grupo vacío
        # Añadimos los vértices cuyos sucesores no estén ya en grupo
        for v in vertex_set:
            # Simple code --------
            #can_add_v = True
            #for suc in g.succs(v):
            #    if suc in grupo:
            #        can_add_v = False  # v tiene un sucesor en el grupo
            #        break
            #if can_add_v:
            #    grupo.add(v)

            # Estas dos lineas (con generadores) reemplazan a las siete anteriores
            if not any(suc in grupo for suc in g.succs(v)):
                grupo.add(v)

        solution.append(grupo)  # Añadimos el grupo a la solución
        vertex_set -= grupo     # Quitamos los vértices del grupo de V

    return solution


if __name__ == '__main__':
    graph = UndirectedGraph(E=[(0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 3), (2, 5),
                               (3, 4), (3, 5), (3, 6), (4, 7), (5, 6), (5, 8), (6, 7),
                               (6, 8), (6, 9), (7, 9), (8, 9)])
    print(coloring_solve(graph))
