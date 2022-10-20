# coding: latin1

import unittest

from algoritmia.datastructures.graphs import (UndirectedGraph, Digraph,
                                              WeightingFunction)


class TestDigraphs(unittest.TestCase):
    def setUp(self):
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3), (3, 0), (0, 2), (0, 4), (0, 7)]
        self.g1 = Digraph(V=range(8), E=self.edges)
        self.g1bis = Digraph(E=self.edges)
        self.g1bis.add_vertex(6)
        edges = self.edges + [(1, 3)]
        self.g6 = UndirectedGraph(V=range(8), E=self.edges)
        self.g8 = Digraph(V=range(8), E=edges)

    def test_readonly(self):
        for g in self.g1, self.g1bis:
            self.assertEqual(len(g.V), 8)
            self.assertEqual(len(g.E), len(self.edges))
            for (u, v) in self.edges:
                self.assertTrue((u, v) in g.E)
            for u in g.V:
                succ = set(v for (uu, v) in self.edges if uu == u)
                pred = set(v for (v, uu) in self.edges if uu == u)
                self.assertEqual(succ, set(g.succs(u)))
                self.assertEqual(pred, set(g.preds(u)))
            self.assertFalse((0, 0) in g.E)

            self.assertEqual(g.out_degree(0), 5)
            self.assertEqual(g.in_degree(0), 2)

    def test_remove_self_loop(self):
        self.g8.remove_vertex(1)
        self.assertEqual(9, len(self.g8.E))

    def test_edit_edges(self):
        for g in self.g1, self.g1bis:
            self.assertFalse(1 in g.succs(7))
            self.assertFalse(7 in g.succs(1))
            self.assertFalse(7 in g.preds(1))
            self.assertFalse(1 in g.preds(7))
            g.add_edge((7, 1))
            self.assertEqual(len(g.E), len(self.edges) + 1)
            self.assertTrue((7, 1) in g.E)
            self.assertFalse((1, 7) in g.E)
            self.assertTrue(1 in g.succs(7))
            self.assertFalse(7 in g.succs(1))
            self.assertTrue(7 in g.preds(1))
            self.assertFalse(1 in g.preds(7))

            self.assertTrue(7 in g.succs(0))
            self.assertFalse(0 in g.succs(7))
            self.assertTrue(0 in g.preds(7))
            self.assertFalse(7 in g.preds(0))
            g.remove_edge((0, 7))
            self.assertFalse((0, 7) in g.E)
            self.assertEqual(len(g.E), len(self.edges))
            self.assertFalse(0 in g.succs(7))
            self.assertFalse(7 in g.succs(0))
            self.assertFalse(7 in g.preds(0))
            self.assertFalse(0 in g.preds(7))

    def test_edit_vertices(self):
        for g in self.g1, self.g1bis:
            g.add_vertex(6)
            self.assertTrue(6 in g.V)
            self.assertFalse((0, 6) in g.E)
            self.assertFalse(0 in g.succs(6))
            self.assertFalse((6, 0) in g.E)
            self.assertFalse(6 in g.succs(0))

            if g == self.g6:  # Por cobertura
                g.add_vertex(10)

            g.remove_vertex(0)
            self.assertFalse((1, 0) in g.E)
            self.assertFalse((0, 1) in g.E)
            self.assertFalse(0 in set(s for v in g.V for s in g.succs(v)))
            self.assertFalse(0 in set(s for v in g.V for s in g.preds(v)))

    def test_contains(self):
        for g in self.g1, self.g1bis:
            self.assertFalse(g.contains_edge((7, 1)))
            self.assertFalse(g.contains_edge((1, 7)))
            g.add_edge((7, 1))
            self.assertTrue(g.contains_edge((7, 1)))
            self.assertFalse(g.contains_edge((1, 7)))

class TestUndirectedGraph(unittest.TestCase):
    def setUp(self):
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3), (0, 2), (0, 4), (0, 7)]
        self.undirected_edges = set()
        for (u, v) in self.edges:
            self.undirected_edges.add((u, v))
            self.undirected_edges.add((v, u))
        self.g1 = UndirectedGraph(V=range(8), E=self.edges)
        self.g1bis = UndirectedGraph(E=self.edges)
        self.g1bis.add_vertex(6)
        self.g6 = UndirectedGraph(V=range(8), E=self.edges)
        self.g7 = UndirectedGraph(V=range(8), E=self.edges)

    def test_V_contains(self):
        for g in self.g1, self.g1bis:
            for i in range(8):
                self.assertTrue(i in g.V)
                self.assertFalse(8 + i in g.V)

    def test_E_contains(self):
        for g in self.g1, self.g1bis:
            for (u, v) in self.edges:
                self.assertTrue((u, v) in g.E or (v, u) in g.E)
                self.assertFalse((u, v + 8) in g.E)
                self.assertFalse((u + 8, v) in g.E)

    def test_remove_vertex(self):
        self.g7.remove_vertex(0)
        self.assertEqual(4, len(self.g7.E))

    def test_V_len(self):
        for g in self.g1, self.g1bis:
            self.assertEqual(len(g.V), 8)

    def test_E_len(self):
        for g in self.g1, self.g1bis:
            self.assertEqual(len(g.E), 10)

    def test_V_repr(self):
        for g in self.g1, self.g1bis:
            self.assertEqual(set(g.V), set(eval(repr(g.V))))

    def test_E_repr(self):
        for g in self.g1, self.g1bis:
            self.assertEqual(set(g.E), set(eval(repr(g.E))))

    def test_succs_and_preds(self):
        for g in self.g1, self.g1bis:
            for u in g.V:
                succ = set(v for (uu, v) in self.undirected_edges if uu == u)
                pred = set(v for (v, uu) in self.undirected_edges if uu == u)
                self.assertEqual(succ, set(g.succs(u)))
                self.assertEqual(pred, set(g.preds(u)))

    def test_out_degree(self):
        for g in self.g1, self.g1bis:
            self.assertEqual(g.out_degree(0), 6)
            for v in g.V:
                self.assertEqual(g.out_degree(v), g.in_degree(v))

    def test_repr(self):
        for g in self.g1, self.g1bis:
            gg = eval(repr(g))
            self.assertEqual(set(g.V), set(gg.V))
            self.assertEqual(set(g.E), set(gg.E))

    def test_edit_edges(self):
        for g in self.g1, self.g1bis:
            g.add_edge((7, 1))
            # self.assertEqual(len(g.E), len(self.undirected_edges)+2)
            self.assertTrue((7, 1) in g.E)
            # self.assertTrue((1,7) in g.E)
            self.assertTrue(7 in g.succs(1))
            self.assertTrue(1 in g.succs(7))
            self.assertTrue(7 in g.preds(1))
            self.assertTrue(1 in g.preds(7))


            g.remove_edge((0, 7))
            # self.assertFalse((7,0) in g.E)
            self.assertFalse((0, 7) in g.E)
            self.assertFalse(7 in g.succs(0))
            self.assertFalse(0 in g.succs(7))
            self.assertFalse(7 in g.preds(0))
            self.assertFalse(0 in g.preds(7))

            g.add_edge((1, 3))
            self.assertTrue((1, 3) in g.E)
            # self.assertTrue((3,1) in g.E)
            self.assertTrue(1 in g.succs(3))
            self.assertTrue(3 in g.succs(1))
            self.assertTrue(1 in g.preds(3))
            self.assertTrue(3 in g.preds(1))

    def test_edit_vertices(self):
        for g in self.g1, self.g1bis:
            g.add_vertex(6)
            self.assertTrue(6 in g.V)
            self.assertFalse((0, 6) in g.E)
            self.assertFalse(0 in g.succs(6))
            self.assertFalse((6, 0) in g.E)
            self.assertFalse(6 in g.succs(0))

            if g == self.g6:  # Por cobertura
                g.add_vertex(10)

            g.remove_vertex(0)
            self.assertFalse((1, 0) in g.E)
            self.assertFalse((0, 1) in g.E)
            self.assertFalse(0 in set(s for v in g.V for s in g.succs(v)))
            self.assertFalse(0 in set(s for v in g.V for s in g.preds(v)))

    def test_contains(self):
        for g in self.g1, self.g1bis:
            self.assertFalse(g.contains_edge((7, 1)))
            self.assertFalse(g.contains_edge((1, 7)))
            g.add_edge((7, 1))
            self.assertTrue(g.contains_edge((7, 1)))
            self.assertTrue(g.contains_edge((1, 7)))

class TestRedimDigraphs(unittest.TestCase):
    def setUp(self):
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3), (3, 0), (0, 2), (0, 4), (0, 7)]
        self.g = Digraph(V=range(8), E=self.edges)

    def test_edit_edges(self):
        for g in [self.g]:
            g.add_edge((7, 1))
            self.assertEqual(len(g.E), len(self.edges) + 1)
            self.assertTrue((7, 1) in g.E)
            self.assertFalse((1, 7) in g.E)

            g.remove_edge((0, 7))
            self.assertFalse((7, 0) in g.E)
            self.assertFalse((0, 7) in g.E)

            g.add_edge((12, 1))
            self.assertTrue((12, 1) in g.E)
            self.assertFalse((1, 12) in g.E)

            g.add_edge((1, 12))
            self.assertTrue((1, 12) in g.E)


class TestWeightingFunction(unittest.TestCase):
    def setUp(self):
        self.sym = WeightingFunction([((0, 0), 1), ((1, 1), 2), ((1, 2), 3)], symmetrical=True)
        self.sym_d = WeightingFunction({(0, 0): 1, (1, 1): 2, (1, 2): 3}, symmetrical=True)
        self.asym = WeightingFunction([((0, 0), 1), ((1, 1), 2), ((1, 2), 3)], symmetrical=False)
        self.asym_d = WeightingFunction({(0, 0): 1, (1, 1): 2, (1, 2): 3}, symmetrical=False)
        self.rep = WeightingFunction([((0, 1), 10), ((0, 2), 2), ((1, 0), 10)], symmetrical=True)

    def test_getitem(self):
        for wf in [self.sym, self.sym_d]:
            self.assertEqual(wf(0, 0), 1)
            self.assertEqual(wf(1, 1), 2)
            self.assertEqual(wf(1, 2), 3)
            self.assertEqual(wf(2, 1), 3)
        for wf in [self.asym, self.asym_d]:
            self.assertEqual(wf(0, 0), 1)
            self.assertEqual(wf(1, 1), 2)
            self.assertEqual(wf(1, 2), 3)
            self.assertRaises(KeyError, wf.__call__, (2, 1))
            self.assertRaises(KeyError, wf.__call__, (2, 1))

        self.assertRaises(ValueError, WeightingFunction, *[[((0, 1), 1), ((0, 2), 2), ((1, 0), 3)], True])
        self.assertEqual(self.rep(0, 1), 10)
        self.assertEqual(self.rep(1, 0), 10)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
