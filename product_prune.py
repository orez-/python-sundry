class _Result(list):
    def __init__(self, parent, contents):
        super(_Result, self).__init__(contents)
        self.parent = parent

    def verify(self, aggressive=False):
        for self.parent.interrupted_at, value in enumerate(self, -bool(aggressive)):
            yield value
        self.parent.interrupted_at = None


class sensitive_product(object):
    def __init__(self, *args, **kwds):
        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        self.pools = [tuple(arg) for arg in args] * kwds.get('repeat', 1)
        self.interrupted_at = None
        self.done = not all(self.pools)
        if self.done:
            return
        self.indices = [0 for _ in self.pools]
        self.stepper = range(len(self.pools))[::-1]
        self.cache = [pool[0] for pool in self.pools]
        self.start = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.start:
            self.start = False
        elif self.interrupted_at is not None:
            self.done = self._step(self.interrupted_at)
            self.interrupted_at = None
        else:
            self.done = self._step()

        if self.done:
            raise StopIteration

        result = _Result(self, self.cache)
        return result

    def _step(self, nuke_till=float('inf')):
        for i in self.stepper:
            self.indices[i] += 1
            pool = self.pools[i]
            if self.indices[i] == len(pool) or i > nuke_till:
                self.indices[i] = 0
                self.cache[i] = pool[0]
            else:
                self.cache[i] = pool[self.indices[i]]
                return False
        return True


def day_11():
    import re

    product = sensitive_product('abcdefghjkmnpqrstuvwxyz', repeat=8)
    for result in product:
        if all(a == b for a, b in zip('hepxxyzz', result.verify())):
            break

    for result in product:
        result = ''.join(result)
        if re.search(r'(.)\1.*(.)\2', result):
            for a, b, c in zip(result, result[1:], result[2:]):
                if ord(a) + 1 == ord(b) == ord(c) - 1:
                    print(result)
                    break

if __name__ == '__main__':
    day_11()

# # find all combinations of 6 non-negative integers that sum to 10
# # Oh damn. This problem is okay with reseting the offender too, but
# # the day 11 problem expects the offender to advance.
# goal = 10
# for result in sensitive_product(range(11), repeat=5):
#     s = 0
#     for elem in result.verify(True):
#         s += elem
#         if s > goal:
#             break
#     else:
#         print("!", *result, goal - s)


# goal = 10
# product_iter = negotiable_product(range(11), repeat=5)
# for result in product_iter:
#     s = 0
#     for i, elem in enumerate(result):
#         s += elem
#         if s > goal:
#             product_iter.send(i)
#             break
#     else:
#         print("!", *list(result), goal - s)


# goal = 10
# for result in negotiable_product(range(11), repeat=5):
#     s = 0
#     for i, elem in enumerate(result):
#         s += elem
#         if s > goal:
#             product_iter.send(i)
#     else:
#         print("!", *list(result), goal - s)
