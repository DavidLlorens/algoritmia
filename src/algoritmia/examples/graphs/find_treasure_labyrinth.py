from typing import *

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo

Vertex = tuple[int, int]


def find_treasure_breadthfirst(g: UndirectedGraph, v_start: Vertex, v_treasure: Vertex) -> Optional[Vertex]:
    queue = Fifo()
    seen = set()
    queue.push(v_start)
    seen.add(v_start)
    while len(queue) > 0:
        v = queue.pop()
        if v == v_treasure:
            return v
        for suc in g.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push(suc)
    return None


def find_treasure_depthfirst(g: UndirectedGraph, v_start: Vertex, v_treasure: Vertex) -> Optional[Vertex]:
    def explorar_desde(v):
        seen.add(v)
        if v == v_treasure:  # preorder
            return v  # preorder
        for suc in g.succs(v):
            if suc not in seen:
                res = explorar_desde(suc)
                if res is not None:
                    return res
        # if v == v_treasure:    # postorder
        #    return v           # postorder

    seen = set()
    return explorar_desde(v_start)


# Main program -------------------------------------------------------------------------

corridors = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)), ((0, 1), (0, 2)),
             ((2, 0), (1, 0)), ((2, 1), (2, 2)), ((2, 2), (2, 3)), ((0, 1), (1, 1)),
             ((0, 2), (1, 2)), ((0, 3), (1, 3)), ((1, 1), (2, 1)), ((1, 2), (2, 2))]
labyrinth = UndirectedGraph(E=corridors)

pos_start = (0, 0)
pos_treasure = (1, 3)

# room = find_treasure_breadthfirst(labyrinth, pos_start, pos_treasure)
room = find_treasure_depthfirst(labyrinth, pos_start, pos_treasure)

if room is None:
    print('Treasure not found.')
else:
    print(f'Treasure found on room {room}.')
