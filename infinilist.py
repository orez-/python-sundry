def _index(indexable):
    if not hasattr(indexable, '__index__'):
        raise TypeError(f"list indices must be integers or slices, not {type(indexable).__name__}")
    return indexable.__index__()


class SparseList:
    def __init__(self, iterable=(), *, default=None):
        if isinstance(iterable, SparseList):
            if default is not None:
                # No technical reason to disallow this, but logically it's weird to "rewrite" all
                # `default` elements of the source SparseList
                raise TypeError("may not specify `default` when creating from existing SparseList")
            self._default = iterable._default
            self._min = iterable._min
            self._max = iterable._max
            self._data = dict(iterable._data)
        else:
            self._default = default
            self._data = dict(enumerate(iterable))
            if self._data:
                self._min = 0
                self._max = len(self._data) - 1
            else:
                self._min = None
                self._max = None

    def __iter__(self):
        # Kind of weird to make this iterable: where to start?
        raise TypeError(f"{type(self).__name__!r} object is not iterable")

    def __getitem__(self, key):
        if not isinstance(key, slice):
            return self._data.get(_index(key), self._default)
        if not self._data:
            return []
        return [
            self._data.get(i, self._default)
            for i in range(key.start or self._min, key.stop or (self._max + 1), key.step or 1)
        ]

    def _unset(self, key):
        self._data.pop(key, None)
        if not self._data:
            self._min = None
            self._max = None
            return
        if self._min in (key, None):
            self._min = min(self._data)
        if self._max in (key, None):
            self._max = max(self._data)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise NotImplementedError("Assigning to slices is not implemented")
        key = _index(key)
        if value != self._default:  # set
            self._data[key] = value
            if self._min is None or key < self._min:
                self._min = key
            if self._max is None or key > self._max:
                self._max = key
        else:  # "unset"
            self._unset(key)

    def __delitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError("Deleting slices is not implemented")
        self._unset(key)

# ---

# def test_shit():
