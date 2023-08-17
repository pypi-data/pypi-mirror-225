# autotypedict

Dictionary-like class that automatically typecasts string-like values to standard types.

## Installation

### Using pip

```shell
python -m pip install -U autotypedict
```

## Usage

### Importing the class

```py
from autotypedict import AutoTypeDict
```

### Examples

```python
>>> d = {"foo": {"baz": "42"}, "bar": {"baz": "n/a", "qux": "true"}}
>>> AutoTypeDict(d)  # typecast every value
{'foo': {'baz': 42}, 'bar': {'baz': None, 'qux': True}}
>>> AutoTypeDict(d, ignored_keys=("baz",))  # ignore "baz"
{'foo': {'baz': '42'}, 'bar': {'baz': 'n/a', 'qux': True}}
>>> AutoTypeDict(d, ignored_keys=("bar.baz",))  # ignore d["bar"]["baz"]
{'foo': {'baz': 42}, 'bar': {'baz': 'n/a', 'qux': True}}
>>> td = AutoTypeDict()
>>> td.data = d  # updating data attribute to ignore typecasting
>>> td
{'foo': {'baz': '42'}, 'bar': {'baz': 'n/a', 'qux': 'true'}}
```

## Caveats

Values are only typecasted when the `AutoTypeDict` instance is updated directly, so avoid using type-specific operations on mutable objects within the dictionary (e.g. `list.append`, `dict.update`).

If using these methods is unavoidable, call the `.refresh()` instance method to re-process the dictionary.

Alternatives to common type operations:

Operation | Non-typecasted | Typecasted
:--- | :--- | :---
Append to list | `td["list"].append(v)` | `td["list"] += [v]`
Update dict | `td["dict"].update({k: v})` | `td["dict"][k] = v`
Merge dict | `td["dict"].update(other_dict)` | `td["dict"] \|= merge_dict` <sup>[1]</sup>

[1]: Python 3.9 or later
