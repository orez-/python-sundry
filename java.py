import inspect


class DispatchFn:
    def __init__(self, parent, initial_value):
        self.parent = parent
        self.fns = [initial_value]

    def add_fn(self, fn):
        self.fns.append(fn)

    def __call__(self, *args, **kwargs):
        for fn in self.fns:
            try:
                sig = inspect.signature(fn).bind(self.parent, *args, **kwargs)
                if any(
                        key in fn.__annotations__ and not isinstance(arg, fn.__annotations__[key])
                        for key, arg in sig.arguments.items()):
                    continue
            except TypeError:
                ...
            else:
                return fn(self.parent, *args, **kwargs)
        params = ", ".join(filter(bool, [
            ", ".join(map(repr, args)),
            ", ".join("{}={!r}".format(key, value) for key, value in kwargs.items()),
        ]))
        raise TypeError("no suitable method found for {}({})".format(fn.__name__, params))


class DispatchDict(dict):
    def __init__(self, parent):
        self.parent = parent

    def __setitem__(self, key, value):
        if key in self:
            if not isinstance(self[key], DispatchFn):
                super().__setitem__(key, DispatchFn(self.parent, self[key]))
            self[key].add_fn(value)
        else:
            super().__setitem__(key, value)


class MetaDispatch(type):
    def __prepare__(self, bases, **kwargs):
        return DispatchDict(self)

# ---

class Baz(metaclass=MetaDispatch):
    def foo(self, *, baz: int):
        print("int baz", baz)

    def foo(self, *, baz):
        print("nonint baz", baz)

    def foo(self, one):
        print("one", one)

    def foo(self, one, two):
        print("two", one, two)


f = Baz()
print(f.foo)

f.foo("un", "dos")
f.foo("ayy")
f.foo(baz="foob")
f.foo(baz=80)
f.foo(1, 2, 3)
