from single_dispatch import deep_traverse
from collections import UserDict


class T(UserDict):
    def __getitem__(self, key):
        return deep_traverse(self.data, key)

a = {1: {1: {1: 1, 3: 8}}}

a = T(a)
# init(a)
a[1, 1, 1]

print(a[1, 1, []])