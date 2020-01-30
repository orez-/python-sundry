"""
PEP 457
"""
import collections
import inspect
import re


class Undefined:
    """Singleton object representing no passed argument."""
    def __bool__(self):
        return False


undefined = Undefined()


class PosSignature:
    def __init__(self, names, groups):
        self.names = names
        self.groups = groups
        self._argcount = {}

    def _fill_positional(self, args):
        ...

    def bind(self, args, kwargs):
        num_args = len(args)
        if num_args >= len(self.posonly):
            ...
        else:
            self._argcount[num_args]


def _parse_signature(pos_signature, fn):
    fn_sig = inspect.signature(fn)
    sig = re.sub(r'\s', '', pos_signature)  # XXX
    parameters = sig.split(',')
    if parameters and not parameters[-1]:  # pop trailing comma
        parameters.pop()

    group_stack = collections.deque()
    groups = []
    names = []

    symbol_level = 0
    fn_params = iter(fn_sig.parameters)

    for param in parameters:
        match = re.fullmatch(r'(\[*)(?:(\/|\*)|(\*{0,2})(\w+))(\]*)', param)
        if not match:
            raise SyntaxError("invalid syntax", (None, 0, 1, param))
        leading, symbol, stars, name, trailing = match.groups()

        if leading and symbol_level:
            raise SyntaxError("groups must be positional-only")
        for _ in leading:
            if group_stack:
                raise NotImplementedError("nested [ ]s are not allowed")
            group_stack.append([])

        if symbol:
            if group_stack:
                raise SyntaxError("groups must be positional-only")
            if symbol == '/':
                if symbol_level > 0:
                    raise SyntaxError("invalid syntax")
                symbol_level = 1
            elif symbol == '*':
                if symbol_level > 1:
                    raise SyntaxError("invalid syntax")
                if symbol_level == 0 and groups:
                    raise SyntaxError("groups must be positional-only")
                symbol_level = 2
            else:
                raise SyntaxError("invalid syntax")
        else:
            if stars:
                raise NotImplementedError(stars)
            if name != next(fn_params, None):
                raise ValueError("parameters must match")

            if group_stack:
                group_stack[-1].append(name)
            names.append(name)

        for _ in trailing:
            groups.append(group_stack.pop())

    if next(fn_params, None):
        raise ValueError("parameters must match")

    return PosSignature(
        positional=0,
        both=0,
        named=0,
        names=0,
        groups=0,
    )
    # positional_only, _, rest = sig.rpartition('/')
    # print(positional_only, rest)


def positional(signature):
    """
    TODO

    - Original function is defined with defaults but no splats
    - `positional` fn takes a matching signature with splats and the
        positional marker but no defaults.
    - If necessary original function can force named arguments (for defaults in any order)
    - positional-only args must be grouped to have a default??
    """
    def inner(fn):
        sig = _parse_signature(signature, fn)
        if list(inspect.signature(fn).parameters) != sig.parameters:
            raise ValueError("Signatures must match.")
        def anon(*args, **kwargs):
            kws = sig.bind(args, kwargs)
            return fn(**kws)
        return anon
    return inner


# ---

import pytest


@pytest.mark.parametrize('args,expected', [
    (['ch'], (undefined, undefined, 'ch', undefined)),
    (['ch', 'attr'], (undefined, undefined, 'ch', 'attr')),
    (['y', 'x', 'ch'], ('y', 'x', 'ch', undefined)),
    (['y', 'x', 'ch', 'attr'], ('y', 'x', 'ch', 'attr')),
])
def test_pep_ex(args, expected):
    @positional('[y, x], ch, [attr], /')
    def addch(y, x, ch, attr):
        return y, x, ch, attr

    assert addch(*args) == expected


@pytest.mark.xfail
@pytest.mark.parametrize('args,kwargs', [
    (['one'], {'self': 50}),
    (['two'], {'self': 100, 'other': 200}),
    (['three'], {'another': 300}),
    (['four'], {}),
])
def test_kwargs(args, kwargs):
    @positional('self, /, **kw')
    def method(self, kw):
        return self, kw

    assert method(*args, **kwargs) == (args, kwargs)


@pytest.mark.xfail
@pytest.mark.parametrize('args', [
    [10],
    [3, 11],
    [6, 12, 3],
])
def test_rangelike(args):
    @positional('[start], end, [step], /')
    def range_(*, start=0, end, step=1):
        return range(start, end, step)

    assert range_(*args) == range(*args)


@pytest.mark.xfail
@pytest.mark.parametrize('args,kwargs', [
    ([], {}),
    ([], {'one': 1, 'two': 2}),
    ([enumerate("cool")], {}),
    ([{'one': 1}], {'two': 2, 'three': 3}),
])
def test_dictlike(args, kwargs):
    @positional('posarg, /, **kw')
    def dict_(posarg, kw):
        if posarg is undefined:
            return dict(**kw)
        else:
            return dict(posarg, **kw)

    assert dict_(*args, **kwargs) == dict(*args, **kwargs)



@pytest.mark.xfail
@pytest.mark.parametrize('args,kwargs,expected', [
    ([], {'three': 3}, (undefined, 2, 3)),
    ([1], {'three': 3}, (1, 2, 3)),
    ([], {'two': 80, 'three': 3}, (undefined, 80, 3)),
    ([1, 80], {'three': 3}, (1, 80, 3)),
    ([1], {'two': 80, 'three': 3}, (1, 80, 3)),
])
def test_mixed(args, kwargs, expected):
    @positional('[one], /, two, *, three')
    def fn(*, one, two=2, three):
        return one, two, three

    assert fn(*args, **kwargs) == expected


@pytest.mark.xfail
@pytest.mark.parametrize('args,kwargs,expected', [
    ([], {}, (undefined, undefined, 3)),
    ([80], {}, (undefined, undefined, 80)),
    ([1, 2], {}, (1, 2, 3)),
    ([1, 2, 80], {}, (1, 2, 80)),
    ([], {'three': 80}, (undefined, undefined, 80)),
    ([1, 2], {'three': 80}, (1, 2, 80)),
])
def test_both_default(args, kwargs, expected):
    @positional('[one, two], /, three')
    def fn(*, one, two, three=3):
        return one, two, three

    assert fn(*args, **kwargs) == expected


@pytest.mark.xfail
@pytest.mark.parametrize('args,expected', [
    ([1, 2], (1, 2)),
    ([2], (undefined, 2)),
])
def test_weird_fill(args, expected):
    @positional('[one], /, two')
    def fn(one, two):
        return one, two

    assert fn(*args) == expected
