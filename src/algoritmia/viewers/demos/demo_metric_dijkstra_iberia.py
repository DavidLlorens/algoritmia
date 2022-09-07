from algoritmia.viewers.graph2d_viewer import Graph2dViewer
from algoritmia.algorithms.traversers import dijkstra_edge_traverser, dijkstra_metric_edge_traverser
from algoritmia.data.iberia import iberia2d, km2d, coords2d

if __name__ == '__main__':
    v_initial = coords2d["Madrid"]
    v_final = coords2d["Bilbao"]

    edges = dijkstra_edge_traverser(iberia2d, km2d, v_initial)
    # edges = dijkstra_metric_edge_traverser(iberia2d, km2d, v_initial, v_final)
    colors = {}
    for (u, v) in edges:
        colors[v] = 'red'
        if v == v_final: break
    colors[v_initial] = 'palegreen'
    colors[v_final] = 'palegreen'

    gv = Graph2dViewer(iberia2d, canvas_width=800, canvas_height=800, vertexmode=Graph2dViewer.X_Y, colors=colors)
    gv.run()
