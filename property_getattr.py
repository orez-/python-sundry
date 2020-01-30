# Problem: AttributeErrors within a @property method are caught and
# suppressed by the class's `__getattr__`.

class Foo1:
    """Class which returns 'foo' on bad attribute lookup."""

    def __getattr__(self, key):
        return 'foo'

    @property
    def bar(self):
        return None.baz


print(Foo1().nonsense)
print(Foo1().bar)  # should raise an AttributeError, but is suppressed by `__getattr__`


# "Solution":
class PropertyAttributeError(Exception):
    """Raised when a @GetattrSafeProperty method raises an AttributeError."""


class GetattrSafeProperty:
    """
    Drop-in replacement for built-in `property` class, which replaces
    AttributeErrors with PropertyAttributeError.
    """
    def __init__(self, fn):
        self._fn = fn

    def __get__(self, instance, owner):
        if not instance:
            return self
        try:
            return self._fn(instance)
        except AttributeError as e:
            raise PropertyAttributeError from e


class GetattrSafePropertyMeta(type):
    """
    Metaclass to make @property methods on a class with __getattr__
    raise PropertyAttributeError instead of AttributeError.
    """
    def __prepare__(cls, bases, **kwargs):
        return {'property': GetattrSafeProperty}


class Foo2(metaclass=GetattrSafePropertyMeta):
    """Class which returns 'foo' on bad attribute lookup."""

    def __getattr__(self, key):
        return 'foo'

    @property
    def bar(self):
        return None.baz


print(Foo2().nonsense)
print(Foo2().bar)  # raises a PropertyAttributeError with meaningful error traceback
