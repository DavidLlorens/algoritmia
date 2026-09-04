# coding: latin1

import unittest
from random import seed, shuffle

from algoritmia.datastructures.prioritymaps import (MinHeapMap, MaxHeapMap, MinFibonacciHeap, MaxFibonacciHeap)


class TestHeapMaps(unittest.TestCase):
    def setUp(self):
        self.pd1 = MinHeapMap()
        self.pairs = [('a', 1), ('z', 10), ('b', 5), ('c', 8), ('d', 12), ('e', 10)]
        self.pd2 = MinHeapMap(self.pairs)
        self.pairdict = dict(self.pairs)
        self.pd3 = MinHeapMap(self.pairdict)

    def test_ctor(self):
        self.assertEqual(len(self.pd1), 0)
        self.assertEqual(len(self.pd2), 6)
        self.assertEqual(len(self.pd2), 6)

    def test_opt(self):
        self.assertRaises(IndexError, self.pd1.opt)
        for i in (1, 5, 8, 10, 10, 12):
            self.assertEqual(self.pd2[self.pd2.opt()], i)
            self.pd2.extract_opt()
            self.assertEqual(self.pd3[self.pd3.opt()], i)
            self.pd3.extract_opt()

    def test_getitem(self):
        for k, v in self.pairs:
            self.assertEqual(self.pd2[k], v)
            self.assertEqual(self.pd3[k], v)
        self.assertRaises(KeyError, self.pd2.__getitem__, 'xx')
        self.assertRaises(KeyError, self.pd3.__getitem__, 'xx')

    def test_setitem(self):
        for pd in self.pd1, self.pd2, self.pd3:
            for k, v in pd.items():
                pd[k] = pd[k] + 1
                self.assertEqual(pd[k], v + 1)
                pd[k] = pd[k] - 10
                self.assertEqual(pd[k], v - 9)
            for k, v in ('xx', 10), ('yy', 100):
                pd[k] = v
                self.assertEqual(pd[k], v)

    def test_opt_value_and_item(self):
        for pd in self.pd1, self.pd2, self.pd3:
            if len(pd) > 0:
                self.assertEqual(pd.opt_item()[1], pd.opt_value())
                self.assertEqual(pd.opt_item()[0], pd.opt())
            else:
                self.assertRaises(IndexError, pd.opt_item)

    def test_contains(self):
        for pd in self.pd2, self.pd3:
            for k, v in self.pairs:
                self.assertTrue(k in pd)
        for pd in [self.pd1]:
            for k, v in self.pairs:
                self.assertFalse(k in pd)

    def test_del(self):
        for pd in self.pd2, self.pd3:
            for k, v in self.pairs:
                del pd[k]
            self.assertEqual(len(pd), 0)

    def test_repr(self):
        i = 0
        for pd in self.pd1, self.pd2, self.pd3:
            i += 1
            if len(pd) > 0:
                self.assertEqual(list(sorted(self.pairs)), list(sorted(eval(repr(pd)).items())))

    def test_min_and_max_prioritydics(self):
        a = MinHeapMap(self.pairs)
        b = MaxHeapMap(self.pairs)
        self.assertEqual(len(self.pairs), len(a))
        self.assertEqual(len(self.pairs), len(b))


class TestHeapMap2(unittest.TestCase):
    def setUp(self):
        seed(0)
        self.ll = [(chr(ord('a') + i), i) for i in range(26)]
        shuffle(self.ll)
        self.minpd = MinHeapMap(data=self.ll)
        self.maxpd = MaxHeapMap(data=self.ll)

    def test_opt_onNonEmptyPriorityDict_getsOptimumKey(self):
        self.assertEqual(self.minpd.opt(), 'a')
        self.assertEqual(self.maxpd.opt(), 'z')

    def test_opt_item_onNonEmptyPriorityDict_getsOptimumItem(self):
        self.assertEqual(self.minpd.opt_item(), ('a', 0))
        self.assertEqual(self.maxpd.opt_item(), ('z', 25))

    def test_opt_value_onNonEmptyPriorityDict_getsOptimumValue(self):
        self.assertEqual(self.minpd.opt_value(), 0)
        self.assertEqual(self.maxpd.opt_value(), 25)

    def test_extract_opt_onNonEmptyPriorityDict_extractsOptimumAndGetsKey(self):
        self.assertEqual(self.minpd.extract_opt(), 'a')
        self.assertEqual(self.minpd.opt(), 'b')
        self.assertEqual(self.maxpd.extract_opt(), 'z')
        self.assertEqual(self.maxpd.opt(), 'y')

    def test_extract_opt_onNonEmptyPriorityDict_extractsOptimumAndGetsItem(self):
        self.assertEqual(self.minpd.extract_opt_item(), ('a', 0))
        self.assertEqual(self.minpd.opt(), 'b')
        self.assertEqual(self.maxpd.extract_opt_item(), ('z', 25))
        self.assertEqual(self.maxpd.opt(), 'y')

    def test_contains_KeyInDict_returnsTrue(self):
        for i in range(26):
            self.assertTrue(chr(ord('a') + i) in self.minpd)
            self.assertTrue(chr(ord('a') + i) in self.maxpd)

    def test_contains_KeyNotInDict_returnsFalse(self):
        for c in 'A', '1':
            self.assertFalse(c in self.minpd)
            self.assertFalse(c in self.maxpd)

    def test_getItem_KeyInDict_returnsAssociateValue(self):
        for i in range(26):
            self.assertEqual(self.minpd[chr(ord('a') + i)], i)
            self.assertEqual(self.maxpd[chr(ord('a') + i)], i)

    def test_getItem_KeyNotInDict_raisesException(self):
        for c in 'A', '1':
            self.assertRaises(KeyError, self.minpd.__getitem__, c)
            self.assertRaises(KeyError, self.maxpd.__getitem__, c)

    def test_setItem_KeyNotInDict_createsNewItem(self):
        self.minpd['A'] = -1
        self.assertEqual(self.minpd['A'], -1)
        self.minpd['1'] = 100
        self.assertEqual(self.minpd['1'], 100)

    def test_setItem_KeyInDict_changesItem(self):
        self.minpd['a'] = -1
        self.assertEqual(self.minpd['a'], -1)
        self.minpd['z'] = 100
        self.assertEqual(self.minpd['z'], 100)

    def test_setItem_definingNewOpt_changesOpt(self):
        self.minpd['m'] = -1
        self.assertEqual(self.minpd.opt(), 'm')
        self.maxpd['m'] = 100
        self.assertEqual(self.maxpd.opt(), 'm')

    def test_delItem_existingKey_removesItem(self):
        del self.minpd['m']
        self.assertRaises(KeyError, self.minpd.__getitem__, 'm')
        del self.maxpd['m']
        self.assertRaises(KeyError, self.maxpd.__getitem__, 'm')

    def test_delItem_nonExistingKey_raisesException(self):
        self.assertRaises(KeyError, self.minpd.__delitem__, 'A')
        self.assertRaises(KeyError, self.maxpd.__delitem__, 'A')

    def test_keys_onPriorityDict_iteratesAllKeys(self):
        self.assertEqual(set(self.minpd.keys()), set((a for (a, b) in self.ll)))
        self.assertEqual(set(self.maxpd.keys()), set((a for (a, b) in self.ll)))

    def test_values_onPriorityDict_iteratesAllValues(self):
        self.assertEqual(set(self.minpd.values()), set((b for (a, b) in self.ll)))
        self.assertEqual(set(self.maxpd.values()), set((b for (a, b) in self.ll)))

    def test_items_onPriorityDict_iteratesAllItems(self):
        self.assertEqual(set(self.minpd.items()), set(self.ll))
        self.assertEqual(set(self.maxpd.items()), set(self.ll))

    def test_get_onExistingKey_returnsValue(self):
        self.assertEqual(self.minpd.get('a', 100), 0)
        self.assertEqual(self.maxpd.get('a', 100), 0)

    def test_get_onNonExistingKey_returnsDefaultValue(self):
        self.assertEqual(self.minpd.get('A', 100), 100)
        self.assertEqual(self.maxpd.get('A', 100), 100)

    def test_setdefault_onExistingKey_returnsValue(self):
        self.assertEqual(self.minpd.setdefault('a', 100), 0)
        self.assertEqual(self.maxpd.setdefault('a', 100), 0)

    def test_setdefault_onNonExistingKey_returnsNewValue(self):
        self.assertEqual(self.minpd.setdefault('A', 100), 100)
        self.assertEqual(self.maxpd.setdefault('A', 100), 100)

    def test_iter_onPriorityMap_returnsKeys(self):
        self.assertEqual(set(self.minpd), set((a for (a, b) in self.ll)))
        self.assertEqual(set(self.maxpd), set((a for (a, b) in self.ll)))

    def test_len_onPriorityMap_returnsSize(self):
        self.assertEqual(len(self.minpd), 26)
        self.assertEqual(len(self.maxpd), 26)

    def test_repr_onPriorityMap_shouldReturnEvaluableExpression(self):
        self.assertEqual(list(sorted(self.minpd)), list(sorted(eval(repr(self.minpd)))))
        self.assertEqual(list(sorted(self.maxpd)), list(sorted(eval(repr(self.maxpd)))))


class TestFibonacciHeap(unittest.TestCase):
    def setUp(self):
        self.pairs = [('a', 1), ('z', 11), ('b', 5), ('c', 8), ('d', 12), ('e', 10)]
        self.a = MinFibonacciHeap(self.pairs)

    def test_len(self):
        self.assertEqual(len(self.pairs), len(self.a))

    def test_opt(self):
        for i in (1, 5, 8, 10, 11, 12):
            self.assertEqual(self.a[self.a.opt()], i)
            self.a.extract_opt()

    def test_getitem(self):
        for k, v in self.pairs:
            self.assertEqual(self.a[k], v)
        self.assertRaises(KeyError, self.a.__getitem__, 'xx')

    def test_setitem(self):
        for k, v in self.a.items():
            v = self.a[k]
            self.assertRaises(ValueError, self.a.__setitem__, k, v + 1)
            self.a[k] = self.a[k] - 10
            self.assertEqual(self.a[k], v - 10)
        for k, v in ('xx', 10), ('yy', 100):
            self.a[k] = v
            self.assertEqual(self.a[k], v)

        v = -100
        while len(self.a) > 0:
            w = self.a.opt_value()
            self.assertTrue(v <= w)
            self.a.extract_opt()
            v = w

    def test_opt_value_and_item(self):
        if len(self.a) > 0:
            self.assertEqual(self.a.opt_item()[1], self.a.opt_value())
            self.assertEqual(self.a.opt_item()[0], self.a.opt())
        else:
            self.assertRaises(IndexError, self.a.opt_item)

    def test_contains(self):
        for k, v in self.pairs:
            self.assertTrue(k in self.a)
        for k in 'x', 'y', '':
            self.assertFalse(k in self.a)

    def test_del(self):
        for k, v in self.pairs:
            del self.a[k]
        self.assertEqual(len(self.a), 0)

    def test_repr(self):
        self.assertEqual(len(self.a), len(eval(repr(self.a))))


class TestFibonacciHeap2(unittest.TestCase):
    def setUp(self):
        seed(0)
        self.ll = [(chr(ord('a') + i), i) for i in range(26)]
        shuffle(self.ll)
        self.minpd = MinFibonacciHeap(data=self.ll)
        self.maxpd = MaxFibonacciHeap(data=self.ll)

    def test_opt_onNonEmptyPriorityDict_getsOptimumKey(self):
        self.assertEqual(self.minpd.opt(), 'a')
        self.assertEqual(self.maxpd.opt(), 'z')

    def test_opt_item_onNonEmptyPriorityDict_getsOptimumItem(self):
        self.assertEqual(self.minpd.opt_item(), ('a', 0))
        self.assertEqual(self.maxpd.opt_item(), ('z', 25))

    def test_opt_value_onNonEmptyPriorityDict_getsOptimumValue(self):
        self.assertEqual(self.minpd.opt_value(), 0)
        self.assertEqual(self.maxpd.opt_value(), 25)

    def test_extract_opt_onNonEmptyPriorityDict_extractsOptimumAndGetsKey(self):
        self.assertEqual(self.minpd.extract_opt(), 'a')
        self.assertEqual(self.minpd.opt(), 'b')
        self.assertEqual(self.maxpd.extract_opt(), 'z')
        self.assertEqual(self.maxpd.opt(), 'y')

    def test_extract_opt_onNonEmptyPriorityDict_extractsOptimumAndGetsItem(self):
        self.assertEqual(self.minpd.extract_opt_item(), ('a', 0))
        self.assertEqual(self.minpd.opt(), 'b')
        self.assertEqual(self.maxpd.extract_opt_item(), ('z', 25))
        self.assertEqual(self.maxpd.opt(), 'y')

    def test_contains_KeyInDict_returnsTrue(self):
        for i in range(26):
            self.assertTrue(chr(ord('a') + i) in self.minpd)
            self.assertTrue(chr(ord('a') + i) in self.maxpd)

    def test_contains_KeyNotInDict_returnsFalse(self):
        for c in 'A', '1':
            self.assertFalse(c in self.minpd)
            self.assertFalse(c in self.maxpd)

    def test_getItem_KeyInDict_returnsAssociateValue(self):
        for i in range(26):
            self.assertEqual(self.minpd[chr(ord('a') + i)], i)
            self.assertEqual(self.maxpd[chr(ord('a') + i)], i)

    def test_getItem_KeyNotInDict_raisesException(self):
        for c in 'A', '1':
            self.assertRaises(KeyError, self.minpd.__getitem__, c)
            self.assertRaises(KeyError, self.maxpd.__getitem__, c)

    def test_setItem_KeyNotInDict_createsNewItem(self):
        self.minpd['A'] = -1
        self.assertEqual(self.minpd['A'], -1)
        self.minpd['1'] = 100
        self.assertEqual(self.minpd['1'], 100)

    def test_setItem_KeyInDict_changesItem(self):
        self.minpd['a'] = -1
        self.assertEqual(self.minpd['a'], -1)
        self.maxpd['z'] = 100
        self.assertEqual(self.maxpd['z'], 100)

    def test_setItem_KeyInDictButNotImproving_raisesException(self):
        self.assertRaises(ValueError, self.minpd.__setitem__, 'a', 100)
        self.assertRaises(ValueError, self.maxpd.__setitem__, 'a', -1)

    def test_setItem_definingNewOpt_changesOpt(self):
        self.minpd['m'] = -1
        self.assertEqual(self.minpd.opt(), 'm')
        self.maxpd['m'] = 100
        self.assertEqual(self.maxpd.opt(), 'm')

    def test_delItem_existingKey_removesItem(self):
        del self.minpd['m']
        self.assertRaises(KeyError, self.minpd.__getitem__, 'm')
        del self.maxpd['m']
        self.assertRaises(KeyError, self.maxpd.__getitem__, 'm')

    def test_delItem_nonExistingKey_raisesException(self):
        self.assertRaises(KeyError, self.minpd.__delitem__, 'A')
        self.assertRaises(KeyError, self.maxpd.__delitem__, 'A')

    def test_keys_onPriorityDict_iteratesAllKeys(self):
        self.assertEqual(set(self.minpd.keys()), set((a for (a, b) in self.ll)))
        self.assertEqual(set(self.maxpd.keys()), set((a for (a, b) in self.ll)))

    def test_values_onPriorityDict_iteratesAllValues(self):
        self.assertEqual(set(self.minpd.values()), set((b for (a, b) in self.ll)))
        self.assertEqual(set(self.maxpd.values()), set((b for (a, b) in self.ll)))

    def test_items_onPriorityDict_iteratesAllItems(self):
        self.assertEqual(set(self.minpd.items()), set(self.ll))
        self.assertEqual(set(self.maxpd.items()), set(self.ll))

    def test_get_onExistingKey_returnsValue(self):
        self.assertEqual(self.minpd.get('a', 100), 0)
        self.assertEqual(self.maxpd.get('a', 100), 0)

    def test_get_onNonExistingKey_returnsDefaultValue(self):
        self.assertEqual(self.minpd.get('A', 100), 100)
        self.assertEqual(self.maxpd.get('A', 100), 100)

    def test_setdefault_onExistingKey_returnsValue(self):
        self.assertEqual(self.minpd.setdefault('a', 100), 0)
        self.assertEqual(self.maxpd.setdefault('a', 100), 0)

    def test_setdefault_onNonExistingKey_returnsNewValue(self):
        self.assertEqual(self.minpd.setdefault('A', 100), 100)
        self.assertEqual(self.maxpd.setdefault('A', 100), 100)

    def test_iter_onPriorityMap_returnsKeys(self):
        self.assertEqual(set(self.minpd), set((a for (a, b) in self.ll)))
        self.assertEqual(set(self.maxpd), set((a for (a, b) in self.ll)))

    def test_len_onPriorityMap_returnsSize(self):
        self.assertEqual(len(self.minpd), 26)
        self.assertEqual(len(self.maxpd), 26)

    def test_repr_onPriorityMap_shouldReturnEvaluableExpression(self):
        self.assertEqual(list(sorted(self.minpd)), list(sorted(eval(repr(self.minpd)))))
        self.assertEqual(list(sorted(self.maxpd)), list(sorted(eval(repr(self.maxpd)))))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
