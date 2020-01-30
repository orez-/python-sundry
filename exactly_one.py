import functools
import inspect


def conjunction_join(words, conjunction):
    words = list(words)
    if len(words) > 2:
        words[:-1] = [", ".join(words[:-1]) + ","]
    return f" {conjunction} ".join(words)


def exactly_one(*mutex_keys):
    def decorator(fn):
        sig = inspect.signature(fn)
        _mutex_keys = set(mutex_keys)
        for key in _mutex_keys:
            if sig.parameters[key].default is sig.empty:
                raise TypeError(f"parameter {key!r} must have a default")

        @functools.wraps(fn)
        def anon(*args, **kwargs):
            bound_args = sig.bind(*args, **kwargs)
            set_keys = bound_args.arguments.keys() & _mutex_keys
            if not set_keys:
                terms = conjunction_join(map(repr, mutex_keys), conjunction="or")
                raise TypeError(f"One of {terms} must be passed.")
            if len(set_keys) > 1:
                terms = conjunction_join(map(repr, mutex_keys), conjunction="or")
                raise TypeError(f"Only one of {terms} may be passed.")
            return fn(*args, **kwargs)
        return anon
    return decorator


# ---
import pytest


def test_multiple():
    @exactly_one('one', 'two')
    def foo(one=1, two=2):
        return one, two

    with pytest.raises(TypeError):
        foo('ONE', 'TWO')


def test_none():
    @exactly_one('one', 'two')
    def foo(one=1, two=2):
        return one, two

    with pytest.raises(TypeError):
        foo()


def test_many():
    @exactly_one('one', 'two', 'three', 'four')
    def foo(one=1, two=2, three=3, four=4):
        return one, two, three, four

    assert foo(three='THREE') == (1, 2, 'THREE', 4)
