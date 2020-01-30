import functools
import itertools
import operator


def xor_sum(iterable):
    return functools.reduce(operator.xor, iterable, 0)


class SpragueGrundyGenerator:
    # https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem
    def __init__(self):
        self._numbers = [0, 1, 2]
        self._iter = self._generator()

    def _generator(self):
        for num in itertools.count(len(self._numbers)):
            values = set(
                xor_sum(self._numbers[s] for s in splits)
                for splits in split_pins(num)
            )

            # Get the mex
            # I don't understand what the mex represents.
            for m in itertools.count(0):
                if m not in values:
                    break
            self._numbers.append(m)
            yield m

    def get(self, value):
        while len(self._numbers) <= value:
            next(self._iter)
        return self._numbers[value]


sgg = SpragueGrundyGenerator()


def ilen(iterable):
    return sum(1 for _ in iterable)


def _split_pins(num):
    for i in range(num // 2 + 1):
        yield [i, num - i]


def split_pins(num):
    yield from _split_pins(num - 1)
    yield from _split_pins(num - 2)


def fucking_magic(pins_string):
    return bool(xor_sum(
        sgg.get(ilen(iterable))
        for key, iterable in itertools.groupby(pins_string)
        if key == 'I'
    ))


if __name__ == '__main__':
    for _ in range(int(input())):
        input()
        print("WIN" if fucking_magic(input()) else "LOSE")
