from algoritmia.algorithms.mst import kruskal, prim
from algoritmia.data.iberia import iberia2d, km2d
from algoritmia.viewers.graph2d_mst_viewer import Graph2dMstViewer

# g_msf = kruskal(iberia2d, km2d)
g_msf = prim(iberia2d, km2d)

gv = Graph2dMstViewer(iberia2d, g_msf, canvas_width=800, canvas_height=800, margin=50)
gv.run()
