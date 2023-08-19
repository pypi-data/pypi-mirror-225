from functools import singledispatch


def recursion_level(func):
    def wrapper(*args ,**kwargs):
        try:
            func.depth += 1
            ret = func(*args, **{**kwargs, "depth": func.depth})
            func.depth -= 1
        except TypeError:
            raise AssertionError("Need '**kwargs' in method signature declaration")
        return ret
    func.depth = 0
    return wrapper

@singledispatch
def get_keyvalue(o):
    pass

@get_keyvalue.register(dict)
def _(o):
    return o.items()

@get_keyvalue.register(list)
def _(o):
    return enumerate(o)

@singledispatch
def flatten(o):
    return {(): o}

@flatten.register(dict)
@flatten.register(list)
def _(o):
    return {
        (k, *kinner): vinner
        for k, v in get_keyvalue(o)
            for kinner, vinner in get_keyvalue(flatten(v))
    } 


def zip_dicts(i1, i2, element_mapping=lambda a,b: (a,b), element_filter=lambda a,b: a!=b, **kwargs):
    match i1, i2:
        case dict(), dict(): return dictsum(i1, i2, element_mapping, element_filter)
        case list(), list(): return listsum(i1, i2)
        case _: return element_mapping(i1, i2) if element_filter(i1, i2) else None
    

def dictsum(d1, d2, e_mapping, e_filter, per_itempair=zip_dicts):
    return {
        k: value
        for k in set((*d1.keys(), *d2.keys()))
        if (value := per_itempair(d1.get(k), d2.get(k), e_mapping, e_filter))
    }


def listsum(l1, l2, e_mapping, e_filter, per_itempair=zip_dicts):
    return {
        i: value
        for i, items in enumerate(zip(l1,l2))
        if (value := per_itempair(*items, e_mapping, e_filter))
    }
