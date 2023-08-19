from objectutils.traverse import deep_traverse, PathGroup as pg
from unittest import TestCase


class TestTraverse(TestCase):
    def test_traverse_dict_pathgroup(self):
        self.assertListEqual(
            deep_traverse({1: {4: 1}, 2: {3: {4: 4}, 5: 5}}, [pg([1, 4], [2, 3])]),
            [1, {4: 4}]
        )

    def test_traverse_dict_anykey(self):
        self.assertListEqual(
            deep_traverse({1: {4: 1}, 2: {3: {4: 4}, 5: {4: 4}}}, [2, [], 4]),
            [4, 4]
        )

    def test_traverse_list(self):
        self.assertEqual(
            deep_traverse([1, 2, [1, 2, [1, 2]]], [2, 2, 1]),
            2
        )
    
    def test_dict_traverse_trivial(self):
        a = {1:{}, 2: {3: 4, 5: 6, 7: 8}}
        self.assertEqual(
            deep_traverse(a, [2, 3]),
            4
        )

        self.assertEqual(
            deep_traverse(a, []),
            a
        )

        with self.assertRaises(KeyError):
            deep_traverse(a, [1, 0])

    def test_list_traverse_trivial(self):
        a = [[], [1], [1, 2]]
        self.assertEqual(
            deep_traverse(a, [2, 1]),
            2
        )

        self.assertEqual(
            deep_traverse(a, []),
            a
        )
        with self.assertRaises(IndexError):
            deep_traverse(a, [1, 1])

        with self.assertRaises(TypeError):
            deep_traverse(a, [1, 0, 0])

    def test_function_call(self):
        a = {1: {4: 1}, 2: {3: {4: 4}, 5: 5, 6: 6}}
        self.assertEqual(
            deep_traverse(a, [sum, pg([1, 4], [2, 5])]),
            6
        )

        self.assertEqual(
            deep_traverse(a, [sum, 2, pg([5], [6])]),
            11
        )

    def test_class_call(self):
        a = {"computers": 
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
        }
        from collections import Counter
        from itertools import chain
        self.assertEqual(
            deep_traverse(a, [Counter, "computers", chain.from_iterable, [], "software"]),
            {"s1": 2, "s2": 2, "s3": 2}
        )