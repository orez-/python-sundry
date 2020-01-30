# https://www.hillelwayne.com/post/negatypes/
import abc


class ABCComposable(abc.ABCMeta):
    def __and__(self, other):
        def and_(cls, c):
            return issubclass(c, self) and issubclass(c, other)
        name = f"{self.__name__} & {other.__name__}"
        return ABCComposable(name, (abc.ABC,), {'__subclasshook__': classmethod(and_)})

    def __rand__(self, other):
        def and_(cls, c):
            return issubclass(c, other) and issubclass(c, self)
        name = f"{other.__name__} & {self.__name__}"
        return ABCComposable(name, (abc.ABC,), {'__subclasshook__': classmethod(and_)})

    def __or__(self, other):
        def or_(cls, c):
            return issubclass(c, self) or issubclass(c, other)
        name = f"{self.__name__} | {other.__name__}"
        return ABCComposable(name, (abc.ABC,), {'__subclasshook__': classmethod(or_)})

    def __ror__(self, other):
        def or_(cls, c):
            return issubclass(c, other) or issubclass(c, self)
        name = f"{other.__name__} | {self.__name__}"
        return ABCComposable(name, (abc.ABC,), {'__subclasshook__': classmethod(or_)})

    def __invert__(self):
        def not_(cls, c):
            return not issubclass(c, self)
        name = f"~{self.__name__}"
        return ABCComposable(name, (abc.ABC,), {'__subclasshook__': classmethod(not_)})


def abcc(cls):
    def proxy(_, c):
        return issubclass(c, cls)
    return ABCComposable(cls.__name__, (), {'__subclasshook__': classmethod(proxy)})


if __name__ == '__main__':
    import collections.abc


    class One(metaclass=ABCComposable):
        ...


    class Two(metaclass=ABCComposable):
        ...


    class OneAndTwo(One, Two):
        ...


    assert isinstance(One(), One | Two)
    assert isinstance(Two(), One | Two)
    assert isinstance(OneAndTwo(), One | Two)
    assert not isinstance(One(), One & Two)
    assert not isinstance(Two(), One & Two)
    assert isinstance(OneAndTwo(), One & Two)
    assert not isinstance(One(), ~One)
    assert isinstance(One(), ~Two)
    assert isinstance(One(), One & ~Two)
    assert not isinstance(OneAndTwo(), One & ~Two)
    print(One & Two)
    print(One | Two)
    print(~One)
    print(One & ~Two)

    IterableNotString = collections.abc.Iterable & ~abcc(str)
    print(IterableNotString)
    assert isinstance([], IterableNotString)
    assert isinstance(range(10), IterableNotString)
    assert isinstance((x for x in range(10)), IterableNotString)
    assert not isinstance("lol", IterableNotString)
