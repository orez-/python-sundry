import collections


# this is just a shittier itertools.groupby that uses comprehensions
# instead of keyfunctions

class schmefault_dict(collections.defaultdict):
    def __init__(self, type_, initial=None):
        if isinstance(initial, dict):
            super(schmefault_dict, self).__init__(type_, initial)
            return

        super(schmefault_dict, self).__init__(type_)
        if initial is None:
            return

        method = {
            set: set.add,
            list: list.append,
        }[type_]

        for key, value in initial:
            method(self[key], value)


print(schmefault_dict(list, ((x // 5, x) for x in xrange(100))))
print()
print(schmefault_dict(set, ((x // 5, x) for x in xrange(100))))
print()
print(schmefault_dict(list, {1: [5, 6, 7], 2: [6, 7, 8]}))
print()
print(schmefault_dict(set))
