import contextlib


def group_equal(*iterables):
    """
    Make an iterator that returns tuples of equivalent elements from `iterables`.

    The elements of `iterables` are pairs of values and a key function. Generally, the iterables
    need to already be sorted on the same key functions. Yields a tuple of the length of `iterables` of
    individual elements from these iterables which all equal each other (through their respective
    key functions).

    An element of an iterable will be used at most once: the results are not combinatoric.
    No single unique element of an iterable will appear more than once in the output.

    Examples:
        >>> i = lambda x: x
        >>> list(group_equal(
        ...     (range(0, 100, 2), i),
        ...     (range(0, 100, 3), i),
        ...     (range(0, 100, 5), i),
        ... ))
        [[0, 0, 0], [30, 30, 30], [60, 60, 60], [90, 90, 90]]

        >>> list(group_equal(
        ...     (["one", "two", "four", "five", "three"], len),
        ...     ([1, 2, 3, 4, 4, 5], i),
        ...     (["oh", "wow", "holy", "dang"], len),
        ... )
        [('one', 3, 'wow'), ('four', 4, 'holy'), ('five', 4, 'dang')]

    """
    if not iterables:
        return

    iterables, key_fns = zip(*iterables)
    iterables = [iter(i) for i in iterables]

    with contextlib.suppress(StopIteration):
        values = [next(i) for i in iterables]

        while True:
            keys = [key_fn(value) for key_fn, value in zip(key_fns, values)]
            if all(key == keys[0] for key in keys):
                yield tuple(values)
                values = [next(i) for i in iterables]
            else:
                index = min(enumerate(keys), key=lambda x: x[1])[0]
                values[index] = next(iterables[index])
