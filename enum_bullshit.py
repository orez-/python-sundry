from __future__ import print_function

import enum


class Enum(enum.Enum):
    def __new__(cls, *args):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class EnumBullshit(Enum):
    none = ()
    one = "One"
    two = ("1", "2")
    no_alias_pls = ()


print(EnumBullshit.none.value)
print(EnumBullshit.one.value)
print(EnumBullshit.two.value)
print(EnumBullshit.none == EnumBullshit.no_alias_pls)
