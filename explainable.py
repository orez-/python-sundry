import functools


class ExplainableResult:
    """
    Object to fetch the result from an iterator, and optionally the explanation for that result.

    See `yields_why` for usage.
    """
    def __init__(self, iterator):
        try:
            self.result = next(iterator)
        except StopIteration as exc:
            self.result = exc.value
            self._explain = None
        self._iterator = iterator

    def explain(self):
        try:
            return self._explain
        except AttributeError:
            try:
                next(self._iterator)
            except StopIteration as exc:
                self._explain = exc.value
            else:
                raise RuntimeError("generator didn't stop") from None
        return self._explain


def yields_why(fn):
    """
    Decorator to wrap results from a generator function as `ExplainableResult`s.

    This function should either `yield` a single result followed by the
    `return` of an explanation, or should simply `return` a single result.
    The results are returned as a `ExplainableResult`. The results are exposed
    via `result`, and the explanations are _only_ loaded when `explain()` is called.
    """
    @functools.wraps(fn)
    def anon(*args, **kwargs):
        return ExplainableResult(fn(*args, **kwargs))
    return anon


if __name__ == '__main__':
    @yields_why
    def is_prime(num):
        i = 2
        while i * i <= num:
            if num % i == 0:
                yield False
                break
            i += 1
        else:
            return True

        print("Ok fetchin explanation for", num, "starting at", i)
        original_num = num
        prime_factors = []
        while i * i <= num:
            while num % i == 0:
                prime_factors.append(i)
                num //= i
            i += 1
        if num != 1:
            prime_factors.append(num)
        return f"{original_num} is divisible by {', '.join(map(str, prime_factors))}"

    is_51_prime = is_prime(51)
    print(is_51_prime.result)
    print(is_51_prime.explain())
    print()

    is_53_prime = is_prime(53)
    print(is_53_prime.result)
    print(is_53_prime.explain())
    print()

    is_3127_prime = is_prime(3127)
    print(is_3127_prime.result)
    print(is_3127_prime.explain())
