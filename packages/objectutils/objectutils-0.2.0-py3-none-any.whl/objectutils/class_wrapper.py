from .single_dispatch import deep_traverse
from collections import UserDict, UserList
from functools import singledispatch

@singledispatch
def T(obj):
    pass

@T.register(dict)
def _(obj):
    return TraverseDict(obj)

@T.register(list)
def _(obj):
    return TraverseList(obj)

class TraverseDict(UserDict):
    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key, )
        return deep_traverse(self.data, key)
        

class TraverseList(UserList):
    def __getitem__(self, key):
        try:
            return deep_traverse(self.data, key)
        except TypeError:
            return super().__getitem__(key)