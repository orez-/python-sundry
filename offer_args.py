import inspect


def offer_args(fn, kwargs):
    """
    Invoke function with **kwargs, omitting unexpected kwargs.
    """
    sig = inspect.signature(fn)

    to_kwargs = {}
    for name, param in sig.parameters.items():
        if param.kind == param.VAR_KEYWORD:
            return fn(**kwargs)
        if name in kwargs:
            to_kwargs[name] = kwargs[name]
    return fn(**to_kwargs)

# ---

import pytest

def test_regular():
    def foo(one, three):
        return one, three

    kwargs = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4}
    assert offer_args(foo, kwargs) == (1, 3)


def test_kwargs():
    def bar(one, three, **four):
        return one, three, four

    kwargs = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4}
    assert offer_args(bar, kwargs) == (1, 3, {'zero': 0, 'two': 2, 'four': 4})


def test_no_args():
    def nawrgs():
        return True

    kwargs = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4}
    assert offer_args(nawrgs, kwargs) is True


def test_all_args():
    def all_args(zero, one, two, three, four):
        return zero, one, two, three, four

    kwargs = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4}
    assert offer_args(all_args, kwargs) == (0, 1, 2, 3, 4)


def test_bad():
    def bad(one, whoops):
        return one, whoops

    kwargs = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4}
    with pytest.raises(TypeError):
        offer_args(bad, kwargs)


def test_ok():
    def ok(one, whoops=5):
        return one, whoops

    kwargs = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4}
    assert offer_args(ok, kwargs) == (1, 5)
