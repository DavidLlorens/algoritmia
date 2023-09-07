import unittest
from algoritmia.algorithms.topological_sort import topological_sort
from algoritmia.datastructures.graphs import Digraph

class TestTopsorter(unittest.TestCase):
    def test_topsort(self):
        G = Digraph(E=[(0,1), (1,2), (2,3), (3,4), (4,5)])
        self.assertEqual(tuple(topological_sort(G)), tuple(range(6)))
        self.assertEqual(tuple(topological_sort(G)), tuple(range(6)))
        G = Digraph(E=[('C', 'C++'), ('C', 'Objective C'), ('C', 'Java'), ('C', 'C#'),
                       ('C++', 'C#'), ('C++', 'Java'),
                       ('Java', 'C#')])
        ts = tuple(topological_sort(G))
        print(ts)
        for (u,v) in G.E:
            self.assertTrue(ts.index(u) < ts.index(v))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()