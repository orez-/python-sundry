import collections
import functools
import inspect
import textwrap


def get_parameters_by_kind(fn):
    """
    Get a function's parameter names grouped by their `kind`.

    As a convenience, *args and **kwargs are delisted, since there can
    be at most one of each.
    """
    params = collections.defaultdict(list)
    for key, parameter in inspect.signature(fn).parameters.items():
        params[parameter.kind].append(key)
    params = dict(params)

    # Delist *args and **kwargs
    for kind in [inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD]:
        if kind in params:
            (params[kind],) = params[kind]
    return params


def demote_var_keyword(fn):
    """
    Return the given function with its **var_keyword parameter converted
    to a regular non-splatted argument.

        foo(a, *b, c, **d) -> foo(a, *b, c, d)

    This function makes use of some serious eval magic to achieve this.
    It should not be used by anyone.
    """
    source = inspect.getsource(fn)
    source = textwrap.dedent(source)

    # remove decorators
    while source.startswith('@'):
        _, source = source.split('\n', 1)

    # replace `**kwargs` with `kwargs`
    # XXX: this is not a foolproof replacement
    kwargs_name = get_parameters_by_kind(fn).get(inspect.Parameter.VAR_KEYWORD)
    if kwargs_name:
        source = source.replace(f'**{kwargs_name}', kwargs_name, 1)

    # compile the source code into a new function and return it
    code = compile(source, 'anything', 'exec')
    globals_collector = {}
    eval(code, {}, globals_collector)
    return globals_collector[fn.__name__]


def enforce_positional(fn):
    """
    Decorator to mark and enforce any non-keyword-only parameters as positional-only.

    By enforcing parameters as positional-only, we're also able to avoid
    named parameter collisions when collecting **kwargs:

        class Foo:
            @enforce_positional
            def method(self, **kwargs):
                ...

        Foo().method(self=0)

    This function makes use of some dark eval magic and should never be
    used by anyone. In particular this decorator makes no promises about
    playing nicely with REPLs, lambdas, default arguments, annotations,
    or other decorators.
    """
    # fn(a, *b, c, **d) -> fn(a, *b, c, d)
    # anon(*args, **kwargs) splits out d and calls fn

    params = get_parameters_by_kind(fn)

    kw_only_keys = params.get(inspect.Parameter.KEYWORD_ONLY, ())
    kwargs_name = params.get(inspect.Parameter.VAR_KEYWORD)
    kwargsless_fn = demote_var_keyword(fn)

    # Mark parameters as positional only.
    # Python provides a built-in way to mark parameters as positional
    # only, despite not offering a way to define or enforce this.
    # Currently this just changes the way the function's signature
    # displays, eg with ipython's `foo?`.
    sig = inspect.signature(fn)
    translation = {inspect.Parameter.POSITIONAL_OR_KEYWORD: inspect.Parameter.POSITIONAL_ONLY}
    fn.__signature__ = sig.replace(parameters=[
        param.replace(kind=translation.get(param.kind, param.kind))
        for param in sig.parameters.values()
    ])

    @functools.wraps(fn)
    def anon(*args, **kwargs):
        known_keys = {key: kwargs.pop(key) for key in kw_only_keys if key in kwargs}
        if kwargs_name:
            known_keys[kwargs_name] = kwargs
        return kwargsless_fn(*args, **known_keys)

    return anon

# --

import pytest


def test_bare():
    @enforce_positional
    def foo():
        return 'hi'

    assert foo() == 'hi'


def test_minimal():
    @enforce_positional
    def foo(bar):
        return bar * 2

    assert foo(1) == 2
    with pytest.raises(TypeError):
        foo(bar=1)


def test_kwargsless():
    @enforce_positional
    def foo(bar, *baz, bang):
        return bar, baz, bang

    assert foo(1, 2, 3, bang=4) == (1, (2, 3), 4)
    with pytest.raises(TypeError):
        foo(bar=1, bang=2)


def test_simple():
    @enforce_positional
    def foo(bar, **kwargs):
        return bar, kwargs

    assert foo(1, bar=2) == (1, {'bar': 2})
    with pytest.raises(TypeError):
        foo(bar=1)


def test_tougher():
    @enforce_positional
    def foo(bar, *baz, bang, **kwargs):
        return bar, baz, bang, kwargs

    assert (
        foo(1, 2, 3, bar=4, baz=5, bang=6, boom=7) ==
        (1, (2, 3), 6, {'bar': 4, 'baz': 5, 'boom': 7})
    )
    with pytest.raises(TypeError):
        foo(bar=1, bang=2)


def test_kwarg_collision():
    @enforce_positional
    def foo(bar, *baz, bang, **kwargs):
        return bar, baz, bang, kwargs

    assert (
        foo(1, 2, 3, bar=4, baz=5, bang=6, kwargs=7) ==
        (1, (2, 3), 6, {'bar': 4, 'baz': 5, 'kwargs': 7})
    )


def test_extra_kwarg():
    @enforce_positional
    def foo(bar, baz):
        return bar, baz

    with pytest.raises(TypeError):
        foo(1, 2, bang=3)


def test_accepting_method():
    class Foo:
        @enforce_positional
        def foo(self, **kwargs):
            return self, kwargs

    foo = Foo()
    assert foo.foo(self=1) == (foo, {'self': 1})


def test_demote_var_kw():
    @demote_var_keyword
    def foo(
        one,
        **kwargs
    ):
        return 8

    assert (
        inspect.signature(foo).parameters['kwargs'].kind ==
        inspect.Parameter.POSITIONAL_OR_KEYWORD
    )


def test_demote_var_kw_tougher():
    @demote_var_keyword
    def foo(
        one=lambda **kwargs: 'lol',
        **kwargs
    ):
        return 8

    assert (
        inspect.signature(foo).parameters['kwargs'].kind ==
        inspect.Parameter.POSITIONAL_OR_KEYWORD
    )


def test_lambda():
    foo = demote_var_keyword(lambda one, **kwargs: 8)
    assert (
        inspect.signature(foo).parameters['kwargs'].kind ==
        inspect.Parameter.POSITIONAL_OR_KEYWORD
    )
