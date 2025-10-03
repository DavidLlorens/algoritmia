from algoritmia.datastructures.graphs import UndirectedGraph

if __name__ == "__main__":
    edges = [('Castelló', 'Sagunt'), ('Sagunt', 'València')]

    ugraph = UndirectedGraph(E=edges)  # Parameter V is optional
    print(ugraph.V)  # Output: {'Sagunt', 'València', 'Castelló'}
    print(ugraph.succs('Sagunt'))  # Output: {'València', 'Castelló'}
