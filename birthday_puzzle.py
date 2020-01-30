# age = pth prime number
# p is prime
# sum(primes 2 - p) = age
# third such number
# 5, 17, 41
import itertools

import prime_generator

primes = prime_generator.PrimeGenerator()

sum_ = 0
for p in itertools.count(1):
    if p not in primes:
        continue
    prime = primes.nth_prime(p - 1)
    if prime != sum(primes.primes_below(p)):
        continue
    print(primes.primes_below(p), p, prime)
