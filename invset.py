class InvSet:
    """
    Inverse Set: a set which contains all values _except_ those specified.

    Interoperable with builtin `set` and `frozenset` classes wherever possible.

    Is not iterable: how would you iterate all values??
    """
    def __new__(self, iterable=()):
        if isinstance(iterable, InvSet):
            return set(iterable._excluded)
        return super().__new__(self)

    def __init__(self, iterable=()):
        self._excluded = set(iterable)

    def __contains__(self, value):
        return value not in self._excluded

    def __invert__(self):
        return set(self._excluded)

    def __sub__(self, other):
        return InvSet(self._excluded | other)

    def __rsub__(self, other):
        return other & self._excluded

    def __and__(self, other):
        return other - self._excluded

    def __rand__(self, other):
        return self & other

    def __or__(self, other):
        return InvSet(self._excluded - other)

    def __ror__(self, other):
        return self | other

    def __xor__(self, other):
        return InvSet(self._excluded ^ other)

    def __rxor__(self, other):
        return self ^ other

    def __lt__(self, other):
        if isinstance(other, (set, frozenset)):
            return False
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._excluded > other._excluded

    def __gt__(self, other):
        if isinstance(other, (set, frozenset)):
            return self._excluded.isdisjoint(other)
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._excluded < other._excluded

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def isdisjoint(self, other):
        if isinstance(other, InvSet):
            return False
        return not any(value in self for value in other)

    def __repr__(self):
        return f"{type(self).__name__}({self._excluded})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._excluded == other._excluded

    def copy(self):
        return InvSet(self._excluded)

    def add(self, elem):
        self._excluded.discard(elem)

    def remove(self, elem):
        if elem in self._excluded:
            raise KeyError(elem)
        self._excluded.add(elem)

    def discard(self, elem):
        self._excluded.add(elem)

# ---

import pytest


def test_cloney():
    s = {3, 4}
    inv = InvSet(s)
    s.add(5)
    assert inv == InvSet({3, 4})


def test_in():
    assert 2 in InvSet({3, 4})


def test_not_in():
    assert 3 not in InvSet({3, 4})


def test_negate():
    values = {1, 2, 3}
    invset = InvSet(values)
    assert ~invset == values


@pytest.mark.parametrize("left,right,expected", [
    ({1, 2, 3}, InvSet({1, 2, 4}), {1, 2}),
    (InvSet({1, 2, 4}), {1, 2, 3}, InvSet({1, 2, 3, 4})),
    (InvSet({1, 2}), InvSet({2, 3}), {3}),
])
def test_sub(left, right, expected):
    assert left - right == expected


@pytest.mark.parametrize("left,right,expected", [
    ({1, 2, 3}, InvSet({1, 2, 4}), {3}),
    (InvSet({4, 5, 6}), {5, 6, 7, 8}, {7, 8}),
    (InvSet({4, 5, 6}), InvSet({6, 7, 8}), InvSet({4, 5, 6, 7, 8})),
])
def test_and(left, right, expected):
    assert left & right == expected


@pytest.mark.parametrize("left,right,expected", [
    ({1, 2, 4}, InvSet({1, 2, 3}), InvSet({3})),
    (InvSet({4, 5, 6}), {5, 6, 7, 8}, InvSet({4})),
    (InvSet({4, 5, 6}), InvSet({6, 7, 8}), InvSet({6})),
])
def test_or(left, right, expected):
    assert left | right == expected


@pytest.mark.parametrize("left,right,expected", [
    (InvSet({1, 2, 3}), {2, 3}, True),
    (InvSet({1, 2, 3}), {2, 4}, False),
    # can't really monkeypatch `set` :(
    # ({2, 3}, InvSet({1, 2, 3}), True),
    # ({2, 4}, InvSet({1, 2, 3}), False),
    (InvSet({1, 2, 3}), InvSet({3, 4, 5}), False),
])
def test_isdisjoint(left, right, expected):
    assert left.isdisjoint(right) == expected


@pytest.mark.parametrize("left,right,expected", [
    ({1, 2, 4}, InvSet({1, 2, 3}), InvSet({3, 4})),
    (InvSet({4, 5, 6}), {5, 6, 7, 8}, InvSet({4, 7, 8})),
    (InvSet({4, 5, 6}), InvSet({6, 7, 8}), {4, 5, 7, 8}),
])
def test_xor(left, right, expected):
    assert left ^ right == expected


@pytest.mark.parametrize("left,right,expected", [
    (InvSet({1, 2}), InvSet({3, 4}), False),
    (InvSet({1, 2, 3, 4}), InvSet({2, 3}), True),
    (InvSet({1, 2, 3}), InvSet({2, 3, 4}), False),
    (InvSet({1, 2}), {3, 4}, False),
    ({3, 4}, InvSet({1, 2}), True),
    (InvSet({1, 2}), InvSet({1, 2}), False),
])
def test_lt(left, right, expected):
    assert (left < right) == expected


@pytest.mark.parametrize("left,right,expected", [
    (InvSet({3, 4}), InvSet({1, 2}), False),
    (InvSet({2, 3}), InvSet({1, 2, 3, 4}), True),
    (InvSet({2, 3, 4}), InvSet({1, 2, 3}), False),
    (InvSet({1, 2}), {3, 4}, True),
    ({3, 4}, InvSet({1, 2}), False),
    (InvSet({1, 2}), InvSet({1, 2}), False),
])
def test_gt(left, right, expected):
    assert (left > right) == expected


@pytest.mark.parametrize("left,right,expected", [
    (InvSet({1, 2}), InvSet({3, 4}), False),
    (InvSet({1, 2, 3, 4}), InvSet({2, 3}), True),
    (InvSet({1, 2, 3}), InvSet({2, 3, 4}), False),
    (InvSet({1, 2}), {3, 4}, False),
    ({3, 4}, InvSet({1, 2}), True),
    (InvSet({1, 2}), InvSet({1, 2}), True),
])
def test_lte(left, right, expected):
    assert (left <= right) == expected


@pytest.mark.parametrize("left,right,expected", [
    (InvSet({3, 4}), InvSet({1, 2}), False),
    (InvSet({2, 3}), InvSet({1, 2, 3, 4}), True),
    (InvSet({2, 3, 4}), InvSet({1, 2, 3}), False),
    (InvSet({1, 2}), {3, 4}, True),
    ({3, 4}, InvSet({1, 2}), False),
    (InvSet({1, 2}), InvSet({1, 2}), True),
])
def test_gte(left, right, expected):
    assert (left >= right) == expected


def test_copy():
    invs = InvSet({1, 2, 3})


@pytest.mark.parametrize("invset,value,expected", [
    (InvSet({1, 2}), 2, InvSet({1})),
    (InvSet({1, 2}), 3, InvSet({1, 2})),
])
def test_add(invset, value, expected):
    invset.add(value)
    assert invset == expected


def test_remove():
    inv = InvSet({1, 2})
    inv.remove(3)
    assert inv == InvSet({1, 2, 3})


def test_bad_remove():
    inv = InvSet({1, 2})
    with pytest.raises(KeyError):
        inv.remove(2)


@pytest.mark.parametrize("invset,value,expected", [
    (InvSet({1, 2}), 2, InvSet({1, 2})),
    (InvSet({1, 2}), 3, InvSet({1, 2, 3})),
])
def test_discard(invset, value, expected):
    invset.discard(value)
    assert invset == expected


@pytest.mark.parametrize("fn", [
    lambda: InvSet({1, 2}) - 5,
    lambda: 5 - InvSet({1, 2}),
    lambda: InvSet({1, 2}) & 5,
    lambda: 5 & InvSet({1, 2}),
    lambda: InvSet({1, 2}) | 5,
    lambda: 5 | InvSet({1, 2}),
    lambda: InvSet({1, 2}) ^ 5,
    lambda: 5 ^ InvSet({1, 2}),
    lambda: InvSet({1, 2}) < 5,
    lambda: 5 < InvSet({1, 2}),
    lambda: InvSet({1, 2}) > 5,
    lambda: 5 > InvSet({1, 2}),
    lambda: InvSet({1, 2}) <= 5,
    lambda: 5 <= InvSet({1, 2}),
    lambda: InvSet({1, 2}) >= 5,
    lambda: 5 >= InvSet({1, 2}),
])
def test_operator_type_error(fn):
    with pytest.raises(TypeError) as exc:
        fn()
