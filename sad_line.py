from __future__ import division


def get_line(width, height):
    points = []
    y = 0
    delta_y = abs(height / width)
    for x in range(width):
        yield x, int(round(y))
        y += delta_y


def print_line(width, height):
    board = [[' ' for _ in range(width + 1)] for _ in range(height + 1)]
    for x, y in get_line(width, height):
        board[y][x] = 'o'

    print('\n'.join(''.join(row) for row in board))


print_line(20, 10)
