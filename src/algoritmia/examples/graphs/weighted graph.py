from algoritmia.datastructures.graphs import UndirectedGraph, WeightingFunction

weighted_edges = {('Castelló', 'Sagunt'): 43, ('Sagunt', 'València'): 50}

wf = WeightingFunction(weighted_edges, symmetrical=True)
road_graph = UndirectedGraph(E=weighted_edges.keys())

print(wf('Castelló', 'Sagunt'))  # Output: 43
