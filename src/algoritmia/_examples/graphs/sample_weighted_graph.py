from algoritmia.datastructures.graphs import UndirectedGraph, WeightingFunction

if __name__ == "__main__":
    weighted_edges = {('Castelló', 'Sagunt'): 43, ('Sagunt', 'València'): 50}

    # Construimos la función de pesos a partir del diccionario anterior
    wf = WeightingFunction(weighted_edges, symmetrical=True)
    # Ejemplos de uso:
    print(wf('Castelló', 'Sagunt'))  # Output: 43
    print(wf('Sagunt', 'Castelló'))  # Output: 43 (al utilizar 'symmetrical=True')

    # Podemos aprovechar las claves del diccionario para crear el grafo
    road_graph = UndirectedGraph(E=weighted_edges.keys())

    # Podemos considerar un grafo de carreteras con distancias (pesos en las aristas) como una tupla
    weighted_road_graph = (road_graph, wf)
