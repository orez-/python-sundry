def do_while(fn):
    yield
    while fn():
        yield


def test_fn():
    import random

    for _ in do_while(lambda: x != 5):
        x = random.randint(0, 10)
        print(x)

test_fn()
