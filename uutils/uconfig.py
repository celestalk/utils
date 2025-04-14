import collections.abc as a
import typing as t

__all__ = ['Config', 'ConfigItem']


class ConfigItem(t.Protocol):
    """ Protocol for config items """

    def __iter__(self): ...


class Config(a.Mapping):
    """ ReadOnly Configuration holder
    """

    class Item(a.Mapping):
        """ Configuration item
        """

        def __init__(self, path: tuple[str, ...], source: a.Mapping[str, t.Any]):
            self._path = path
            self._dict = dict((name, self._normalize((path + (name,)), value))
                              for name, value in source.items())

        def __getattr__(self, name: str) -> t.Any:
            if name in self._dict:
                return self._dict[name]
            raise AttributeError(f'Config `.{'.'.join(self._path)}` has no attribute `{name}`')

        def __getitem__(self, key, /):
            value = getattr(self, key)
            if isinstance(value, a.Mapping):
                return dict(**value)
            elif isinstance(value, tuple):
                return [dict(**item) if isinstance(item, a.Mapping) else item for item in value]
            return value

        def __iter__(self):
            return iter(self._dict.keys())

        def __len__(self):
            return len(self._dict)

        @classmethod
        def _normalize(cls, path: tuple[str, ...], value: t.Any, from_array=False) \
                -> t.Any | tuple[t.Self] | t.Self:
#            if isinstance(value, Config):
#                return cls(path, dict(value))
#            el
            if isinstance(value, a.Mapping):
                return cls(path, value)
            elif isinstance(value, (bytes, bytearray, str)):
                return value
            elif isinstance(value, a.Iterable):
                if from_array:
                    raise ValueError("Nested arrays (tuple, set, list, ...) are not supported.")
                value = [value for value in value]
                return tuple(cls._normalize(path[:-1] + (f'{path[-1:]}[{N}]',), value[N], True)
                             for N in range(len(value)))
            return value

    def __init__(self, source: a.Mapping[str, t.Any], **kwargs: t.Any):
        self._item = self.Item((), dict(source, **kwargs))

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self._item, name)

    def __getitem__(self, key, /):
        return self._item[key]

    def __len__(self):
        return len(self._item)

    def __iter__(self):
        return iter(self._item)
