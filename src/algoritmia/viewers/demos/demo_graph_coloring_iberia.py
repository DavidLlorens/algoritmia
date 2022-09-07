from algoritmia.examples.greedy.graph_coloring_greedy import coloring_solve
from algoritmia.viewers.graph2d_viewer import Graph2dViewer

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]

if __name__ == '__main__':
    from algoritmia.data.iberia import iberia2d

    colors_set = list(coloring_solve(iberia2d))
    print(f"Solution with {len(colors_set)} colors.")
    colors = {}
    cols = ['red', 'green', 'blue', 'orange', 'yellow', 'brown', 'pink', 'black', 'white']
    if len(colors_set) > len(cols):
        raise Exception('Not enought colors')

    for i, s in enumerate(colors_set):
        for v in s:
            colors[v] = cols[i]

    gv = Graph2dViewer(iberia2d, canvas_width=800, canvas_height=800, vertexmode=Graph2dViewer.X_Y,
                       colors=colors, title=f"Graph coloring - {len(colors_set)} colors")
    gv.run()
