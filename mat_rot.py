import itertools

def get_board():
    return [
        raw_input().split()
        for _ in xrange(m)
    ]


def get_unwrapped(board):
    starboard = zip(*board)

    unwrapped = []
    for layer in xrange(min(m, n) // 2):
        # > v
        # ^ <
        end = -layer - 1
        unwrapped.append(
            sum(map(list, (
                board[layer][layer:end],
                starboard[end][layer:end],
                board[end][end:layer:-1],
                starboard[layer][end:layer:-1],
            )), [])
        )
    return unwrapped


def wrap_matrix(unwrapped):
    board = [[None] * n for _ in xrange(m)]
    starboard = [[None] * m for _ in xrange(n)]

    for layer, wrap in enumerate(unwrapped):
        end = -layer - 1
        wrap = iter(wrap)
        board[layer][layer:end] = itertools.islice(wrap, len(starboard) + end - layer)
        starboard[end][layer:end] = itertools.islice(wrap, len(board) + end - layer)
        board[end][end:layer:-1] = itertools.islice(wrap, len(starboard) + end - layer)
        starboard[layer][end:layer:-1] = itertools.islice(wrap, len(board) + end - layer)

    # Merge the two together
    return [
        [row or col for row, col in zip(rowset, colset)]
        for rowset, colset in zip(board, zip(*starboard))
    ]


def rotate(wrap, rotate):
    rotate %= len(wrap)
    return wrap[rotate:] + wrap[:rotate]


m, n, r = map(int, raw_input().split())
# r, c
board = get_board()
unwrapped = get_unwrapped(board)
unwrapped = [rotate(wrap, r) for wrap in unwrapped]
matrix = wrap_matrix(unwrapped)
print '\n'.join(' '.join(row) for row in matrix)
