import six


class DoNotSetMeta(type):
    def __new__(cls, name, bases, attrs):
        print(attrs)
        if 'donotset' in attrs:
            raise Exception("ofuk")
        return super(DoNotSetMeta, cls).__new__(cls, name, bases, attrs)


class Foo(object):
    def __init__(self):
        self.foo = 4


@six.add_metaclass(DoNotSetMeta)
class Bar(Foo):
    pass


class Baz(Bar):
    donotset = 10
