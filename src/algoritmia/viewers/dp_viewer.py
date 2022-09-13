"""
Visor de grafos de dependencias y trellis de programacion dinámica
@author: David Llorens dllorens@uji.es

02/12/2021: Version 1
"""

from typing import *
from math import sin, cos, pi, sqrt, atan2
import tkinter

from easypaint import EasyPaint

Num = Union[int, float]
Label = str


class NodeStyle:
    def __init__(self, color: str = 'black', width: int = 1, fontsize: int = 10, fx: float = 1.0, fy: float = 1.0):
        self.color = color
        self.width = width
        self.fontsize = fontsize
        self.fx = fx
        self.fy = fy

    def _key(self) -> tuple[str, int]:
        return self.color, self.width

    def __hash__(self) -> int:
        return hash(self._key)

    def __eq__(self, other: 'NodeStyle') -> bool:
        if not isinstance(other, NodeStyle):
            return False
        return self._key() == other._key()


class EdgeStyle(NodeStyle):
    def __init__(self, color: str = 'black', width: int = 1, fontsize: int = 10, fx: float = 1.0, fy: float = 1.0,
                 pos: float = 0.5):
        super().__init__(color, width, fontsize, fx, fy)
        self.pos = pos

    def __key(self) -> tuple[tuple[str, int], float]:
        return super()._key(), self.pos


Pos = tuple[Num, Num]
Node = tuple[Pos, Label, NodeStyle]
Edge = tuple[Node, Node, Label, NodeStyle]


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

class DPViewer(EasyPaint):
    current = 0

    def __init__(self, ledges: list[list[Edge]], lnodes: list[set[Node]], is_directed=True,
                 canvas_width: int = 400, canvas_height: int = 300, margin: int = 15,
                 axes_names=('', ''),
                 background='white',
                 node_size: Optional[float] = None,
                 titles=None,
                 swap: bool = False):
        super().__init__()
        self.node_size = node_size
        self.margin = margin
        self.ledges = ledges
        self.edges = ledges[self.current]
        self.lnodes = lnodes
        self.nodes = self.lnodes[self.current]
        self.titles = titles
        self.axes_names = axes_names
        self.swap = swap

        self.is_directed = is_directed

        self.num_x = len(set(p[0] for (p, _, _) in self.nodes))
        self.num_y = len(set(p[1] for (p, _, _) in self.nodes))

        self.min_x = min(p[0] for (p, _, _) in self.nodes)
        self.max_x = max(p[0] for (p, _, _) in self.nodes)

        self.min_y = min(p[1] for (p, _, _) in self.nodes)
        self.max_y = max(p[1] for (p, _, _) in self.nodes)

        self.title = 'Graph Viewer' if titles is None else titles[0]
        self.background = background
        self.size = canvas_width, canvas_height
        if self.swap:
            self.coordinates = (0, self.size[1], self.size[0], 0)

        w, h = self.size
        w -= self.margin
        h -= self.margin
        sizex = self.max_x - self.min_x + 1
        sizey = self.max_y - self.min_y + 1
        self.cell_size = cell_size = min(w / sizex, h / sizey)

        self.m = ((w - cell_size * sizex) / 2 - self.min_x * cell_size + self.margin / 2,
                  (h - cell_size * sizey) / 2 - self.min_y * cell_size + self.margin / 2)
        if self.node_size is None:
            self.node_size = (w * h / len(self.nodes)) ** 0.5 / 10  # cell_size / 8

    def on_key_press(self, keysym):
        if keysym in ['Return', 'Escape']:
            self.close()
        if keysym.upper() == 'SPACE':
            self.current = (self.current + 1) % len(self.ledges)
            self.edges = self.ledges[self.current]
            self.title = self.titles[self.current]
            self.erase('arrow')
            for edge in self.edges:
                self.draw_arrow(edge)
            self.nodes = self.lnodes[self.current]
            self.erase('vertex')
            for node in self.nodes:
                self.draw_vertex(node)
        if keysym.upper() == 'P':
            self.save_eps("saved.eps")

    def draw_arrow(self, edge, tag='arrow'):
        cell_size = self.cell_size
        m = self.m
        (u, _, _), (v, _, _), label, style = edge
        width = style.width

        if not self.is_directed:
            self.create_line((u[0] + 0.5) * cell_size + m[0], (u[1] + 0.5) * cell_size + m[1],
                             (v[0] + 0.5) * cell_size + m[0], (v[1] + 0.5) * cell_size + m[1])
        else:
            p1, p2 = find_intersec_point(v[0], v[1], (self.node_size + width + 2) / self.cell_size,
                                         u[0], u[1], v[0], v[1])
            _, (x2, y2) = min((dist(u, p1), p1), (dist(u, p2), p2))

            p1, p2 = find_intersec_point(u[0], u[1], (self.node_size + width + 2) / self.cell_size,
                                         v[0], v[1], u[0], u[1])
            _, (x1, y1) = min((dist(v, p1), p1), (dist(v, p2), p2))

            self._draw_arrow(x1, y1, x2, y2, label, style, tag=tag)

    def _draw_arrow(self, x1, y1, x2, y2, label, style, tag='arrow'):
        cell_size = self.cell_size
        m = self.m
        color = style.color
        width = style.width
        fs = style.fontsize
        pos = style.pos

        # x1, y1 = u
        l2 = self.node_size

        phi = 30 * pi / 180
        l1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        l2 /= (self.cell_size * 4)

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
        if pos >= 0:
            def x(t): return t * x1 + (1 - t) * x2

            def y(t): return t * y1 + (1 - t) * y2

            xm, ym = x(pos), y(pos)
            xr, yr = x2 - x1, y2 - y1
            a = atan2(yr, xr)

            ix = 0
            if abs(a) < 0.01 or abs(abs(a) - pi) < 0.01:
                anchor = 'S'
            elif abs(abs(a) - pi / 2) < 0.01:
                anchor = 'E'
                ix = 2
            elif 0 <= a <= pi / 2 or -pi <= a <= -pi / 2:
                anchor = 'SE' if not self.swap else 'SW'
            else:
                anchor = 'SW' if not self.swap else 'SE'

            self.create_text((xm + 0.5) * self.cell_size + self.m[0] - ix,
                             (ym + 0.5) * self.cell_size + self.m[1],
                             label, fs, color=color, anchor=anchor, tag=tag)

    def draw_vertex(self, node: Node, tag='vertex'):
        u, label, style = node
        fill = style.color
        width = style.width
        fs = style.fontsize
        self.create_filled_circle((u[0] + 0.5) * self.cell_size + self.m[0],
                                  (u[1] + 0.5) * self.cell_size + self.m[1],
                                  self.node_size, color='black', width=width, fill=fill, tag=tag)
        if label is not None:
            ls = label.split('\n')
            if len(ls) == 1:
                label = ls[0]
                self.create_text((u[0] + 0.5) * self.cell_size + self.m[0],
                                 (u[1] + 0.5) * self.cell_size + self.m[1],
                                 label, fs, color='black', tag=tag)
            if len(ls) == 2:
                label1, label2 = ls
                self.create_text((u[0] + 0.5) * self.cell_size + self.m[0],
                                 (u[1] + 0.5) * self.cell_size + self.m[1],
                                 label1, fs, anchor="S", color='black', tag=tag)
                self.create_text((u[0] + 0.5) * self.cell_size + self.m[0],
                                 (u[1] + 0.5) * self.cell_size + self.m[1] - 0.05 * self.cell_size,
                                 label2, fs, anchor="N", color='blue', tag=tag)

    def main(self):
        for edge in self.edges:
            self.draw_arrow(edge)
        for node in self.nodes:
            self.draw_vertex(node)

        arrow_style = EdgeStyle(color='black', fontsize=12, width=1, pos=0.5)
        if self.swap:
            lh, lv = self.axes_names[1], self.axes_names[0]
        else:
            lh, lv = self.axes_names[0], self.axes_names[1]
        kk = 2 * self.node_size / self.cell_size
        if lv != '':
            self._draw_arrow(-kk, 0, -kk, (self.size[1] - 2 * self.m[1]) / self.cell_size - 1, lv, arrow_style,
                             tag='axe')
        if lh != '':
            self._draw_arrow(0, -kk, (self.size[0] - 2 * self.m[0]) / self.cell_size - 1, -kk, lh, arrow_style,
                             tag='axe')


if __name__ == '__main__':
    node_style = NodeStyle(color='palegreen', width=1, fontsize=12)
    node_styleA = NodeStyle(color='pink', width=2, fontsize=12)
    arrow_style = EdgeStyle(color='black', width=1, fontsize=12, pos=0.5)
    arrow_style2 = EdgeStyle(color='blue', width=2, fontsize=12, pos=0.5)

    a = ((10, 1), 'A', node_styleA)
    b = ((15, 4), 'B', node_styleA)
    c = ((10, 7), 'C', node_style)
    d = ((20, 4), 'D', node_style)
    nodes = {a, b, c, d}

    edges = [(a, b, '7', arrow_style2), (c, a, '1', arrow_style), (b, d, '-2', arrow_style), (c, b, '4', arrow_style)]
    edges2 = [(b, a, '-7', arrow_style2), (a, c, '-1', arrow_style), (d, b, '2', arrow_style),
              (b, c, '-4', arrow_style)]

    viewer = DPViewer([edges, edges2], [nodes, nodes],
                      titles=["Grafo A (pulsa 'Space')", "Grafo B (pulsa 'Space')"],
                      canvas_width=400, canvas_height=300)
    viewer.run()
