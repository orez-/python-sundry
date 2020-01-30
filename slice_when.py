import itertools


def slice_when(iterable, predicate):
    """
    Chunk `iterable` between elements that satisfy `predicate`.

    This method splits each chunk by passing adjacent elements from the iterable into `predicate`.
    Splits occur where `predicate` returns true for adjacent elements.

    a = [1, 2, 4, 9, 10, 11, 12, 15, 16, 19, 20, 21]
    b = slice_when(a, lambda i, j: i+1 != j)
    # b = [[1, 2], [4], [9, 10, 11, 12], [15, 16], [19, 20, 21]]
    c = (','.join(map(str, i)) if len(i) < 3 else '{}-{}'.format(i[0], i[-1]) for i in b)
    # c = ["1,2", "4", "9-12", "15,16", "19-21"]
    d = ','.join(c)
    # d = "1,2,4,9-12,15,16,19-21"

    http://ruby-doc.org/core-2.2.3/Enumerable.html#method-i-slice_when
    """
    one, two = itertools.tee(iter(iterable))
    next(two)
    chunk = []
    for after, before in zip(two, one):
        chunk.append(before)
        if predicate(before, after):
            yield chunk
            chunk = []
    chunk.append(next(one))
    yield chunk
