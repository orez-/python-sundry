# Create a list of tuples of iterable, key function through unnecessary currying
def spooky_scurry(i=None, k=None):
    def _inner(iterable=None, key_fn=None):
        if iterable is None:
            return _inner.values

        if key_fn is None:
            key_fn = lambda x: x

        _inner.values.append((iterable, key_fn))
        return _inner
    _inner.values = []
    return _inner(i, k)


spooky_scurry([1, 2, 3])(["a", "bb", "ccc"], len)()


iter_key_list = (
    spooky_scurry
    ([1, 2, 3])
    (["a", "bb", "ccc"], len)
)()
print(iter_key_list)


# print reduce(lambda a, n: a(*n), args, spooky_scurry)()
