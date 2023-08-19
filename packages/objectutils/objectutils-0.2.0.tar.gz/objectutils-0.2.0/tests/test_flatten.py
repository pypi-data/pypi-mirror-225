from objectutils import flatten
from unittest import TestCase


class TestFlatten(TestCase):
    def test_combined(self):
        obj = {"computers": [
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

        self.assertEqual(
            flatten(obj),
            {
                ("computers", 0, "computername"): "1",
                ("computers", 0, "software", 0): "s1",
                ("computers", 0, "software", 1): "s2",
                ("computers", 1, "computername"): "2",
                ("computers", 1, "software", 0): "s2",
                ("computers", 1, "software", 1): "s3",
                ("computers", 2, "computername"): "3",
                ("computers", 2, "software", 0): "s1",
                ("computers", 2, "software", 1): "s3",
            }
        )
    def test_flatten_list(self):
        a = [1,2,3, [1]]
        self.assertEqual(
            flatten(a),
            {
                (0,): 1,
                (1,): 2,
                (2,): 3,
                (3, 0): 1
            }
        )