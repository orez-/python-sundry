def side_effect(fn, iterable):
    """
    Like `map`, but yields the element.
    """
    for elem in iterable:
        fn(elem)
        yield elem


class lazy_product:
    def __init__(self, *args):
        # no repeat.
        self.restart_lists = [[] for _ in args]
        self.iters = [
            side_effect(rlist.append, arg)
            for arg, rlist in zip(args, self.restart_lists)
        ]
        try:
            self.values = [next(it) for it in self.iters]
        except StopIteration:
            self.done = True
            return
        self.done = False
        self.stepper = range(len(self.iters))[::-1]

    def __iter__(self):
        return self

    def __next__(self):
        if self.done:
            raise StopIteration
        return_value = tuple(self.values)
        self.done = self._step()
        return return_value

    def _step(self):
        for i in self.stepper:
            try:
                self.values[i] = next(self.iters[i])
                return False
            except StopIteration:
                self.iters[i] = iter(self.restart_lists[i])
                self.values[i] = next(self.iters[i])
        return True

# ---

import itertools

for a, b, c in lazy_product(itertools.count(), 'abc', '369'):
    if a == 20:
        break
    print(a, b, c)
