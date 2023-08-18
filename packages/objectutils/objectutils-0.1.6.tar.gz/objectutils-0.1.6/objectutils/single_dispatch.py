from functools import singledispatch
from types import FunctionType, BuiltinFunctionType
from .fallbacks import fallback


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
    try:
        return traverse_item(p, o)(rest)
    except Exception as e:
        return traverse_item(p, o, exception=e)(rest)


@singledispatch
@fallback()
def traverse_item(p, o):
    return lambda rest: deep_traverse(o[p], rest)

@traverse_item.register(list)
@fallback()
def process_list(p, o):
    return lambda rest: type(p)([deep_traverse(o, (key, *rest)) for key in p or get_all_keys(o)])

@traverse_item.register(PathGroup)
@fallback()
def process_pathgroup(p, o):
    return lambda rest: p.traverse(o, rest)

def unpacked_args_handler(p, o):
    return lambda rest: p(deep_traverse(o, rest))

@traverse_item.register(type)
@traverse_item.register(BuiltinFunctionType)
@traverse_item.register(FunctionType)
@fallback({
        TypeError: unpacked_args_handler
    })
def process_func_item(p, o):
    return lambda rest: p(*deep_traverse(o, rest))

