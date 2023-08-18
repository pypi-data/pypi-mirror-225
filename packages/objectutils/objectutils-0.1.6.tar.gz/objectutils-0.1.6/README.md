# ```objectutils```

## Installation

```bash
pip install objectutils
```

## About
Tiny functions that extend python json-like objects functionality as highly customizable: 

- diff
- sum
- flattening
- traversing 

operations on json-like python objects(lists, dicts)

Allows writing comprehensions without comprehensions 🙃

### For example, having the following response from some API:

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


>Only python 3.10+ supported

>Provided as python library and made to be used from python directly. 

Inspired by:
- [jmespath](https://jmespath.org)
- [jq](https://jqlang.github.io/jq/)
