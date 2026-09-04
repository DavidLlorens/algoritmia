# coding: latin1

import unittest

from algoritmia.datastructures.mergefindsets import MergeFindSet


class TestMFset(unittest.TestCase):
    def setUp(self):
        self.mf1 = MergeFindSet()
        self.mf2 = MergeFindSet(((i,) for i in range(10)))

    def test_mfsets(self):
        for i in range(10):
            self.mf1.add(i)
        for i in range(10):
            self.assertEqual(self.mf1.find(i), i)
            self.assertEqual(self.mf2.find(i), i)
        for i in range(0, 10, 2):
            self.mf1.merge(i, i + 1)
            self.mf2.merge(i, i + 1)
        for i in range(0, 10, 2):
            self.assertEqual(self.mf1.find(i), self.mf1.find(i + 1))
            self.assertEqual(self.mf2.find(i), self.mf2.find(i + 1))
        for i in range(0, 10 - 3, 4):
            self.mf1.merge(i, i + 3)
            self.mf2.merge(i, i + 3)
        for i in range(0, 10 - 4, 4):
            self.assertEqual(self.mf1.find(i), self.mf1.find(i + 1))
            self.assertEqual(self.mf1.find(i), self.mf1.find(i + 2))
            self.assertEqual(self.mf1.find(i), self.mf1.find(i + 3))
            self.assertEqual(self.mf2.find(i), self.mf2.find(i + 1))
            self.assertEqual(self.mf2.find(i), self.mf2.find(i + 2))
            self.assertEqual(self.mf2.find(i), self.mf2.find(i + 3))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
