class Square:
    def __init__(self, *, left, bottom, **kwargs):
        self.bottom = bottom
        self.left = left

        self._autofill_fields(kwargs)

    def _autofill_fields(self, kwargs):
        if len(kwargs) > 1:
            raise TypeError("overconstrained square")
        if not kwargs:
            raise TypeError("underconstrained square")
        if 'top' in kwargs:
            self.top = kwargs['top']
            self.length = self.top - self.bottom
            self.area = self.length * self.length
            self.right = self.left + self.length
        elif 'area' in kwargs:
            self.area = kwargs['area']
            self.length = self.area ** 0.5
            self.top = self.bottom + self.length
            self.right = self.left + self.length
        elif 'right' in kwargs:
            self.right = kwargs['right']
            self.length = self.right - self.left
            self.area = self.length * self.length
            self.top = self.bottom + self.length
        elif 'length' in kwargs:
            self.length = kwargs['length']
            self.area = self.length * self.length
            self.top = self.bottom + self.length
            self.right = self.left + self.length
        else:
            [arg] = kwargs
            raise TypeError(f"unexpected keyword argument {arg}")

    @property
    def top_right(self):
        return (self.right, self.top)

    @property
    def bottom_left(self):
        return (self.left, self.bottom)


def triangle_area(pt1, pt2, pt3):
    xa, ya = pt1
    xb, yb = pt2
    xc, yc = pt3
    return abs(((xa - xc) * (yb - ya) - (xa - xb) * (yc - ya)) / 2)


bl_square = Square(
    left=0,
    bottom=0,
    area=5,
)

tl_square = Square(
    left=0,
    bottom=bl_square.top,
    right=bl_square.right,
)

mid_square = Square(
    left=bl_square.right,
    bottom=0,
    top=tl_square.top,
)

big_square = Square(
    left=mid_square.right,
    bottom=0,
    top=523,
)

print(triangle_area(
    tl_square.bottom_left,
    tl_square.top_right,
    big_square.top_right,
))
