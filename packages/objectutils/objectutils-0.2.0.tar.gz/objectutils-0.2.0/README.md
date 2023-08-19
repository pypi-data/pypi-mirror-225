# ```objectutils```

## Installation

```bash
pip install objectutils
```

## About
Tiny functions that extend python json-like objects functionality as highly customizable: 

- [traversing](#deep_traverse)
- [flattening](#flatten)
- [sum](#zip_dicts)
- [diff](#using-as-diff-default-mapping-and-filter)

operations on json-like python objects(lists, dicts)

Allows writing comprehensions without comprehensions 🙃

>Only python 3.10+ supported

>Provided as python library and made to be used from python directly. 

Inspired by:
- [jmespath](https://jmespath.org)
- [jq](https://jqlang.github.io/jq/)


## Examples
### Having the following response from some API:

```python
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
```
### ```deep_traverse```
You should write something like that to get the ```Counter``` of the software installed in total:

```python
from itertools import chain

c = Counter(chain.from_iterable([computer["software"] for computer in obj["computers"]]))
```

Such expressions getting even worse in more complicated cases.
With ```deep_traverse``` method provided by this tiny lib you should do the following to get the same ```Counter```:

```python
from objectutils import deep_traverse

c = deep_traverse(obj, [Counter, chain.from_iterable, "computers", [], "software"])
```

```deep_traverse``` supports callable objects in its path, as well as the keys of object.
```[]``` considered as all the possible values in iterable, as 'asterisk'(*).

> If applicable, calls the funcs and callable objects with unpacked iterable from the right. On exception that was predicted in this case, tries to call with single argument

As for me, it is much clearer approach than writing comprehensions or loops in such cases.

### ```flatten```
```python
from objectutils import flatten
```
Use ```flatten(obj)``` to get a flat dictionary in form ```{path: plain value}``` 
For the data above, the result is the following:
```python
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
```
### ```zip_dicts```
Used to join values of two similar dicts on same paths. May be used to find a diff betweens two dicts, join values as a sum

```python
from objectutils import zip_dicts


d1 = {
    1: {
        2: 3,
        3: 3,
    }
}
d2 = {
    1: {
        2: 4,
        3: 3,
    }
}
zip_dicts(d1, d2, lambda a, b: a+b, lambda a, b: a==b) # {1: {3: 6}} - "find a sum on all same paths where values are equal"
```
Third argument is a function for two items on the same paths, fourth is the filter for leaf dict values. 

#### Using as diff (default mapping and filter)
```python
d1 = {
    1: {
        3: 3,
        4: 2,
    }
}
d2 = {
    1: {
        3: 3,
        4: 3,
    }
}
zip_dicts(d1, d2) # {1: {4: (2, 3)}} - elements on path [1, 4] not equal(2 and 3 correspondingly)
```


The keys are the paths that may be used in ```deep_traverse``` to get the value next to them. However intended usage is to reduce the path somehow, using ```".".join()``` or something like that
