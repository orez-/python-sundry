import heapq

import util


@util.apply(sorted)
def control():
    for a in range(10, 100):
        for b in range(10, a + 1):
            yield a * b, b, a


def strat1():
    a = 10
    b = 10
    cache = {a: (b, a * b)}
    max_key = a

    while True:
        a, (b, prod) = min(cache.items(), key=lambda item: item[1][1])
        if a == max_key:
            max_key += 1
            cache[max_key] = (
                max_key, max_key * max_key,
            )
        yield prod, a, b
        cache[a] = (b + 1, a * (b + 1))


def strat2():
    a = 10
    b = 10
    cache = [(a * b, a, b)]
    max_key = a

    while True:
        prod, a, b = heapq.heappop(cache)
        if a == max_key:
            max_key += 1
            heapq.heappush(cache, (max_key * max_key, max_key, max_key))
        yield prod, a, b
        b += 1
        heapq.heappush(cache, (a * b, a, b))

# ---

def compare_strats(*strat_fns):
    import more_itertools

    for iteration_results in zip(*(fn() for fn in strat_fns)):
        print(iteration_results)
        if not more_itertools.all_equal(ab for ab, _, _ in iteration_results):
            break


def main(strat):
    for ab, a, b in strat():
        print(ab, a, b)


if __name__ == '__main__':
    # compare_strats(control, strat1, strat2)
    main(strat2)
