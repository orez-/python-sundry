import functools

class OperatorPartial(object):
    def __init__(self, fn, with_repr=None):
        self._fn = fn
        self._repr = with_repr if with_repr is not None else repr(fn)
        functools.update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        """
        Actual invocation of the function.
        """
        return self._fn(*args, **kwargs)

    def __neg__(self):
        return type(self)(
            fn=lambda *args, **kwargs: -self(*args, **kwargs),
            with_repr="-{!r}".format(self),
        )

    def __gt__(self, other):
        return type(self)(
            fn=lambda *args, **kwargs: self(*args, **kwargs) > other,
            with_repr="{!r} > {!r}".format(self, other),
        )

    def __add__(self, other):
        return type(self)(
            fn=lambda *args, **kwargs: self(*args, **kwargs) + other,
            with_repr="{!r} + {!r}".format(self, other),
        )

    def __radd__(self, other):
        return type(self)(
            fn=lambda *args, **kwargs: other + self(*args, **kwargs),
            with_repr="{!r} + {!r}".format(other, self),
        )

    def __divmod__(self, other):
        return type(self)(
            fn=lambda *args, **kwargs: divmod(self(*args, **kwargs), other),
            with_repr="divmod({!r}, {!r})".format(self, other),
        )

    def __rdivmod__(self, other):
        return type(self)(
            fn=lambda *args, **kwargs: divmod(other, self(*args, **kwargs)),
            with_repr="divmod({!r}, {!r})".format(other, self),
        )

    def __abs__(self):
        return type(self)(
            fn=lambda *args, **kwargs: abs(self(*args, **kwargs)),
            with_repr="abs({!r})".format(self),
        )

    def __getitem__(self, other):
        return type(self)(
            fn=lambda *args, **kwargs: self(*args, **kwargs)[other],
            with_repr="{!r}[{!r}]".format(self, other),
        )

    # pretend I added a bunch more operators here

    def __repr__(self):
        return self._repr


@OperatorPartial
def identity(x):
    return x


if __name__ == '__main__':
    __builtins__.len = OperatorPartial(__builtins__.len)

    @OperatorPartial
    def squared(value):
        return value * value

    print(squared)
    print(-squared)
    print(len + 5)

    print((len > 5)("wat"))
    print((len > 5)("wat the fak"))
    print(sorted(["one", "eight", "one billion"], key=len))
    print(sorted(["one", "eight", "one billion"], key=-len))
    print((-squared + 10)(5))

    @OperatorPartial
    def doubled(value):
        return value * 2

    print(squared + doubled)
    print((squared + doubled)(5)(2))

    print(divmod(squared, 5)(3))
    print(divmod(squared, doubled)(3)(4))
    print(divmod(squared, doubled))

    import itertools
    keyfn = identity[0]
    print(keyfn)
    result = itertools.groupby(sorted(['abc', 'bcd', 'axy'], key=keyfn), keyfn)
    print([(key, list(values)) for key, values in result])
