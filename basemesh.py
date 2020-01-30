# -*- coding: utf-8 -*-
import collections


def base(value, base_):
    if base_ == 10:
        return value
    if any(base_ <= int(v) for v in str(value)):
        raise ValueError
    ret_val = collections.deque()
    while value:
        value, mod = divmod(value, base_)
        ret_val.appendleft(str(mod))
    return int(''.join(ret_val))


class Mesh(object):
    def __init__(self):
        self.facts = []

    def fact(self, lhs, rhs, result):
        self.facts.append((lhs, rhs, result))

    def solve(self):
        return sum(
            self.solve_fn(lhs, rhs, result)
            for lhs, rhs, result in self.facts
        )

    def solve_fn(self, lhs, rhs, result):
        # return (lhs + rhs) * 2 == result
        # return (lhs + rhs) * len(str(lhs) + str(rhs)) == result
        return (lhs + rhs) * len(str(lhs) + str(rhs)) == result

    def solve_base(self):
        for l_base in xrange(2, 11):
            for r_base in xrange(2, 11):
                for res_base in xrange(2, 11):
                    try:
                        if all(
                            base(lhs, l_base) + base(rhs, r_base) == base(result, res_base)
                            for lhs, rhs, result in self.facts
                        ):
                            return l_base, r_base, res_base
                    except ValueError:
                        pass
        return r'¯\_(ツ)_/¯'


mesh = Mesh()
mesh.fact(1, 4, 10)
mesh.fact(2, 5, 14)
mesh.fact(6, 10, 40)
mesh.fact(9, 11, 30)
print mesh.solve()
