import bisect
import itertools


class PrimeGenerator(object):
    def __init__(self):
        self._gen = self._gen_fn()
        next(self._gen)

    def primes_below(self, num):
        if self._primes[-1] < num:
            for p in self._gen:
                if p >= num:
                    return self._primes[:]
        return self._primes[:bisect.bisect(self._primes, num)]

    def nth_prime(self, n):
        diff = n - len(self._primes) + 1
        if diff >= 0:
            for _ in itertools.izip(xrange(diff), self._gen):
                pass
        return self._primes[n]

    def __contains__(self, value):
        self.primes_below(value + 1)
        # TODO: bisect
        return value in self._primes

    def _gen_fn(self):
        self._primes = [2]
        yield 2
        for i in itertools.count(3):
            for p in self._primes:
                if p * p > i:
                    self._primes.append(i)
                    yield i
                    break
                if i % p == 0:
                    break


if __name__ == '__main__':
    p = PrimeGenerator()
    print p.nth_prime(5)
    print p.nth_prime(4)
