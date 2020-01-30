try:
    y = reversed(enumerate(range(5, 15, 2)))
except TypeError:
    print("A problem.")


class enumerate(enumerate):
    def __init__(self, iterable, start=0):
        self.iterable = iterable
        self.start = start

    def __reversed__(self):
        try:
            rev_iter = self.iterable.__reversed__
            end = self.iterable.__len__
        except AttributeError:
            # Standard explosion
            return super().__reversed__()

        i = end() + self.start - 1
        for elem in rev_iter():
            yield i, elem
            i -= 1


x = reversed(enumerate(range(5, 15, 2)))
print("A solution!")
print(list(x))
