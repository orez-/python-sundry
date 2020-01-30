import collections
# import pickle
import cloudpickle as pickle
import typing


def test_one():
    Foo = collections.namedtuple('Foo', 'bar')
    domp = pickle.dumps(Foo(10))
    Foo = collections.namedtuple('Foo', 'bar, baz')
    foo = pickle.loads(domp)
    print(foo.bar)


def test_two():
    class Foo(typing.NamedTuple):
        bar: int

        def __setstate__(self, data):
            print("1ss")

        def __getstate__(self):
            print("1gs")

    domp = pickle.dumps(Foo(10))

    class Foo(typing.NamedTuple):
        bar: int
        baz: str

        def __setstate__(self, data):
            print("2ss")

        def __getstate__(self):
            print("2gs")

    foo = pickle.loads(domp)
    print(foo.bar)
    print(foo._fields)
