from objectutils.class_wrapper import T
from objectutils.single_dispatch import PathGroup as pg
from objectutils import deep_traverse
from unittest import TestCase


class TestTraverseSingleDispatch(TestCase):
    def test_traverse_dict_pathgroup(self):
        a = T({1: {4: 1}, 2: {3: {4: 4}, 5: 5}})
        self.assertListEqual(
            a[pg([1, 4], [2, 3])],
            [1, {4: 4}]
        )

    def test_traverse_dict_anykey(self):
        a = T({1: {4: 1}, 2: {3: {4: 4}, 5: {4: 4}}})
        self.assertListEqual(
            a[2, [], 4],
            [4, 4]
        )

    def test_traverse_list(self):
        a = T([1, 2, [1, 2, [1, 2]]])
        self.assertEqual(
            a[2, 2, 1],
            2
        )
    
    def test_dict_traverse_trivial(self):
        a = T({1:{}, 2: {3: 4, 5: 6, 7: 8}})
        self.assertEqual(
            a[2, 3],
            4
        )

        self.assertEqual(
            deep_traverse(a, []),
            a
        )

        with self.assertRaises(KeyError):
            a[1, 0]

    def test_list_traverse_trivial(self):
        a = T([[], [1], [1, 2]])
        self.assertEqual(
            a[2, 1],
            2
        )

        self.assertEqual(
            a[[]],
            a
        )
        with self.assertRaises(IndexError):
            a[1, 1]

        with self.assertRaises(TypeError):
            a[1, 0, 0]

    def test_function_call(self):
        a = T({1: {4: 1}, 2: {3: {4: 4}, 5: 5, 6: 6}})
        self.assertEqual(
            a[sum, pg([1, 4], [2, 5])],
            6
        )

        self.assertEqual(
            a[sum, 2, pg([5], [6])],
            11
        )

    def test_class_call(self):
        a = T({"computers": 
            [
                {
                    "computername": "1",
                    "software": ["s1", "s2"],
                },
                {
                    "computername": "2",
                    "software": ["s2", "s3"],
                },
                {
                    "computername": "3",
                    "software": ["s1", "s3"],
                },
            ]
        })
        from collections import Counter
        from itertools import chain
        self.assertEqual(
            a[Counter, chain.from_iterable, "computers", [], "software"],
            {"s1": 2, "s2": 2, "s3": 2}
        )

    def test_fallback_call(self):
        a = T({1: [1,2,3,4]})
        s = lambda *args: sum(args)
        self.assertEqual(
            a[lambda *args: sum(args), 1],
            10
        )
        self.assertEqual(
            a[lambda a: sum(a), 1],
            10
        )
