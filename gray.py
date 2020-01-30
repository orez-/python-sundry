# def total_iterative_gray_code_strs(n):
#     if n < 1:
#         return
#     g = ['0', '1']
#     for _ in range(n - 1):
#         print(g)
#         # simultaneously:
#         # - reverse g, prepend a 1 to each, and throw em on the end
#         # - prepend a 0 to each of g
#         for i in range(len(g))[::-1]:
#             char = '1' + g[i]
#             g[i] = '0' + g[i]
#             g.append(char)
#     return g


# def total_iterative_gray_code_ints(n):
#     if n < 1:
#         return
#     g = [(0,), (1,)]
#     for _ in range(n - 1):
#         # simultaneously:
#         # - reverse g, prepend a 1 to each, and throw em on the end
#         # - prepend a 0 to each of g
#         for i in range(len(g))[::-1]:
#             char = (1,) + g[i]
#             g[i] = (0,) + g[i]
#             g.append(char)
#     return g


# def total_iterative_gray_code_changes(collection):
#     collection = list(collection)
#     if not collection:
#         return

#     last_subset = set()
#     bitsets = iter(total_iterative_gray_code_ints(len(collection)))
#     next(bitsets)
#     for bits in bitsets:
#         subset = {item for bit, item in zip(bits, collection) if bit}
#         yield frozenset(subset - last_subset), frozenset(last_subset - subset)
#         last_subset = subset


def powerset_delta(collection):
    # https://en.wikipedia.org/wiki/Gray_code
    lookup = {
        key: value
        for i, elem in enumerate(collection)
        for key, value in [
            (1 << i, (frozenset([elem]), frozenset())),
            (-1 << i, (frozenset(), frozenset([elem]))),
        ]
    }
    n = len(lookup) // 2
    last_gray = 0
    for i in range(1, 1 << n):
        gray = i ^ (i >> 1)
        yield lookup[gray - last_gray]
        last_gray = gray


# for added, removed in total_iterative_gray_code_changes("abcd"):
#     print(added, removed)

# ---
import inspect

import pytest


@pytest.mark.parametrize("gray_code", [iterative_gray_code_changes])
def test_gray(gray_code):
    result = gray_code("dcba")
    assert inspect.isgenerator(result)
    result = list(result)

    expected = [
        (frozenset({'d'}), frozenset()),
        (frozenset({'c'}), frozenset()),
        (frozenset(), frozenset({'d'})),
        (frozenset({'b'}), frozenset()),
        (frozenset({'d'}), frozenset()),
        (frozenset(), frozenset({'c'})),
        (frozenset(), frozenset({'d'})),
        (frozenset({'a'}), frozenset()),
        (frozenset({'d'}), frozenset()),
        (frozenset({'c'}), frozenset()),
        (frozenset(), frozenset({'d'})),
        (frozenset(), frozenset({'b'})),
        (frozenset({'d'}), frozenset()),
        (frozenset(), frozenset({'c'})),
        (frozenset(), frozenset({'d'})),
    ]
    assert result == expected


# @pytest.mark.parametrize("gray_code", [total_iterative_gray_code])
# def test_gray(gray_code):
#     result = ['0000', '0001', '0011', '0010', '0110', '0111', '0101', '0100', '1100', '1101', '1111', '1110', '1010', '1011', '1001', '1000']
#     assert gray_code(4) == result
