import unittest
from algoritmia.algorithms.traverse import traverse_bf, traverse_df
from algoritmia.datastructures.graphs import Digraph
from random import seed


class TestTraversers(unittest.TestCase):
    def setUp(self):
        self.G = Digraph(E=[(0,1), (0,2), (1, 3), (2, 3), (3, 4), (5, 6)])
        seed(0)

    def test_breadth_first_traversal(self):
        self.assertTrue(tuple([v for (u,v) in traverse_bf(self.G, 0)]) in ((0, 1, 2, 3, 4), (0, 2, 1, 3, 4)))

    def test_recursive_preorder_traversal(self):
        self.assertTrue(tuple([v for (u,v) in traverse_df(self.G, 0)]) in ((0, 1, 3, 4, 2), (0, 2, 3, 4, 1)))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()