import math

def round(n, ):
    return math.floor(n + 0.5)


r = 13
for y in range(r * 2 + 1):
    for x in range(r * 2 + 1):
        nx = x - r
        ny = y - r
        if nx ** 2 + ny ** 2 == r ** 2:
            print(end='#')
        else:
            print(end=' ')
    print()
print()


def bresham(slope):
    for x in range(30):
        yield x, round(slope * x)


for x, y in bresham(0.5):
    print(" " * y + "#")
