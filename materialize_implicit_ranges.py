# '2016-01-01', 2, 17
# '2016-01-02', 1, 53

# start         end           qmin  qmax  amt
# '2016-01-01'  '2016-01-02'     2     ∞   17
# '2016-01-02'             ∞     1     ∞   53

# ---

# '2016-01-01', 1, 17
# '2016-01-10', 1, 53

# start         end           qmin  qmax  amt
# '2016-01-01'  '2016-01-10'     1     ∞   17
# '2016-01-10'             ∞     1     ∞   53

# ---

# '2016-01-01', 1, 17
# '2016-01-10', 1, 53
# '2016-01-05', 9, 91

# start         end           qmin  qmax  amt
# '2016-01-01'  '2016-01-05'     1     ∞   17
# '2016-01-05'             ∞     9     ∞   91
# '2016-01-05'  '2016-01-10'     1     9   53
# '2016-01-10'             ∞     1     9   53

import itertools


class Infinity:
    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __repr__(self):
        return 'inf'


inf = Infinity()


def overlay(*lists):
    """
    Merge passed sequences, taking elements from the first sequence until
    it is exhausted, then continuing from the next index in the next
    sequence, and so on until all sequences are exhausted.

    Example:
        >>> overlay([1], [0, 2, 3], [0, 0, 0, 4, 5])
        [1, 2, 3, 4, 5]
    """
    missing = object()

    return [
        next(elem for elem in elems if elem is not missing)
        for elems in itertools.zip_longest(*lists, fillvalue=missing)
    ]


def materialize_implicit_ranges(ranges):
    """
    Given a list of orthant regions as defined by their lower-bound points,
    return a list of non-overlapping regions. Where two orthant regions
    overlap, the one with highest `sort` precedence is used.

    :param ranges [(lower_1, lower_2, ...)]
    :return [((lower_1, upper_1), (lower_2, upper_2), ...)]
    """
    ranges = sorted(ranges)

    dbl_bounded = []
    for rng in ranges:
        dbl_bounded = list(_get_dbl_bounded(dbl_bounded, rng))
    return dbl_bounded


def _get_dbl_bounded(dbl_bounded, rng):
    """
    Apply the orthant region defined by lower-bound point `rng` to list of
    non-overlapping regions of `dbl_bounded`, and yield the resulting regions.

    The values of `rng` _must_ have higher `sort` precedence than any `rng`
    previously added to `dbl_bounded`.

    This function does not modify `dbl_bounded`.

    :param dbl_bounded [((lower_1, upper_1), (lower_2, upper_2), ...)]
    :param rng [(lower_1, lower_2, ...)]
    :return [((lower_1', upper_1'), (lower_2', upper_2'), ...)]
    """
    # Yield the new region defined by the given point.
    yield tuple((start, inf) for start in rng)

    # Identify if this new region masks existing regions.
    for box in dbl_bounded:
        # If any axis of the new point exceeds the upper bound of a region,
        # that box is unaffected by the new region and may be yielded as-is.
        disjoint = any(pt >= upper for pt, (lower, upper) in zip(rng, box))

        if disjoint:
            yield box
            continue

        # Create between 0 and |axes| new regions from the old region.
        # These are the regions created by limiting the upper bounds of the old region to the
        # lower bounds of the region `rng` defines, in each axis.
        coord = []
        lower_box, upper_box = zip(*box)

        for i, pt in enumerate(rng):
            # Determine the lower bounds for the new region created by the intersection.
            # This starts as the lower bound of the old region, but we must be careful to avoid
            # overlap in newly created regions. To compensate, we set the lower bound in this axis
            # for all subsequently created regions to the upper bound in this axis of this region.
            new_lower_bounds = overlay(coord, lower_box)
            coord.append(pt)

            # Determine the upper bounds for the new region created by the intersection.
            # Each new region is only (newly) upper-bounded in one axis, by that axis in the lower
            # bound of the region `rng` defines (with potentially one new region for each axis).
            new_upper_bounds = list(upper_box)
            new_upper_bounds[i] = pt

            # Omit regions with a width of 0 or less in any axis.
            new_bounds = tuple(zip(new_lower_bounds, new_upper_bounds))
            if all(lower < upper for lower, upper in new_bounds):
                yield new_bounds

# ---
import datetime

import pytest


@pytest.mark.parametrize('args,expected', (
    ([(1,), (10,), (5,)], {((1, 5),), ((5, 10),), ((10, inf),)}),
    (
        [(1, 1), (10, 1), (5, 9)],
        {((1, 5), (1, inf)), ((5, 10), (9, inf)), ((5, 10), (1, 9)), ((10, inf), (1, inf))},
    ),
    (
        [(1, 1, 1), (3, -5, 1)],
        {((1, 3), (1, inf), (1, inf)), ((3, inf), (-5, inf), (1, inf))},
    ),
    (
        [(1, 2, 3), (4, 5, 6)],
        {
            ((1, 4), (2, inf), (3, inf)),
            ((4, inf), (2, 5), (3, inf)),
            ((4, inf), (5, inf), (3, 6)),
            ((4, inf), (5, inf), (6, inf)),
        },
    ),
    (
        [(datetime.date(2016, 1, 1), 2), (datetime.date(2016, 1, 2), 1)],
        {
            ((datetime.date(2016, 1, 2), inf), (1, inf)),
            ((datetime.date(2016, 1, 1), datetime.date(2016, 1, 2)), (2, inf)),
        },
    )
))
def test(args, expected):
    result = set(materialize_implicit_ranges(args))
    assert result == expected, "Actual: %r; Expected: %r" % (result, expected)
