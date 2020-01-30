import itertools

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r)
        for r in range(len(s)+1)
    )

def baseline(list_):
    p = powerset(list_)
    next(p)
    return max(p, key=lambda s: -abs(sum(s)))

def sum0(list_):
    if 0 in list_:
        return [0]
    p = itertools.groupby(sorted(list_), key=lambda x: x > 0)
    negative = list(next(p)[1])
    positive = list(next(p)[1])
    # print(list(powerset(negative)))
    # print(list(powerset(positive)))

# print(baseline([2, 3, 100, -99]))
# print(baseline([100, -89, -8, 11]))
print(sum0([2, 3, 100, -99]))
print(sum0([100, -89, -8, 11]))
