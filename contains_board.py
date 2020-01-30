import re

def get_board():
    r, c = map(int, raw_input().split())
    board = [
        raw_input()
        for _ in xrange(r)
    ]
    return r, c, board

def go():
    R, C, board = get_board()
    r, c, subset = get_board()
    leader = re.compile(r'(?={})'.format(subset[0]))
    for row_num, first_row in enumerate(board[:-len(subset)]):
        for match in leader.finditer(first_row):
            column = match.start()
            winner = all(
                real_row[column:].startswith(check_row)
                for check_row, real_row in zip(subset, board[row_num:])
            )
            if winner:
                return "YES"
    return "NO"

for _ in xrange(input()):
    print go()
