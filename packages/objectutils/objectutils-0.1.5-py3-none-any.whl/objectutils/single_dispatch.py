from functools import singledispatch
from types import FunctionType, BuiltinFunctionType
classtype = type(FunctionType) # Found no way to import <class 'type'> 🙁


@singledispatch
def get_all_keys(iter):
    pass
    
@get_all_keys.register(tuple)
@get_all_keys.register(list)
def _(key):
    return range(len(key))

@get_all_keys.register
def _(key: dict):
    return key.keys()


class PathGroup:
    def __init__(self, *paths, type=list):
        self.paths = paths
        self.type = type

    def traverse_iter(self, o, rest):
        yield from (deep_traverse(o, (*path, *rest)) for path in self.paths)

    def traverse(self, o, rest):
        return self.type(self.traverse_iter(o, rest))


def deep_traverse(o, path):
    try:
        p, *rest = path
    except ValueError:
        return o
    return traverse_item(p, o)(rest)
        

@singledispatch
def traverse_item(p, o):
    return lambda rest: deep_traverse(o[p], rest)

@traverse_item.register
def _(p: list, o):
    return lambda rest: type(p)([deep_traverse(o, (key, *rest)) for key in p or get_all_keys(o)])

@traverse_item.register
def _(p: PathGroup, o):
    return lambda rest: p.traverse(o, rest)

@traverse_item.register(classtype)
@traverse_item.register(BuiltinFunctionType)
@traverse_item.register(FunctionType)
def _(p, o):
    return lambda rest: p(deep_traverse(o, rest))
