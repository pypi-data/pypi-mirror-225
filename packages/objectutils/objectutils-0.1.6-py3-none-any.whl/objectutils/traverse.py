def get_all_keys(iter):
    """
    Returns all the values that is suitable for `__getitem__()` method of its arg
    """
    try:
        return iter.keys()
    except AttributeError:
        return range(len(iter))


class PathGroup:
    """
    Represents a few alternative paths as a single object
    """
    def __init__(self, *paths, type=list):
        self.paths = paths
        self.type = type

    def traverse_iter(self, o, rest):
        yield from (deep_traverse(o, (*path, *rest)) for path in self.paths)

    def traverse(self, o, rest):
        return self.type(self.traverse_iter(o, rest))


def deep_traverse(o: list | dict, path: list) -> list | dict:
    """
    Method for traversing object with given path

    Sample usage:
    ```
    deep_traverse({1: {4: 1}, 2: {3: {4: 4}, 5: {4: 4}}}, [sum, 2, [], 4]) -> 8 (without 'sum' in path the result is [4, 4])
    ```
    """
    try:
        p, *rest = path
    except ValueError:
        return o
    match p:
        case PathGroup(): return p.traverse(o, rest)
        case [*_]:
            keys = p or get_all_keys(o)
            return type(p)([deep_traverse(o, (key, *rest)) for key in keys])
        case p if callable(p): return p(deep_traverse(o, rest))
        case _: return deep_traverse(o[p], rest)
