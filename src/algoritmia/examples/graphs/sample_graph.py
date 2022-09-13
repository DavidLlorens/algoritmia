from algoritmia.datastructures.graphs import UndirectedGraph

edges = [('Castelló', 'Sagunt'), ('Sagunt', 'València')]
ug = UndirectedGraph(E=edges)    # Parameter V is optional
print(ug.V)                      # Output: {'Sagunt', 'València', 'Castelló'}
print(ug.succs('Sagunt'))        # Output: {'València', 'Castelló'}
