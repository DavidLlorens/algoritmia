from typing import *
from enum import Enum

from algoritmia.datastructures.graphs import UndirectedGraph
from easypaint import EasyPaint

Num = Union[int, float]
Vertex = tuple[Num, Num]


class Mode(Enum):
    ALL = 0
    MST = 1


class Graph2dMstViewer(EasyPaint):

    def __init__(self, g_all: UndirectedGraph[Vertex], g_mst: UndirectedGraph[Vertex],
                 canvas_width: int = 400, canvas_height: int = 300,
                 margin: int = 15, background='white', node_size: Optional[float] = None,
                 colors: dict[Vertex, str] = None):
        self.node_size = node_size
        self.margin = margin
        self.colors = colors
        if not isinstance(g_all, UndirectedGraph) or \
                any([not isinstance(p, tuple) or len(p) != 2 or
                     not isinstance(p[0], int) and not isinstance(p[0], float) or
                     not isinstance(p[1], int) and not isinstance(p[1], float) for p in g_all.V]):
            raise TypeError("The graph must be an UndirectedGraph. Vertices must be tuples of two integers or floats")

        self.g_all = g_all
        self.g_mst = g_mst
        self.mode = Mode.ALL
        self.g = self.g_all

        self.max_y = max(p[1] for p in self.g.V)
        self.max_x = max(p[0] for p in self.g.V)
        self.min_y = min(p[1] for p in self.g.V)
        self.min_x = min(p[0] for p in self.g.V)

        super().__init__()
        self.easypaint_configure(title='2D Graph MST Viewer - Press <space> to toogle',
                                 background=background,
                                 size=(canvas_width, canvas_height))

    def on_key_press(self, keysym: str):
        if keysym.lower() in ['return', 'escape']:
            self.close()
        elif keysym.lower() == 'space':
            if self.mode == Mode.ALL:
                self.g = self.g_mst
                self.mode = Mode.MST
            else:
                self.g = self.g_all
                self.mode = Mode.ALL
            self.erase()
            self.draw_graph()

    def draw_graph(self):
        w, h = self.size
        w -= self.margin
        h -= self.margin
        sizex = self.max_x - self.min_x + 1
        sizey = self.max_y - self.min_y + 1
        cell_size = min(w / sizex, h / sizey)

        m = ((w - cell_size * sizex) / 2 - self.min_x * cell_size + self.margin / 2,
             (h - cell_size * sizey) / 2 - self.min_y * cell_size + self.margin / 2)
        if self.node_size is None:
            self.node_size = (w * h / len(self.g.V)) ** 0.5 / 10  # cell_size / 8

        for u, v in self.g.E:
            self.create_line((u[0] + 0.5) * cell_size + m[0], (u[1] + 0.5) * cell_size + m[1],
                             (v[0] + 0.5) * cell_size + m[0], (v[1] + 0.5) * cell_size + m[1])

        if self.node_size > 0:
            for u in self.g.V:
                if self.colors is None:
                    fill = 'palegreen'
                elif u in self.colors:
                    fill = self.colors[u]
                else:
                    fill = 'white'
                self.create_filled_circle((u[0] + 0.5) * cell_size + m[0], (u[1] + 0.5) * cell_size + m[1],
                                          self.node_size, fill=fill)

    def main(self):
        self.draw_graph()


if __name__ == '__main__':
    from algoritmia.algorithms.mst import kruskal, prim
    from algoritmia.data.iberia import iberia2d, km2d

    # g_msf = kruskal(iberia2d, km2d)
    g_msf = prim(iberia2d, km2d)

    gv = Graph2dMstViewer(iberia2d, g_msf, canvas_width=800, canvas_height=800, margin=50)
    gv.run()
