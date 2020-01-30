from __future__ import generator_stop

import collections


class IndexedSentinel:
    def __init__(self, iiter):
        self._iiter = iiter

    def __bool__(self):
        self._iiter.set_iter(self)  # !!!
        return False

    def __getattr__(self, key):
        return IndexedSentinelGetattr(self, key)

    def __eq__(self, other):
        return IndexedSentinelEq(self, other)


class IndexedSentinelGetattr(IndexedSentinel):
    def __init__(self, parent, key):
        self.key = key
        self.parent = parent
        self._iiter = parent._iiter


class IndexedSentinelEq(IndexedSentinel):
    def __init__(self, parent, constant):
        self.constant = constant
        self.parent = parent
        self._iiter = parent._iiter

# ---

class IndexedTable:
    def __init__(self, shape):
        self.row = collections.namedtuple('Row', shape)
        self._list = set()
        self._index = {field: {} for field in self.row._fields}

    def extend(self, data):
        data = set(data)

        self._list.update(data)

        for elem in data:
            for key, lookup in self._index.items():
                value = getattr(elem, key)
                if value not in lookup:
                    lookup[value] = set()
                lookup[value].add(elem)

    def all(self):
        return iter(self._list)

    def __iter__(self):
        return IndexedTableIter(self)


class IndexedTableIter:
    START = object()
    PRIMED = object()

    def __init__(self, itable):
        self._itable = itable
        self._iter = IndexedTableIter.START

    def set_iter(self, sentinel):
        # XXX: this fn is very proof-of-concept hardcoded
        self._iter = iter(self._itable._index[sentinel.parent.key].get(sentinel.constant, []))

    def __next__(self):
        if self._iter is IndexedTableIter.START:
            self._iter = IndexedTableIter.PRIMED
            return IndexedSentinel(self)

        if self._iter is IndexedTableIter.PRIMED:
            raise Exception(
                "No filter specified in comprehension. "
                "Use '.all()' to iterate all elements"
            )

        # Implicit StopIteration
        return next(self._iter)


if __name__ == '__main__':

    table = IndexedTable(shape='foo bar')
    table.extend(
        table.row(foo=foo, bar=bar)
        for foo in range(1, 11)
        for bar in range(1, 11)
    )

    print( [
        elem.bar for elem in table
        if elem.foo == 10
    ] )
