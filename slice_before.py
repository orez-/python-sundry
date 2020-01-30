import more_itertools


def _take_until(iterable: more_itertools.peekable, predicate):
    try:
        yield next(iterable)
        while not predicate(iterable.peek()):
            yield next(iterable)
    except StopIteration:
        return


def slice_before(iterable, predicate):
    iterable = more_itertools.peekable(iterable)

    while iterable:
        slice_ = _take_until(iterable, predicate)
        yield slice_
        more_itertools.consume(slice_)


if __name__ == '__main__':
    result = slice_before('abcdefghijklmnopqrstuvwxyz', lambda x: x in 'aeiou')
    print(result)  # generator
    value = next(result)
    print(value)  # generator
    print(list(value))  # abcd
    value = next(result)
    print(next(value))  # e
    value = next(result)
    print(list(value))  # ijklmn
    value = next(result)  # -u
    value = next(result)  # -z
    print(list(value))


    print(list(slice_before('', lambda x: x in 'aeoiu')))
