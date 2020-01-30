"""
As I recall this went to shit because `len` int-ifies

2018-07-24: fuck it, roll your own `len`
"""
import contextlib


class LazyList:
    def __init__(self, iterable):
        self._iterable = iterable
        self._list = []

    def __len__(self):
        return LazyLen(self)

    def __bool__(self):
        self._consume_to(0)
        return bool(self._list)

    def _consume_to(self, index):
        index -= len(self._list)
        with contextlib.suppress(StopIteration):
            for _ in range(index):
                self._list.append(next(self._iterable))

    def _consume_all(self):
        self._list.extend(self._iterable)


# class LazyLen(int):
#     def __new__(cls, *args, **kwargs):
#         return super(LazyLen, cls).__new__(cls, 0)
class LazyLen:

    def __init__(self, lazylist):
        self._lazylist = lazylist

    def __bool__(self):
        return bool(self._lazylist)

    def __int__(self):
        return self.__index__()

    def __index__(self):
        self._lazylist._consume_all()
        return len(self._lazylist._list)

    def __gt__(self, other):
        self._lazylist._consume_to(other + 1)
        return len(self._lazylist._list) > other

    def __lt__(self, other):
        self._lazylist._consume_to(other + 1)
        return len(self._lazylist._list) < other

    def __ge__(self, other):
        self._lazylist._consume_to(other)
        return len(self._lazylist._list) >= other

    def __le__(self, other):
        self._lazylist._consume_to(other)
        return len(self._lazylist._list) >= other

    def __repr__(self):
        return str(self.__index__())

    def __str__(self):
        return str(self.__index__())


def len(collection):
    return collection.__len__()


if __name__ == '__main__':
    import itertools

    ll = LazyList(itertools.cycle([1, 2, 3]))
    ln = LazyLen(ll)

    print(bool(ll))

    print(len(ll) > 1)
    print(ln > 3)
