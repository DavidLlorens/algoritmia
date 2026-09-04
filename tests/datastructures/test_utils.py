# coding: latin1
import unittest

from algoritmia.utils import argmax, argmin, infinity


class TestMinMax(unittest.TestCase):
    def testInfinty(self):
        self.assertTrue(infinity > 1)
        self.assertTrue(infinity > 2 ** 1000)
        self.assertTrue(-infinity < 2 ** 1000)

    def test_argmin(self):
        self.assertEqual(argmin((1, 2, 3, 4), lambda x: -x), 4)
        self.assertEqual(argmin([], lambda x: -x), None)

    def test_argmax(self):
        self.assertEqual(argmax((1, 2, 3, 4), lambda x: -x), 1)
        self.assertEqual(argmax([], lambda x: -x), None)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
