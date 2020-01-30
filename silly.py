import itertools

for _ in xrange(input()):
    s = input()
    blocked = [i for i, v in enumerate(raw_input()) if v == "0"]
    areas = {}

    # Find all triangles s.t.:
    #  First point is at 0
    #  Second to third point is smallest distance
    #  First to third point is largest distance
    for i in xrange(1, s // 2 + 1):
        for j in xrange(i + 1, min(i * 2, s - i) + 1):
            d = (j - i, i, s - j)
            n = {
                1: i,  # Equilateral
                2: s,  # Isosceles
                3: s * 2,  # Scalene
            }[len(set(d))]
            areas[d] = n

    # Remove blocked triangles.
    for x, y, z in itertools.combinations(blocked, 3):
        areas[tuple(sorted((y - x, z - y, x - z + s)))] -= 1

    print sum(x * (x - 1) / 2 for x in areas.itervalues())
