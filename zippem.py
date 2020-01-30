import more_itertools


def advance_past(peekable, threshold, default):
    while peekable and peekable.peek()[0] < threshold:
        next(peekable)
    if peekable:
        return peekable.peek()
    return default


def zip_monotonic(walker, *iters, default=None):
    zipped = zip_monotonic_with_data(
        walker,
        *[([elem] for elem in iter_) for iter_ in iters],
        default=default,
    )
    for walk, *rest in zipped:
        yield (walk, *(elem for elem, in rest))


def zip_monotonic_with_data(walker, *iters, default=None):
    iters = list(map(more_itertools.peekable, iters))
    for walk in walker:
        values = (advance_past(iter_, walk, default) for iter_ in iters)
        yield (walk, *values)
