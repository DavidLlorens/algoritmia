import random

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]


def create_labyrinth_mfset(num_rows: int, num_cols: int, extra_corridors: int = 0) -> UndirectedGraph[Vertex]:
    # Crear lista de vértices
    v = [(r, c) for r in range(num_rows) for c in range(num_cols)]

    # Crear lista de aristas entre vértices vecinos
    w = []
    for (r, c) in v:
        if r + 1 < num_rows: w.append(((r, c), (r + 1, c)))
        if c + 1 < num_cols: w.append(((r, c), (r, c + 1)))

    # Barajar la lista de aristas entre vértices vecinos
    random.shuffle(w)
    e = []

    # Crear un MFSet vacío
    mfs = MergeFindSet()

    # Añadir los elementos de 'v' al MFSet
    for vertice in v: mfs.add(vertice)

    # Recorrer aristas en 'w',
    # obtener 'find' de los vertices de cada arista (v1,v2),
    # si 'v1' y 'v2' están en clases diferentes: hacer 'merge' y añadir arista a 'e'
    for (v1, v2) in w:
        if mfs.find(v1) != mfs.find(v2):
            mfs.merge(v1, v2)
            e.append((v1, v2))
        elif extra_corridors > 0:
            e.append((v1, v2))
            extra_corridors -= 1

    return UndirectedGraph(E=e)


if __name__ == '__main__':
    random.seed(42)

    cell_size = 60
    num_rows, num_cols = 6, 8

    g = create_labyrinth_mfset(num_rows, num_cols, extra_corridors=0) # 3

    lv = LabyrinthViewer(g, margin=10,
                         canvas_width=num_cols * cell_size + 20,
                         canvas_height=num_rows * cell_size + 20)
    lv.run()
