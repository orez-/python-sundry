import collections
import itertools

v = [90, 53, 205, 62, 45]
h = [72, 160, 70, 86, 67]
coins = [1, 5, 10, 25, 50]


def get_options(value):
    return [
        collections.Counter(ucoin_list) for ucoin_list in
        set(
            tuple(sorted(coin_list)) for coin_list in
            itertools.product(coins, repeat=5)
        ) if sum(ucoin_list) == value]


def solve():
    v_opts = [get_options(v1) for v1 in v]
    h_opts = [get_options(h1) for h1 in h]

    board = [[set(coins) for _ in xrange(5)] for _ in xrange(5)]
    progress = True
    while progress:
        progress = False
        for row, row_opts in zip(board, v_opts):
            for elem, col_opts in zip(row, h_opts):
                # Known only one option
                if len(elem) == 1:
                    continue
                possible = set()
                for row_opt, col_opt in itertools.product(row_opts, col_opts):
                    intersection = row_opt & col_opt
                    possible |= set(intersection)

                if elem - possible:
                    progress = True

                elem &= possible

                # Only one option
                if len(elem) == 1:
                    coin, = elem
                    for opts in (row_opts, col_opts):
                        for opt in opts[:]:
                            if opt[coin] == 0:
                                opts.remove(opt)
                            opt[coin] -= 1
    print_board(board)


def print_board(board):
    for row in board:
        for elem in row:
            print '{}'.format(','.join(map(str, elem))), '\t',
        print

solve()
