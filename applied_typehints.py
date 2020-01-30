import functools
import typing


T = typing.TypeVar('T')
U = typing.TypeVar('U')

def apply(applied_fn: typing.Callable[[T], U]) -> typing.Callable[[typing.Callable[..., T]], typing.Callable[..., U]]:  # oof
    """
    Decorator to apply a given function to the output of the decorated function.

    Useful for functions with many returns that require an unconditional
    transformation, or for generator functions that should always return
    a list or other aggregation.
    """
    def decorator(decorated_fn: typing.Callable[..., T]) -> typing.Callable[..., U]:
        @functools.wraps(decorated_fn)
        def inner(*args: typing.Any, **kwargs: typing.Any) -> U:
            return applied_fn(decorated_fn(*args, **kwargs))
        return inner
    return decorator


@apply(list)
def foo():
    yield 5
    yield 6


@apply
def not_(value: typing.Any) -> bool:
    """Decorator that boolean-negates the result of the decorated function."""
    return not value

# ---

def is_foo(string: str) -> bool:
    return string == 'foo'


is_not_foo = not_(is_foo)  # is_not_foo is not a boolean!
print(is_not_foo("foo"))
