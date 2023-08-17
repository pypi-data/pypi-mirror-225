from collections import UserDict
from collections.abc import Iterable, Mapping
import json


class AutoTypeDict(UserDict):
    """Dictionary-like class that automatically tries to typecast each
    scalar value to a standard type.

    Values are only typecasted when the `AutoTypeDict` instance is
    updated directly, so avoid using type-specific operations on mutable
    objects within the dictionary (e.g. `list.append`, `dict.update`).
    If using these methods is unavoidable, call the `.refresh()`
    instance method to re-process the dictionary.

    Alternatives to common type operations:

    Operation | Non-typecasted | Typecasted
    :--- | :--- | :---
    Append to list | `td["list"].append(v)` | `td["list"] += [v]`
    Update dict | `td["dict"].update({k: v})` | `td["dict"][k] = v`
    Merge dict | `td["dict"].update(other_dict)` | `td["dict"] \|= merge_dict` [1]

    [1]: Python 3.9 or later

    Attributes:
        data (dict): Underlying data object as a pure `dict`.

    Examples:
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

    """

    def __init__(
        self,
        d: Mapping | None = None,
        ignored_keys: Iterable[str] = (),
        null_values: Iterable = ("null", "n/a", "none"),
        bool_values: Iterable[tuple] = (("yes", "no"), ("true", "false")),
    ):
        """Inits AutoTypeDict.

        Args:
            d: Initial dictionary data. Defaults to `None`.
            ignored_keys: List of object keys to exempt from typecasting.
            Each entry can either be a single key or a simple JSONPath-like
            sequence of keys (e.g. "foo.bar"). Defaults to `()`.
            null_values: List of values to consider as `None`. Defaults to
            `("n/a", "none")`.
            bool_values: List of string pairs to consider as `bool`, where
            the first value is `True` and the second value is `False`.
            Defaults to `(("yes", "no"), ("true", "false"))`.

        """
        self.ignored_keys = ignored_keys
        self.null_values = null_values
        self.bool_values = bool_values
        super().__init__(d)

    def __setitem__(self, key, item):
        self.data[key] = self._typecast_object(item, _keys=(key,))

    def __ior__(self, other):
        self.data |= self._typecast_object(
            other.data if isinstance(other, UserDict) else other
        )
        return self

    def _typecast_object(self, d: Iterable, _keys: tuple = ("",)):
        """Recurse through an object and attempt to typecast each scalar
        value to a standard data type.

        Args:
            d: Object to typecast
            _keys: Key of object, used for recursion

        Returns:
            Iterable: The input object with all scalar values typecast.

        """
        if isinstance(d, Mapping):
            return type(d)(
                (k, self._typecast_object(v, _keys + (k,))) for k, v in d.items()
            )
        elif isinstance(d, Iterable) and not isinstance(d, (str, bytes)):
            return type(d)(self._typecast_object(v, _keys) for v in d)
        elif (_keys[-1] in self.ignored_keys) or (".".join(_keys) in self.ignored_keys):
            return d
        elif isinstance(d, bytes):
            return self._typecast_string(d.decode())
        return self._typecast_string(d) if isinstance(d, str) else d

    def _typecast_string(self, s: str):
        """Try to typecast a string as a standard data type and return
        the result.

        Args:
            s: String to be typecast

        Returns:
            any: The input value as the most appropriate standard type.

        """
        s_l = s.lower().strip()
        if not s_l:  # blank
            return None
        if s_l in self.null_values:  # null
            return None
        if s_l in [x for y in self.bool_values for x in y]:  # bool
            return s_l in [x[0] for x in self.bool_values]
        if pct := s_l.endswith("%"):  # percentage
            s_l = s_l[:-1]
        try:
            num = int(s_l)  # int
        except ValueError:
            try:
                num = float(s_l)  # float
            except ValueError:
                return s.strip()
        return (num / 100) if pct else num

    def refresh(self):
        """Typecast the entire dictionary in place. Call this method if
        changes have been made to the dictionary contents that did not
        directly add or update a key (e.g. appending values to a `list`
        with `.append`, updating a nested `dict` with `.update`).

        Example:
            >>> d = {"foo": ["42", "false"]}
            >>> td = AutoTypeDict(d)
            >>> td
            {'foo': [42, False]}

            >>> td["foo"].append("n/a")
            >>> td
            {'foo': [42, False, 'n/a']}

            >>> td.refresh()
            >>> td
            {'foo': [42, False, None]}

        """
        self.data = self._typecast_object(self.data)

    def to_json(self, **kwargs):
        """Return this object as a JSON-formatted string.

        `kwargs` are passed directly to the `json.dumps` function.

        Returns:
            str: JSON-formatted string

        """

        class TypedEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, AutoTypeDict):
                    return obj.data
                return json.JSONEncoder.default(self, obj)

        return json.dumps(
            self.data,
            cls=TypedEncoder,
            **kwargs
        )
