def maybe_fn(current, rate, weight):
    return current * rate

# ===


def test_must_zero(fn):
    current = fn(current=1, rate=0, weight=1./2)
    assert current == 0, current


def test_must_one(fn):
    current = fn(current=0.84, rate=1, weight=1./2)
    assert current == 0.84, current
    current = fn(current=1, rate=1, weight=1./3)
    assert current == 1, current
    current = fn(current=0, rate=1, weight=4./9)
    assert current == 0, current


if __name__ == "__main__":
    fn = maybe_fn
    for test in [test_must_zero, test_must_one]:
        try:
            test(fn)
        except Exception as e:
            print e.__type__.__name__, e
        else:
            print ".",
