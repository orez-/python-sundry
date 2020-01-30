import collections
import operator


# Bind stuff largely copied from `bind_partial.py`
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

    def __call__(self, *args, **kwgs):
        arg_strs = list(map(repr, args))
        kwg_strs = [f"{key!s}={value!r}" for key, value in kwgs.items()]
        return BindExpression(
            fn=lambda kwargs: None,
            with_repr=f"{self!r}({', '.join(arg_strs + kwg_strs)})",
            bind_keys=(
                self._bind_keys |
                {key for arg in args for key in getattr(arg, '_bind_keys', [])} |
                {key for kwg in kwgs for key in getattr(kwg, '_bind_keys', [])}
            ),
        )

    def __getattr__(self, key):
        return BindExpression(
            fn=lambda kwargs: None,
            with_repr=f"{self!r}.{key!s}",
            bind_keys=self._bind_keys,
        )

    # __contains__ converts to boolean!! rip
    # def __contains__(self, other):
    #     return BindExpression(
    #         fn=lambda kwargs: None,
    #         with_repr=f"{other!r} in {self!r}",
    #         bind_keys=self._bind_keys,
    #     )

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

    def __eq__(self, right):
        return self._binary_op(
            right=right,
            operation=operator.eq,
            with_repr=f"{self!r} == {right!r}",
        )

    def __req__(self, left):
        return BindExpression(
            fn=lambda kwargs: left == self._bind(kwargs),
            with_repr=f"{left!r} == {self!r}",
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
        return self._identifier


class defaultdict(collections.defaultdict):
    """
    A subclass of defaultdict that calls the default function with the
    missing key as an argument.
    """
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            self[key] = self.default_factory(key)
            return self[key]


class BodySnatcherMeta(type):
    def __prepare__(cls, bases, **kwargs):
        return defaultdict(bind)

# ---

class RuleSet1(metaclass=BodySnatcherMeta):
    rule1 = foo == list(bar) + [baz]


# class Query(metaclass=BodySnatcherMeta):
#     query = wp.models.SalesOrder.id in sales_order_ids
    # query = wp.models.SalesOrder.filter(
    #     wp.models.SalesOrder.id in sales_order_ids,
    #     wp.models.SalesOrder.customer_id == customer_id,
    # )


print(RuleSet1.rule1)
print(Query.query)
