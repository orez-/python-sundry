class HexBoard(dict):
    def __init__(self, *args):
        if args:
            args = [{
                self._translate_slice(k): v
                for k, v in dict(*args).items()
            }]
        super().__init__(*args)

    @staticmethod
    def _translate_slice(key):
        try:
            coord = (key.start, key.stop, key.step)
        except AttributeError:
            coord = key
            if len(coord) == 2:
                coord += (None,)

        num_coords = sum(1 for elem in coord if elem is not None)
        if num_coords < 2:
            raise ValueError("coordinate requires at least two values")
        if num_coords == 2:
            # fill in the missing coord
            third_value = -sum(elem for elem in coord if elem is not None)
            coord = tuple(third_value if elem is None else elem for elem in coord)
        elif num_coords == 3:
            if sum(coord):
                raise IndexError("invalid coordinate")
        else:
            raise ValueError("coordinate requires at most three values")
        return coord

    def __getitem__(self, key):
        return super().__getitem__(self._translate_slice(key))

    def __setitem__(self, key, value):
        super().__setitem__(self._translate_slice(key), value)

    def rotate(self, num):
        if num == 0:
            return HexBoard(self)
        negate = num % 2
        twist = num % 3
        new_board = HexBoard()
        for coord, value in self.items():
            coord = coord[twist:] + coord[:twist]
            if negate:
                coord = tuple(-c for c in coord)
            new_board[coord] = value
        return new_board


class Piece:
    def __init__(self, color, coords, rotate=0):
        self.color = color
        self.shape = HexBoard((c, True) for c in coords).rotate(rotate)


def _valid_shapes():
    pieces = []

    green = [
        (-1, 0),
        (0, 0),
        (1, 0),
        (2, 0),
    ]

    pieces += [
        Piece('g', green, i)
        for i in range(3)
    ]

    orange = [
        (0, 0),
        (1, -1),
        (0, 1),
        (0, -1),
    ]

    pieces += [
        Piece('o', orange, i)
        for i in range(6)
    ]

    pink = [
        (0, 0),
        (1, 0),
        (0, 1),
        (0, -1),
    ]

    pieces += [
        Piece('p', pink, i)
        for i in range(6)
    ]

    blue = [
        (0, 0),
        (1, -1),
        (1, 0),
        (0, 1),
    ]

    pieces += [
        Piece('b', blue, i)
        for i in range(3)
    ]

    yellow = [
        (1, -1),
        (0, -1),
        (-1, 0),
        (-1, 1),
    ]

    pieces += [
        Piece('y', yellow, i)
        for i in range(6)
    ]

    pieces.append(Piece('s', [(0, 0)]))
    return pieces



import random

valid_shapes = _valid_shapes()

class Game:
    SIZE = 5

    def __init__(self):
        SIZE = self.SIZE
        self.board = HexBoard()
        for row in range(-SIZE, SIZE + 1):
            for col in range(-SIZE, SIZE + 1):
                if abs(row + col) <= SIZE:
                    self.board[row:col] = False

        self.pieces = [
            random.choice(valid_shapes)
            for _ in range(3)
        ]

    def place_random_piece(self):
        SIZE = self.SIZE
        piece = random.choice(self.pieces)
        while True:
            py = random.randint(-SIZE, SIZE)
            px = random.randint(-SIZE, SIZE)
            can_place = self.can_place_piece(piece, (px, py))
            if can_place:
                for coord in can_place:
                    self.board[coord] = piece.color
                break

    def can_place_piece(self, piece, coord):
        px, py = coord
        coords = [
            (py + y, px + x, -(py + y + px + x))
            for y, x, _ in piece.shape
        ]
        if all(
            all(abs(c) <= self.SIZE for c in coord) and not self.board[coord]
            for coord in coords
        ):
            return coords
        return False

    def display_board(self):
        SIZE = self.SIZE
        for row in range(-SIZE, SIZE + 1):
            print(end=' ' * row)
            for col in range(-SIZE, SIZE + 1):
                if abs(row + col) > SIZE:
                    print(end=' ')
                else:
                    print(self.board[row:col] or '.', end=' ')
            print()
        print()

    def display(self):
        SIZE = self.SIZE

        for row in range(-SIZE, SIZE + 1):
            print(end=' ' * row)
            for col in range(-SIZE, SIZE + 1):
                if abs(row + col) > SIZE:
                    print(end=' ')
                else:
                    print(self.board[row:col] or '.', end=' ')

            for piece in self.pieces:
                pass
            print()
        print()


        # for piece in self.pieces:
        for piece in valid_shapes:
            x_bounds = [x for x, y, z in piece.shape]
            min_x = min(x_bounds)
            max_x = max(x_bounds) + 1

            y_bounds = [y for x, y, z in piece.shape]
            min_y = min(y_bounds)
            max_y = max(y_bounds) + 1

            for row in range(min_x, max_x):
                print(end=' ' * (row - min_x))
                for col in range(min_y, max_y):
                    if (row, col, -row - col) in piece.shape:
                        print(piece.color, end=' ')
                    else:
                        print(end='  ')
                print()
            print()


game = Game()
game.display()
game.place_random_piece()
game.display()
