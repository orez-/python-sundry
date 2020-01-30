import enum


class Vector(object):
    def __init__(self, row, col):
        self._row = row
        self._col = col
        # return tuple.__new__(cls, (row, col))

    def __getitem__(self, index):
        if index == 0:
            return self._row
        if index == 1:
            return self._col
        raise IndexError

    @property
    def row(self):
        return self[0]

    @property
    def col(self):
        return self[1]

    @property
    def x(self):
        return self[1]

    @property
    def y(self):
        return self[0]

    def __add__(self, coord):
        r, c = coord
        return Vector(r + self.row, c + self.col)

    def __radd__(self, coord):
        r, c = coord
        return Vector(r + self.row, c + self.col)

    def __sub__(self, coord):
        r, c = coord
        return Vector(self.row - r, self.col - c)

    def __rsub__(self, coord):
        r, c = coord
        return Vector(r - self.row, c - self.col)

    def __mul__(self, scalar):
        return Vector(self.row * scalar, self.col * scalar)

    def __neg__(self):
        return self * -1

    def __str__(self):
        return str((self.row, self.col))


class Direction(Vector, enum.Enum):
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)


print(type(Direction.up).mro())
print(vars(Direction.up))
print(Direction.up)
print(Direction.up + Direction.up)
print((Direction.up * 5 + Direction.right * 3) * 8)
print(Direction.up + (-4, 4))
print((-4, 4) + Direction.up)
print(-Direction.down)
print(-Direction.down == Direction.up)
print((2, 0) - Direction.down)
print(Direction.down - (2, 0))
