# https://www.hackerrank.com/challenges/iterate-it/problem
import itertools


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


# def known_solve(A):
#     A = set(A)
#     r = 0
#     while A:
#         print(sorted(A))
#         A = set(
#             abs(b - a)
#             for a, b in itertools.combinations(A, 2)
#             if b != a
#         )
#         r += 1
#     return r


def known_solve(A):
    A = set(A)
    r = 0
    while A:
        print(sorted(A))
        # print(sorted(map('{:b}'.format, A)))
        A = set(
            abs(b - a)
            for a, b in itertools.combinations(A, 2)
            if b != a
        )
        r += 1

        # feels like there oughtta be a way to generalize this optimization
        if 1 in A:
            print(sorted(A))
            return r + max(A)
    return r


def trial_solve(A):
    A = set(A)
    r = 0
    while True:
        print(sorted(A))
        # print(sorted(map('{:b}'.format, A)))
        A = set(
            abs(b - a)
            for a, b in itertools.combinations(A, 2)
            if b != a
        )
        r += 1

        if not A:
            return r
        smallest = min(A)

        # ok well that's pretty generalized now but this isn't enough
        if all(a % smallest == 0 for a in A):
            print(sorted(A))
            return r + (max(A) // smallest)


# def trial_solve2(A):
#     A = sorted(set(A))
#     r = 0
#     while A:
#         diffs = [b - a for a, b in pairwise(A)]
#         smallest_jump = min(diffs)

#     pairwise(A)


import random
import pytest


def pytest_generate_tests(metafunc):
    if 'A' in metafunc.fixturenames:
        metafunc.parametrize(
            "A", [
                {random.randint(1, 1000) for _ in range(random.randint(3, 10))}
                for _ in range(10)
            ],
        )


def test_some(A):
    assert known_solve(A) == trial_solve(A)


@pytest.mark.parametrize('B, answer', [
    ([16, 32, 48, 64, 80, 96, 112], 7),
    ([17, 33, 65, 129, 257, 513, 1025, 2049, 4097, 8193, 16385, 32769], 2048),
    # ([11637, 55, 6490, 4056, 8720, 8914, 105, 8533, 37462, 25198], 37352),  # this one is fascinating
    ([2, 4, 49997, 49999], 49976),  # this one's gonna be a real important minimal example
    ([5, 10, 489, 494], 0),
])
@pytest.mark.timeout(10)
def test_special_cases(B, answer):
    assert answer == trial_solve(B)

# if the pairwise difference is all the same add the length of the list
# 17 33 65 129 257 513 1025 2049 4097 8193 16385 32769
# 2048 = 2 ** 11 = 2 ** (12 - 1)
