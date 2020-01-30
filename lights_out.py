# -*- coding: utf-8 -*-

def _alphabeta(node, depth, iterations, player, a=-float('inf'), b=float('inf')):
    if depth == 0 or iterations == 0 or node.gameover:
        # The multiplier here is technically unnecessary, but adding it
        # makes it favor moves that let it win faster or lose slower.
        return node.heuristic(player) * (depth + 1), None, iterations

    choice = None
    if player:
        v = -float('inf')
        for option in node.options():
            alph, _, iterations = _alphabeta(option, depth - 1, iterations - 1, not player, a, b)
            if v < alph:
                v = alph
                choice = option.latest_spot
            a = max(a, v)
            if b <= a:
                break
            if iterations == 0:
                break
    else:
        v = float('inf')
        for option in node.options():
            alph, _, iterations = _alphabeta(option, depth - 1, iterations - 1, not player, a, b)
            if v > alph:
                v = alph
                choice = option.latest_spot
            b = min(b, v)
            if b <= a:
                break
            if iterations == 0:
                break
    return v, choice, iterations


class Board(object):
    def __init__(self, board, ls=None):
        self.board = board
        self.latest_spot = ls

    @classmethod
    def new(cls):
        return cls([
            list(raw_input())
            for _ in xrange(8)
        ])

    @property
    def gameover(self):
        return not any(self.options())

    def options(self):
        for r, row in enumerate(self.board):
            for c, elem in enumerate(row):
                if elem == '0':
                    continue
                assert elem == '1', elem
                rows = map(list, self.board)
                if c != 7:
                    rows[r][c + 1] = '0' if rows[r][c + 1] == '1' else '1'
                if r != 7:
                    rows[r + 1][c] = '0' if rows[r + 1][c] == '1' else '1'
                yield Board(rows, (r, c))

    def heuristic(self, player):
        return -self.gameover


player = input() - 1
board = Board.new()

iterations = 200000
depth = 7
best = None
while iterations:
    _, (r, c), iterations = _alphabeta(board, depth=depth, iterations=iterations, player=player)
    if not best or iterations:
        best = r, c
    if iterations:
        depth += 1

r, c = best
print r, c
