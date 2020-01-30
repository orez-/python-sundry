import inspect


def muxer(adapter_fn, filter_args):
    def decorator(fn):
        def inner(*args, **kwargs):
            call_args = inspect.getcallargs(fn, *args, **kwargs)
            for arg in filter_args:
                call_args.pop(arg, None)
            return adapter_fn(**call_args)
        return inner
    return decorator

# ===

def adapter_fn(two, three, args, kwargs):  # no splats :\
    print(two, three, args, kwargs)

@muxer(adapter_fn, ['session'])
def test(session, two, three, *args, **kwargs):
    pass

# ===

test(1, 2, 3)
test(session=1, two=2, three=3)
test(1, 2, 3, 4, 5, 6)
test(1, 2, 3, 4, foo=5, bar=6)
