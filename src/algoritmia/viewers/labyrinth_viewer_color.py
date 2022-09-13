"""
2021-10-22: Versión 1
@author: David Llorens (dllorens@uji.es)

Hereda de la clase LabyrinthViewer para añadir animación de color.
Se anima el color de los vértices según apareren en la lista marked_cells (en ese el órden).
"""
from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]
Path = list[Vertex]


class LabyrinthViewerColor(LabyrinthViewer):
    def __init__(self, lab: UndirectedGraph,
                 canvas_width: int = 400, canvas_height: int = 400,
                 margin: int = 10, wall_width: int = 2):
        LabyrinthViewer.__init__(self, lab, canvas_width, canvas_height, margin, wall_width)
        self.state = 0
        self.vertex_painted_per_iteration = 20
        self.tt = None

    def on_key_press(self, keysym):
        if keysym != 'Return': return
        if self.state == 0:
            self.state = 1
            self.erase(self.tt)
            self.after(0, lambda: self.anim(0, len(self.marked_cells)))
        elif self.state == 1:
            self.close()

    def anim(self, pos, max_pos):
        mw = self.mw
        mh = self.mh
        i = pos
        while i < min(max_pos, pos + self.vertex_painted_per_iteration):
            cell, color = self.marked_cells[i]
            cx = mw / 2 + cell[1] * self.cell_size + self.cell_size / 2
            cy = mh / 2 + cell[0] * self.cell_size + self.cell_size / 2
            tt = self.create_filled_rectangle(cx - self.cell_size / 2, cy - self.cell_size / 2,
                                              cx + self.cell_size / 2, cy + self.cell_size / 2,
                                              'black', color, width=0)
            self.tag_lower(tt)
            i += 1
        self.update()
        if i < max_pos:
            self.after(0, lambda: self.anim(i, len(self.marked_cells)))

    def main(self):
        self.easypaint_configure(title='Labyrinth Viewer (colored cells)',
                                 background='white',
                                 size=(self.canvas_width, self.canvas_height),
                                 coordinates=(0, self.canvas_height, self.canvas_width, 0))
        self.draw_lab()
        w, h = self.center
        self.tt = self.create_text(w, h, "Press 'Return' to colorize", 14, "C", "red")


if __name__ == '__main__':
    import colorsys
    from algoritmia.datastructures.queues import Fifo


    def int2col(n: int, maxint: int = 255) -> str:
        (r, g, b) = colorsys.hsv_to_rgb(float(n) / maxint * (300 / 360.0), 1.0, 1.0)
        return "#{:02x}{:02x}{:02x}".format(int(255 * r), int(255 * g), int(255 * b))


    def matriz_distancias_anchura(grafo: UndirectedGraph, v_inicial: Vertex) -> dict[Vertex, int]:
        dist: dict[Vertex, int] = {}
        queue = Fifo()
        seen: set[Vertex] = set()
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


    e = [((4, 7), (4, 6)), ((4, 7), (4, 8)), ((1, 3), (0, 3)), ((1, 3), (1, 4)), ((4, 8), (4, 9)), ((3, 0), (2, 0)),
         ((3, 0), (4, 0)), ((2, 8), (2, 7)), ((2, 8), (1, 8)), ((2, 1), (2, 0)), ((2, 1), (2, 2)), ((0, 0), (1, 0)),
         ((1, 6), (1, 5)), ((1, 6), (2, 6)), ((3, 7), (3, 8)), ((3, 7), (3, 6)), ((2, 5), (1, 5)), ((2, 5), (2, 4)),
         ((0, 3), (0, 2)), ((4, 0), (4, 1)), ((1, 2), (0, 2)), ((1, 2), (1, 1)), ((4, 9), (3, 9)), ((3, 3), (2, 3)),
         ((3, 3), (4, 3)), ((2, 9), (3, 9)), ((2, 9), (1, 9)), ((4, 4), (3, 4)), ((4, 4), (4, 3)), ((3, 6), (3, 5)),
         ((2, 2), (3, 2)), ((4, 1), (4, 2)), ((1, 1), (1, 0)), ((0, 1), (0, 2)), ((3, 2), (3, 1)), ((2, 6), (2, 7)),
         ((4, 5), (4, 6)), ((0, 4), (0, 5)), ((0, 4), (1, 4)), ((3, 9), (3, 8)), ((0, 5), (0, 6)), ((0, 7), (0, 6)),
         ((0, 7), (1, 7)), ((4, 2), (4, 3)), ((0, 8), (0, 9)), ((3, 5), (3, 4)), ((1, 8), (1, 7)), ((0, 9), (1, 9)),
         ((2, 3), (2, 4))]

    g = UndirectedGraph(E=e)
    num_rows, num_cols = max(v[0] for v in g.V)+1, max(v[1] for v in g.V)+1
    cell_size = 40
    margin = 10

    # Laberinto en forma de grafo no dirigido

    lv = LabyrinthViewerColor(g,
                              canvas_width=num_cols * cell_size + margin * 2,
                              canvas_height=num_rows * cell_size + margin * 2, margin=margin)

    start = (0, 0)  # (num_rows//2, num_cols//2)
    matriz_dist = matriz_distancias_anchura(g, start)
    maxvalue = max(matriz_dist.values())
    for (v, k) in sorted([(v, k) for (k, v) in matriz_dist.items()]):
        lv.add_marked_cell(k, int2col(v, maxvalue))

    lv.run()
