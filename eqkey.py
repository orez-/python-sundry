def eq_key(cls):
    cls.__eq__ = lambda self, other: self._eq_key() == other._eq_key()
    cls.__hash__ = lambda self: hash(self._eq_key())
    return cls


@eq_key
class Foo:
    def __init__(self, value):
        self.value = value

    def _eq_key(self):
        return self.value


print(Foo(5) == Foo(5))
print(Foo(7) == Foo(5))
