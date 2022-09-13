from math import sin, cos, pi, sqrt
from typing import *
from enum import Enum
import tkinter

from algoritmia.datastructures.graphs import Digraph
from easypaint import EasyPaint

Num = Union[int, float]
Vertex = tuple[Num, Num]
Score = int
Decision = str

infinity = float('infinity')


class RecMode(Enum):
    Classic = 0
    Optimized = 1


# -------------------------------------------------------------------------------------


def run(s: str, t: str, sol: list[Decision]) -> str:
    n = 0
    res = list(s)
    p = 0
    for d in sol:
        if d == 'I':
            res.insert(p, t[n])
            n += 1
            p += 1
        elif d == 'D':
            del res[p]
        else:
            if d == 'S':
                res[p] = t[n]
            p += 1
            n += 1
    res.insert(p, '|')
    return ''.join(res)

Trellis = dict[Vertex, tuple[str, Score, Decision]]

def edit_distance(mode: RecMode, s: str, t: str) -> tuple[Digraph, Trellis, list[Vertex]]:
    LParams = tuple[int, int]

    def D_clasic(m: int, n: int) -> Score:
        if m == 0 and n == 0:
            return 0
        if (m, n) not in mem:
            if n == 0:
                mem[m, n] = D_clasic(m - 1, n) + 1, (m - 1, n), 'D'
            elif m == 0:
                mem[m, n] = D_clasic(m, n - 1) + 1, (m, n - 1), 'I'
            else:
                c, d = (0, '-') if s[m - 1] == t[n - 1] else (1, 'S')
                mem[m, n] = min((D_clasic(m - 1, n) + 1, (m - 1, n), 'D'),
                                (D_clasic(m, n - 1) + 1, (m, n - 1), 'I'),
                                (D_clasic(m - 1, n - 1) + c, (m - 1, n - 1), d))
        return mem[m, n][0]

    def D_opt(m: int, n: int) -> Score:
        if m == 0 and n == 0:
            return 0
        if (m, n) not in mem:
            if n == 0:
                mem[m, n] = D_clasic(m - 1, n) + 1, (m - 1, n), 'D'
            elif m == 0:
                mem[m, n] = D_clasic(m, n - 1) + 1, (m, n - 1), 'I'
            else:
                if s[m - 1] == t[n - 1]:
                    mem[m, n] = D_clasic(m - 1, n - 1), (m - 1, n - 1), '-'
                else:
                    mem[m, n] = min((D_clasic(m - 1, n) + 1, (m - 1, n), 'D'),
                                    (D_clasic(m, n - 1) + 1, (m, n - 1), 'I'),
                                    (D_clasic(m - 1, n - 1) + 1, (m - 1, n - 1), 'S'))
        return mem[m, n][0]

    def path_from(m, n) -> tuple[list[Decision], list[Vertex]]:
        sol = []
        path = [(m, n)]
        while (m, n) != (0, 0):
            _, (m, n), dec = mem[m, n]
            sol.append(dec)
            path.append((m, n))
        sol.reverse()
        return sol, path

    mem: dict[LParams, tuple[Score, LParams, Decision]] = {}
    if mode == RecMode.Classic:
        D_clasic(len(s), len(t))
    else:
        D_opt(len(s), len(t))

    sol, path = path_from(len(s), len(t))

    e = []
    names2 = {}
    p = 0
    for n in range(len(t) + 1):
        if n == 0:
            names2[0, 0] = list(s)
            p = 0
        else:
            a = names2[0, n - 1][:]
            a.insert(p, t[n - 1])
            p += 1
            names2[0, n] = a
        for m in range(1, len(s) + 1):
            a = names2[m - 1, n][:]
            del a[p]
            # p -= 1
            names2[m, n] = a

    names = {}
    if mode == RecMode.Optimized:
        for (m, n) in names2:
            k = m, n
            names2[k].insert(n, '|')
            names[k] = ''.join(names2[k]), infinity, None

    for m in range(len(s) + 1):
        for n in range(len(t) + 1):
            if (m, n) == (0, 0):
                names[m, n] = '|' + s, 0, None
            else:
                if (m, n) in mem:
                    score, (mp, np), decision = mem[m, n]
                    e.append(((mp, np), (m, n)))
                    names[m, n] = run(s, t, path_from(m, n)[0]), score, decision
    return Digraph(E=e), names, path


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

class ViewMode(Enum):
    X_Y = 0
    ROW_COL = 1


class TextMode(Enum):
    Cursor = 0
    D = 1
    Score = 2


class ArrowMode(Enum):
    BackPointers = 0
    Dependecies = 1


class EditDistanceViewer(EasyPaint):
    def __init__(self, mode: RecMode, source: str, target: str,
                 canvas_width: int = 400, canvas_height: int = 300,
                 margin: int = 15, vertexmode: ViewMode = ViewMode.X_Y,
                 background: str = 'white', node_size: Optional[float] = None,
                 colors: Optional[dict[Vertex, str]] = None):

        g, names, path = edit_distance(my_mode, my_source, my_target)
        self.node_size = node_size
        self.margin = margin
        self.colors = colors if colors is not None else {}
        self.rec_mode = mode
        self.names = names
        self.path = path
        self.source = source
        self.target = target
        self.text_mode = TextMode.Cursor
        self.arrow_mode = ArrowMode.Dependecies
        if not isinstance(g, Digraph) or \
                any([not isinstance(p, tuple) or len(p) != 2 or
                     not isinstance(p[0], int) and not isinstance(p[0], float) or
                     not isinstance(p[1], int) and not isinstance(p[1], float) for p in g.V]):
            raise TypeError("The graph must be an UndirectedGraph. Vertices must be tuples of two integers or floats")

        if vertexmode == ViewMode.ROW_COL:
            if any([not isinstance(p[0], int) for p in g.V]):
                raise TypeError("In this mode, vertices must be tuples of two integers")
            g = Digraph(V=[(v[1], -v[0]) for v in g.V], E=[((u[1], -u[0]), (v[1], -v[0])) for (u, v) in g.E])
            path2 = [(v, -u) for (u, v) in self.path]
            self.path = path2
            names2 = dict(((v, -u), vv) for ((u, v), vv) in self.names.items())
            self.names = names2

        self.g = g

        self.max_y = max(p[1] for p in self.g.V)
        self.max_x = max(p[0] for p in self.g.V)
        self.min_y = min(p[1] for p in self.g.V)
        self.min_x = min(p[0] for p in self.g.V)

        super().__init__()
        self.easypaint_configure(title=f'Edit Distance Viewer  [{self.rec_mode}]',
                                 background=background,
                                 size=(canvas_width, canvas_height))

        w, h = self.size
        w -= self.margin
        h -= self.margin
        sizex = self.max_x - self.min_x + 1
        sizey = self.max_y - self.min_y + 1
        cell_size = self.cell_size = min(w / sizex, h / sizey)

        self.m = ((w - cell_size * sizex) / 2 - self.min_x * cell_size + self.margin / 2,
                  (h - cell_size * sizey) / 2 - self.min_y * cell_size + self.margin / 2)
        if self.node_size is None:
            self.node_size = 50  # (w * h / len(self.g.V)) ** 0.5 / 12  # cell_size / 8

    def draw_arrow(self, x1, y1, x2, y2, l2, color='black', width=1, tag='arrow'):
        phi = 30 * pi / 180
        l1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        cell_size = self.cell_size
        m = self.m

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

    def draw_vertex_text_aux(self, u: Vertex):
        if u not in self.names: return
        if self.text_mode == TextMode.Cursor:
            msg, fs = self.names[u][0], 12
        elif self.text_mode == TextMode.D:
            msg, fs = f'D({u[0]},{u[1]})', 12
        else:
            msg, fs = f'{self.names[u][1]}', 18
        self.create_text((u[0] + 0.5) * self.cell_size + self.m[0],
                         (u[1] + 0.5) * self.cell_size + self.m[1],
                         msg, fs, tag='text')
        if self.text_mode != TextMode.Score and self.arrow_mode == ArrowMode.BackPointers:
            self.create_text((u[0] + 0.5) * self.cell_size + self.m[0],
                             (u[1] + 0.35) * self.cell_size + self.m[1],
                             f'{self.names[u][1]}', 10, tag='text')

    def draw_vertex_text(self):
        if self.node_size > 0:
            self.erase('text')
            if self.arrow_mode == ArrowMode.BackPointers:
                for u in self.g.V:
                    self.draw_vertex_text_aux(u)
            else:
                for m in range(len(self.source) + 1):
                    for n in range(len(self.target) + 1):
                        u = m, n
                        self.draw_vertex_text_aux(u)

    def draw_vertex(self):
        if self.node_size > 0:
            self.erase('vertex')
            if self.arrow_mode == ArrowMode.BackPointers:
                for u in self.g.V:
                    width = 4 if u in self.path else 1
                    self.create_filled_circle((u[0] + 0.5) * self.cell_size + self.m[0],
                                              (u[1] + 0.5) * self.cell_size + self.m[1],
                                              self.node_size, fill='gray95', width=width, tag='vertex')
            else:
                width = 1
                for m in range(len(self.source) + 1):
                    for n in range(len(self.target) + 1):
                        u = m, n
                        self.create_filled_circle((u[0] + 0.5) * self.cell_size + self.m[0],
                                                  (u[1] + 0.5) * self.cell_size + self.m[1],
                                                  self.node_size, fill='gray95', width=width, tag='vertex')
                # x1 = (u[0] + 0.5) * cell_size + m[0]
                # y1 = (u[1] + 0.5) * cell_size + m[1]
                # w = self.node_size
                # h = self.node_size*0.25
                # self.create_filled_rectangle(x1-w, y1-h, x1+w, y1+h,
                #                              fill='palegreen')

    def draw_arrows(self):
        self.erase('arrow')
        for u, v in self.g.E:
            if self.arrow_mode == ArrowMode.BackPointers:
                width = 4 if v in self.path else 1
                u, v = v, u
                p1, p2 = find_intersec_point(v[0], v[1], (self.node_size + width) / self.cell_size, u[0], u[1], v[0],
                                             v[1])
                _, (x, y) = min((dist(u, p1), p1), (dist(u, p2), p2))
                color = 'blue' if self.names[u][2] == '-' else 'red'
                self.draw_arrow(u[0], u[1], x, y, 0.1, color, width=width, tag='arrow')
            else:
                width = 0
                for m in range(len(self.source) + 1):
                    for n in range(len(self.target) + 1):
                        v = m, n
                        for ix, iy in [(-1, -1), (-1, 0), (0, -1)]:
                            u = v[0] + ix, v[1] + iy
                            if u[0] < 0 or u[1] < 0: continue
                            p1, p2 = find_intersec_point(v[0], v[1], (self.node_size + width) / self.cell_size,
                                                         u[0], u[1], v[0], v[1])
                            _, (x, y) = min((dist(u, p1), p1), (dist(u, p2), p2))
                            color = 'blue' if (ix, iy) == (-1, -1) and self.source[m - 1] == self.target[
                                n - 1] else 'red'
                            self.draw_arrow(u[0], u[1], x, y, 0.1, color, width=width, tag='arrow')
                            if self.rec_mode == RecMode.Optimized and color == 'blue':
                                break  # a 'blue' arrow forbids 'red' brothers
            self.tag_lower('arrow')

    def draw_labels(self):
        for m in range(0, len(self.source)):
            self.create_text((m + 1) * self.cell_size + self.m[0],
                             0.1 * self.cell_size + self.m[1], self.source[m], 22)
        for n in range(0, len(self.target)):
            self.create_text(0.1 * self.cell_size + self.m[0],
                             (n + 1) * self.cell_size + self.m[1], self.target[n], 22)

    def on_key_press(self, keysym):
        if keysym.lower() in ['return', 'escape']:
            self.close()
            return
        if keysym.lower() == 'p':  # photo
            self.save_eps('edit_distance.eps')
            return

        if keysym.lower() == 't':
            if self.text_mode == TextMode.Cursor:
                self.text_mode = TextMode.D
            elif self.text_mode == TextMode.D:
                self.text_mode = TextMode.Score
            else:
                self.text_mode = TextMode.Cursor
        elif keysym.lower() == 'a':
            if self.arrow_mode == ArrowMode.BackPointers:
                self.arrow_mode = ArrowMode.Dependecies
            else:
                self.arrow_mode = ArrowMode.BackPointers
        self.draw_arrows()
        self.draw_vertex()
        self.draw_vertex_text()
        self.tag_raise('text')

    def main(self):
        self.draw_arrows()
        self.draw_vertex()
        self.draw_vertex_text()
        self.draw_labels()


# -------------------------------------------------------------------------------------


if __name__ == '__main__':
    my_mode = RecMode.Classic
    my_source, my_target = 'costa', 'casa'

    viewer = EditDistanceViewer(my_mode, my_source, my_target,
                                canvas_width=1000, canvas_height=800, vertexmode=ViewMode.X_Y)
    viewer.run()
