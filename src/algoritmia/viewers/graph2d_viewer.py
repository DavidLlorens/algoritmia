"""
05/10/2021: Version 1.5. Tamaño nodos y margen.
28/09/2021: Version 1.4. Actualizado a easypaint 2.x.
28/09/2021: Version 1.3. Añadidos canvas_width y canvas_height en el constructor
                         (reemplazan a window_size)
15/09/2021: Version 1.2. Permite poner el fondo transparente (en el IU es blanco, pero
                         en el eps se genera transparente).
24/09/2019: Version 1.1. Corregido modo ROW_COL para que funcione como LabyrinthViewer
02/10/2013: Version 1
@author: David Llorens dllorens@uji.es

Dos modos de funcionamiento según parámetro del constructor (vertexmode):

- Modo ROW_COL (8 filas, 14 columnas):
   (0,0)-----(0,14)
     |         |
   (8,0)-----(8,14)

- Modo X_Y (mismos puntos):
   (0,14)--(8,14)
     |       |
     |       |
     |       |
   (0,0)---(8,0)
"""

from typing import *
from math import sin, cos, pi, sqrt
import tkinter

from algoritmia.datastructures.graphs import IGraph, UndirectedGraph, Digraph
from easypaint import EasyPaint

Num = Union[int, float]
Vertex = tuple[Num, Num]


# -------------------------------------------------------------------------------------

def dist(p1, p2):
    return sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def find_intersec_point(cx, cy, radius, p1x, p1y, p2x, p2y):
    dx = p2x - p1x
    dy = p2y - p1y

    A = dx * dx + dy * dy
    B = 2 * (dx * (p1x - cx) + dy * (p1y - cy))
    C = (p1x - cx) * (p1x - cx) + (p1y - cy) * (p1y - cy) - radius * radius

    det = B * B - 4 * A * C
    if A <= 0.0000001 or det < 0:
        raise Exception("No real solutions")
    if det == 0:
        # One solution.
        t = -B / (2 * A)
        return (p1x + t * dx, p1y + t * dy), None
    else:
        # Two solutions.
        t1 = (-B + sqrt(det)) / (2 * A)
        t2 = (-B - sqrt(det)) / (2 * A)
        return (p1x + t1 * dx, p1y + t1 * dy), (p1x + t2 * dx, p1y + t2 * dy)


# -------------------------------------------------------------------------------------


class Graph2dViewer(EasyPaint):
    X_Y = 0
    ROW_COL = 1

    def __init__(self, g: IGraph[Vertex], v_label=None, canvas_width: int = 400, canvas_height: int = 300,
                 margin: int = 15, vertexmode=X_Y, background='white', node_size: Optional[float] = None,
                 title=None, colors: Optional[dict[Vertex, str]] = None):
        self.node_size = node_size
        self.margin = margin
        self.colors = colors if colors is not None else {}
        self.is_directed = isinstance(g, Digraph)
        self.v_label = v_label
        if not isinstance(g, UndirectedGraph) and not isinstance(g, Digraph):
            raise TypeError("The first parameter must be an UndirectedGraph or a Digraph")
        if any([not isinstance(p, tuple) or len(p) != 2 or
                not isinstance(p[0], int) and not isinstance(p[0], float) or
                not isinstance(p[1], int) and not isinstance(p[1], float) for p in g.V]):
            raise TypeError("Vertices must be tuples of two integers or floats")

        if vertexmode == Graph2dViewer.ROW_COL:
            if any([not isinstance(p[0], int) for p in g.V]):
                raise TypeError("In this mode, vertices must be tuples of two integers")
            g = UndirectedGraph(V=[(v[1], -v[0]) for v in g.V], E=[((u[1], -u[0]), (v[1], -v[0])) for (u, v) in g.E])

        self.g = g

        self.max_y = max(p[1] for p in self.g.V)
        self.max_x = max(p[0] for p in self.g.V)
        self.min_y = min(p[1] for p in self.g.V)
        self.min_x = min(p[0] for p in self.g.V)

        super().__init__()

        self.easypaint_configure(size=(canvas_width, canvas_height),
                                 title='2D Graph Viewer' if title is None else title,
                                 background=background)

        w, h = self.size
        w -= self.margin
        h -= self.margin
        sizex = self.max_x - self.min_x + 1
        sizey = self.max_y - self.min_y + 1
        self.cell_size = cell_size = min(w / sizex, h / sizey)

        self.m = ((w - cell_size * sizex) / 2 - self.min_x * cell_size + self.margin / 2,
                  (h - cell_size * sizey) / 2 - self.min_y * cell_size + self.margin / 2)
        if self.node_size is None:
            self.node_size = (w * h / len(self.g.V)) ** 0.5 / 10  # cell_size / 8

    def on_key_press(self, keysym):
        if keysym in ['Return', 'Escape']:
            self.close()

    def draw_arrow(self, u, v, color='black', width=1, tag='arrow'):
        cell_size = self.cell_size
        m = self.m
        if not self.is_directed:
            self.create_line((u[0] + 0.5) * cell_size + m[0], (u[1] + 0.5) * cell_size + m[1],
                             (v[0] + 0.5) * cell_size + m[0], (v[1] + 0.5) * cell_size + m[1])
        else:
            p1, p2 = find_intersec_point(v[0], v[1], (self.node_size + width) / self.cell_size,
                                         u[0], u[1], v[0], v[1])
            _, (x2, y2) = min((dist(u, p1), p1), (dist(u, p2), p2))
            x1, y1 = u
            l2 = self.node_size

            phi = 30 * pi / 180
            l1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            l2 /= self.cell_size

            x3 = x2 + l2 / l1 * ((x1 - x2) * cos(phi) + (y1 - y2) * sin(phi))
            x4 = x2 + l2 / l1 * ((x1 - x2) * cos(phi) - (y1 - y2) * sin(phi))

            y3 = y2 + l2 / l1 * ((y1 - y2) * cos(phi) - (x1 - x2) * sin(phi))
            y4 = y2 + l2 / l1 * ((y1 - y2) * cos(phi) + (x1 - x2) * sin(phi))

            self.create_line((x1 + 0.5) * cell_size + m[0], (y1 + 0.5) * cell_size + m[1],
                             (x2 + 0.5) * cell_size + m[0], (y2 + 0.5) * cell_size + m[1],
                             color, width=width, capstyle=tkinter.ROUND, tag=tag)
            self.create_line((x2 + 0.5) * cell_size + m[0], (y2 + 0.5) * cell_size + m[1],
                             (x3 + 0.5) * cell_size + m[0], (y3 + 0.5) * cell_size + m[1],
                             color, width=width, capstyle=tkinter.ROUND, tag=tag)
            self.create_line((x2 + 0.5) * cell_size + m[0], (y2 + 0.5) * cell_size + m[1],
                             (x4 + 0.5) * cell_size + m[0], (y4 + 0.5) * cell_size + m[1],
                             color, width=width, capstyle=tkinter.ROUND, tag=tag)

    def draw_vertex(self, u: Vertex, color='black', fill='palegreen', width=1, tag='vertex'):
        self.create_filled_circle((u[0] + 0.5) * self.cell_size + self.m[0],
                                  (u[1] + 0.5) * self.cell_size + self.m[1],
                                  self.node_size, color=color, width=width, fill=fill, tag=tag)
        if self.v_label is not None:
            label, fs = self.v_label[u], int(self.node_size)
            self.create_text((u[0] + 0.5) * self.cell_size + self.m[0],
                             (u[1] + 0.5) * self.cell_size + self.m[1],
                             label, fs, color=color, tag=tag)

    def main(self):
        width = 1
        color = 'black'
        for u, v in self.g.E:
            self.draw_arrow(u, v, color=color, width=width)
        for u in self.g.V:
            fill = 'palegreen' if len(self.colors) == 0 else self.colors[u] if u in self.colors else 'white'
            self.draw_vertex(u, fill=fill, width=width)


if __name__ == '__main__':
    c = {'A': (10, 1), 'B': (15, 4), 'C': (10, 7), 'D': (20, 4)}
    v_label = dict((v, k) for (k, v) in c.items())

    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'B')]
    edges2 = [(c[u], c[v]) for (u, v) in edges]

    # g = UndirectedGraph(E=edges2)
    g = Digraph(E=edges2)
    viewer = Graph2dViewer(g, v_label, canvas_width=400, canvas_height=300)
    viewer.run()
