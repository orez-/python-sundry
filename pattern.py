REPS = 6

WIDTH = 2 ** REPS
p = 0
for d in xrange(1, REPS + 1):
    p = 2 ** d - 1
    print '{}{}'.format(' ' * (p // 2), ('o' + ' ' * p) * (WIDTH // (p + 1)))
