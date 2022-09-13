import colorsys
import random
import sys

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.queues import Fifo
from algoritmia.viewers.labyrinth_viewer_color import LabyrinthViewerColor
from algoritmia.algorithms.traversers import bf_edge_traverser, df_edge_traverser

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]


def create_labyrinth_nowalls(num_rows: int, num_cols: int) -> UndirectedGraph[Vertex]:
    # Crear lista de vértices
    v = [(r, c) for r in range(num_rows) for c in range(num_cols)]

    # Crear lista de aristas entre vértices vecinos
    w = []
    for (r, c) in v:
        if r + 1 < num_rows: w.append(((r, c), (r + 1, c)))
        if c + 1 < num_cols: w.append(((r, c), (r, c + 1)))

    return UndirectedGraph(E=w)


def create_labyrinth_mfset(num_rows: int, num_cols: int) -> UndirectedGraph[Vertex]:
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

    # AÃ±adir los elementos de 'v' al MFSet
    for vertice in v: mfs.add(vertice)

    # Recorrer aristas en 'w',
    # obtener 'find' de los vertices de cada arista (v1,v2),
    # si 'v1' y 'v2' están en clases diferentes: hacer 'merge' y aÃ±adir arista a 'e'
    for (v1, v2) in w:
        if mfs.find(v1) != mfs.find(v2):
            mfs.merge(v1, v2)
            e.append((v1, v2))

    return UndirectedGraph(E=e)


def matriz_distancias_anchura(grafo, v_inicial):
    dist = {}
    queue = Fifo()
    seen = set()
    queue.push((v_inicial, v_inicial))
    seen.add(v_inicial)
    dist[v_inicial] = 0
    while len(queue) > 0:
        u, v = queue.pop()
        dist[v] = dist[u] + 1
        for suc in grafo.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push((v, suc))
    return dist


def int2col(n: int, maxint: int = 255) -> str:
    (r, g, b) = colorsys.hsv_to_rgb(float(n) / maxint * (300 / 360.0), 1.0, 1.0)
    return "#{:02x}{:02x}{:02x}".format(int(255 * r), int(255 * g), int(255 * b))


def int2gray(n: int, maxint: int = 255) -> str:
    k = 100
    m, M = k / 2, 255 - k / 2
    c = 255 - int(float(n) / maxint * (M - m) + m)
    return "#{:02x}{:02x}{:02x}".format(c, c, c)


def create_laberinth(num_rows: int, num_cols: int, tipo: int) -> UndirectedGraph[Vertex]:
    if tipo == 1:
        g = create_labyrinth_mfset(num_rows, num_cols)
    elif tipo == 2:
        g_aux = create_labyrinth_nowalls(num_rows, num_cols)
        edges = list(bf_edge_traverser(g_aux, (0, 0)))[1:]  # quitamos arista fantasma
        g = UndirectedGraph(E=edges)
    elif tipo == 3:
        g_aux = create_labyrinth_nowalls(num_rows, num_cols)
        edges = list(df_edge_traverser(g_aux, (0, 0)))[1:]  # quitamos arista fantasma
        g = UndirectedGraph(E=edges)
    else:
        raise Exception('Unknown tipo')
    return g


# int2col = int2gray


if __name__ == '__main__':
    random.seed(1)
    sys.setrecursionlimit(10000)

    cell_size = 13
    num_rows, num_cols = 60, 80

    # Tipo: 1 - MFSet random, 2 - Anchura en lab sin paredes, 3 - Profundidad en lab sin paredes
    tipo = 1
    g = create_laberinth(num_rows, num_cols, tipo)
    lv = LabyrinthViewerColor(g,
                              canvas_width=num_cols * cell_size + 20,
                              canvas_height=num_rows * cell_size + 20, margin=10,
                              wall_width=4)

    start = (0, 0)  # (num_rows//2, num_cols//2)
    matriz_dist = matriz_distancias_anchura(g, start)
    maxvalue = max(matriz_dist.values())
    for (v, k) in sorted([(v, k) for (k, v) in matriz_dist.items()]):
        lv.add_marked_cell(k, int2col(v, maxvalue))

    lv.run()
