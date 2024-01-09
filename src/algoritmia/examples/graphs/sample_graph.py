from algoritmia.datastructures.graphs import UndirectedGraph

edges = [('Castelló', 'Sagunt'), ('Sagunt', 'València')]

ugraph = UndirectedGraph(E=edges)  # Parameter V is optional
print(ugraph.V)  # Output: {'Sagunt', 'València', 'Castelló'}
print(ugraph.succs('Sagunt'))  # Output: {'València', 'Castelló'}
