import operator


class BindMeta(type):
    """
    Metaclass for the `bind` class. Enables generating `bind`s by getting
    the attribute with the desired identifier from the `bind` class directly.
    """
    def __getattr__(cls, key):
        return cls(key)


class BindExpression:
    def __init__(self, fn, bind_keys, with_repr):
        self._bind_keys = bind_keys
        self._fn = fn
        self._repr = with_repr

    def __call__(self, **kwargs):
        """
        Bind some or all vars to the BindExpression.

        If all vars in the expression are bound, the final result is returned.
        """
        if not kwargs:
            raise TypeError("at least one bound parameter must be passed")
        extra_keys = kwargs.keys() - self._bind_keys
        if extra_keys:
            raise TypeError("got unexpected keyword arguments: {}".format(
                ', '.join(map(repr, extra_keys))
            ))
        return self._bind(kwargs)

    def _bind(self, kwargs):
        """
        Bind the passed kwargs to this expression.
        """
        # Small optimization: if there's nothing else to fill, return the original.
        if self._bind_keys.isdisjoint(kwargs.keys()):
            return self
        return self._fn(kwargs)

    def _binary_op(self, right, operation, with_repr):
        """
        Helper function for defining binary operations (but not their reverse).

        Handles evaluation appropriately depending on if `right` is also a BindExpression.
        """
        if isinstance(right, BindExpression):
            return BindExpression(
                fn=lambda kwargs: operation(self._bind(kwargs), right._bind(kwargs)),
                with_repr=with_repr,
                bind_keys=self._bind_keys | right._bind_keys,
            )
        return BindExpression(
            fn=lambda kwargs: operation(self._bind(kwargs), right),
            with_repr=with_repr,
            bind_keys=self._bind_keys,
        )

    def __repr__(self):
        return self._repr

    # Start of boilerplate dunder methods.

    def __getitem__(self, key):
        """
        Since there's no __rgetitem__, key may not be a BindExpression.
        """
        return BindExpression(
            fn=lambda kwargs: self._bind(kwargs)[key],
            with_repr=f"{self!r}[{key!r}]",
            bind_keys=self._bind_keys,
        )

    def __abs__(self):
        return BindExpression(
            fn=lambda kwargs: abs(self._bind(kwargs)),
            with_repr=f"abs({self!r})",
            bind_keys=self._bind_keys,
        )

    def __add__(self, right):
        return self._binary_op(
            right=right,
            operation=operator.add,
            with_repr=f"{self!r} + {right!r}",
        )

    def __radd__(self, left):
        # __add__ takes care of the case where `left` is a BindExpression
        return BindExpression(
            fn=lambda kwargs: left + self._bind(kwargs),
            with_repr=f"{left!r} + {self!r}",
            bind_keys=self._bind_keys,
        )

    def __divmod__(self, right):
        return self._binary_op(
            right=right,
            operation=divmod,
            with_repr=f"divmod({self!r}, {right!r})",
        )

    def __rdivmod__(self, left):
        return BindExpression(
            fn=lambda kwargs: divmod(left, self._bind(kwargs)),
            with_repr=f"divmod({left!r}, {self!r})",
            bind_keys=self._bind_keys,
        )


class bind(BindExpression, metaclass=BindMeta):
    def __init__(self, identifier):
        self._identifier = identifier
        self._bind_keys = frozenset({identifier})

    def _bind(self, kwargs):
        # Changing this to a `while` would allow specifying binds in terms
        # of other binds, but then we'd probably want to prevent cyclic
        # references. More trouble than it's worth.
        if self._identifier in kwargs:
            return kwargs[self._identifier]
        return self

    def __repr__(self):
        return f'bind.{self._identifier}'


# ---

def test_identity():
    identity = bind.value
    assert identity(value=10) == 10


def test_adding():
    doubler = bind.value + bind.value
    assert doubler(value=10) == 20


def test_adding_const():
    and5 = bind.value + 5
    assert and5(value=10) == 15


def test_adding_const():
    fiveand = 5 + bind.value
    assert fiveand(value=10) == 15


def test_complex():
    manhattan_distance = abs(bind.coord['x']) + abs(bind.coord['y'])
    assert manhattan_distance(coord={'x': 2, 'y': -3}) == 5


def test_two_bind():
    summer = bind.left + bind.right
    assert summer(left=1, right=2) == 3
    assert summer(left=2)(right=3) == 5
    assert summer(right=3)(left=5) == 8


if __name__ == '__main__':
    manhattan_distance = abs(bind.coord['x']) + abs(bind.coord['y'])
    floating_z = manhattan_distance + abs(bind.z)
    print(floating_z)
    print(floating_z(z=10))
    print(floating_z(coord={'x': -10, 'y': 12}))
