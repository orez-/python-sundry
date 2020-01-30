import collections
import contextlib
import itertools


def square_factors(value):
    factor = 1
    for i in itertools.count(2):
        square = i * i
        if square > value:
            return factor, value
        while value % square == 0:
            value //= square
            factor *= i


class Expression:
    def __int__(self):
        return int(float(self))

    def __rmul__(self, other):
        return self * other

    def __radd__(self, other):
        return self + other


class Dequerator:
    """
    Iterator that can be prepended and appended to.
    """
    def __init__(self, iterator=None):
        self.iterators = collections.deque()
        if iterator:
            self.iterators.append(iter(iterator))

    def __next__(self):
        while True:
            if not self.iterators:
                raise StopIteration
            try:
                return next(self.iterators[0])
            except StopIteration:
                self.iterators.popleft()

    def __iter__(self):
        return self

    def extend_left(self, iterable):
        self.iterators.appendleft(iter(iterable))

    def extend(self, iterable):
        self.iterators.append(iter(iterable))


def _group_constants(exprs):
    if len(exprs) == 1 and isinstance(exprs[0], list):
        exprs = list(exprs[0])
    exprs = Dequerator(exprs)
    constant = 0
    new_exprs = []
    for expr in exprs:
        if isinstance(expr, AdditionExpression):
            exprs.extend_left(expr.exprs)
        elif isinstance(expr, Expression):
            new_exprs.append(expr)
        else:
            constant += expr
    # add the constant if it's not 0, or if we dont have other exprs
    if not new_exprs or constant:
        new_exprs.append(constant)
    return new_exprs


class AdditionExpression(Expression):
    def __new__(cls, *exprs):
        exprs = _group_constants(exprs)
        if len(exprs) == 1:
            return exprs[0]
        return super().__new__(cls)

    def __init__(self, *exprs):
        self.exprs = _group_constants(exprs)

    def __float__(self):
        return sum(map(float, self.exprs))

    def __mul__(self, other):
        # distribute
        return AdditionExpression([
            expr * other
            for expr in self.exprs
        ])

    def __add__(self, other):
        if isinstance(other, AdditionExpression):
            return AdditionExpression(self.exprs + other.exprs)
        return AdditionExpression(*self.exprs, other)

    def __str__(self):
        return ' + '.join(map(str, self.exprs))

    def __repr__(self):
        return f"AdditionExpression({', '.join(map(repr, self.exprs))})"


class sqrt(Expression):
    def __new__(cls, radical, mult=1):
        if radical == 0 or mult == 0:
            return 0
        factor, radical = square_factors(radical)
        mult *= factor
        if radical == 1:
            return mult
        return super().__new__(cls)

    def __init__(self, radical, mult=1):
        factor, radical = square_factors(radical)
        self.radical = radical
        self.mult = mult * factor

    def __str__(self):
        return f"{self.mult if self.mult != 1 else ''}√{self.radical}"

    def __repr__(self):
        return f"sqrt({self.radical}, {self.mult})"

    def __mul__(self, other):
        if isinstance(other, sqrt):
            mult, radical = square_factors(other.radical * self.radical)
            mult *= self.mult * other.mult
            if radical == 1:
                return mult
            return sqrt(radical, mult)
        if isinstance(other, Expression):
            return NotImplemented
        return sqrt(self.radical, self.mult * other)

    def __add__(self, other):
        if isinstance(other, sqrt):
            if self.radical == other.radical:
                return sqrt(self.radical, self.mult + other.mult)
        return AdditionExpression(self, other)

    def __float__(self):
        return self.mult * (self.radical ** 0.5)

# ---

def test_factoring_mult():
    assert str(sqrt(6) * sqrt(14)) == '2√21'


def test_clean_square():
    assert sqrt(6) * sqrt(6) == 6


def test_perfect_square():
    assert sqrt(9) == 3


def test_perfect_square_factor():
    assert str(sqrt(18)) == '3√2'


def test_zero():
    assert sqrt(0) == 0


def test_perfect_cube():
    assert str(sqrt(27)) == '3√3'


def test_addition_matching_factor():
    assert str(3 * sqrt(5) + 5 * sqrt(125)) == '28√5'


def test_addition_nonmatching_factor():
    assert str(sqrt(7) + sqrt(11)) == '√7 + √11'


def test_distribution():
    assert str((sqrt(5) + sqrt(7)) * (sqrt(11) + sqrt(5))) == '√55 + √77 + √35 + 5'


def test_addition_grouping():
    assert str(sqrt(5) + sqrt(7) + sqrt(5)) == '2√5 + √7'
