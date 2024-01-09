from algoritmia.datastructures.graphs import Digraph


# Ordenación topológica de un digrafo acíclico
# Si el grafo tiene algún ciclo, el algoritmo lanza una excepción
def topological_sort[T](g: Digraph[T]) -> list[T]:
    def traverse_from(v: T, used: set[T]):
        seen.add(v)
        for suc_v in g.succs(v):
            if suc_v in used:  # Cycle detection
                raise Exception("The graph has at least one cycle")
            used.add(suc_v)  # Cycle detection
            if suc_v not in seen:
                traverse_from(suc_v, used)
            used.remove(suc_v)  # Cycle detection
        lv.append(v)

    lv = []
    seen = set()
    for v in g.V:
        if len(g.preds(v)) == 0:
            traverse_from(v, set())
    lv.reverse()
    return lv


if __name__ == '__main__':
    edges = [('C', 'C++'), ('C', 'Java'), ('C', 'Objective-C'), ('C', 'C#'),
             ('C++', 'Java'), ('C++', 'C#'), ('Java', 'C#'),
             ('MT', 'Haskell'), ('Haskell', 'C#')]
    my_graph = Digraph(E=edges)
    print(topological_sort(my_graph))
