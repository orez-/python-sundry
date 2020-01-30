class MetaDict(dict):
    no_value = object()

    def __missing__(self, key):
        self[key] = self.no_value
        return self.no_value


class Meta(type):
    def __new__(mcs, name, bases, attrs):
        my_attrs = {
            key: value for key, value in attrs.items()
            if not key.startswith('_')
        }

        the_rest = {
            key: value for key, value in attrs.items()
            if key.startswith('_')
        }

        cls = super().__new__(mcs, name, bases, the_rest)
        # cls.__slots__ = tuple(my_attrs) + ('_fields', '__repr__')
        cls._fields = my_attrs

        def __init__(self, **kwargs):
            for attr, default in my_attrs.items():
                value = kwargs.get(attr, default)
                if value is MetaDict.no_value:
                    raise Exception("missing required value for {!r}".format(attr))
                object.__setattr__(self, attr, value)

        cls.__init__ = __init__

        return cls


    def __prepare__(name, bases, **kwds):
        return MetaDict()


class StructuredObject(metaclass=Meta):
    __slots__ = ()

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                '{}={}'.format(key, getattr(self, key))
                for key in self._fields
            )
        )

    def __setattr__(self, key, value):
        cls = self.__class__.__name__
        raise AttributeError("{!r} object attribute {!r} is read-only".format(cls, key))


# ---
product_id = "foo"

class ItemToAdd(StructuredObject):
    product_id, variant_id, quantity
    display_name = None
    is_takeaway = None
    prescription_request_id = None
    attributes = None
    price_type_id = 1
    price = None


i2a = ItemToAdd(
    product_id=1,
    variant_id=2,
    quantity=3,
)
print(i2a)
print(i2a.price_type_id)
