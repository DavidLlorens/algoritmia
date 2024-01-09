from algoritmia.algorithms.traverse import traverse_dijkstra_dict, traverse_dijkstra_metric_dict
from algoritmia.data.iberia import iberia, km, coords2d, iberia2d
from algoritmia.viewers.graph2d_viewer import Graph2dViewer


def dist(city_a: str, city_b: str) -> float:
    coords_a, coords_b = coords2d[city_a], coords2d[city_b]
    dx, dy = coords_a[0] - coords_b[0], coords_a[1] - coords_b[1]
    return (dx * dx + dy * dy) ** 0.5


if __name__ == '__main__':
    v_initial = 'Madrid'
    v_final = 'Bilbao'
    edges = traverse_dijkstra_dict(iberia, km, v_initial)
    # edges = traverse_dijkstra_metric_dict(iberia, km, dist,v_initial, v_final)
    colors = {}
    for (c1, c2) in edges:
        c1_pos = coords2d[c1]
        c2_pos = coords2d[c2]
        colors[c2_pos] = 'red'
        if c2 == v_final: break
    colors[coords2d[v_initial]] = colors[coords2d[v_final]] = 'palegreen'

    gv = Graph2dViewer(iberia2d, canvas_width=800, canvas_height=800, vertexmode=Graph2dViewer.X_Y, colors=colors)
    gv.run()
