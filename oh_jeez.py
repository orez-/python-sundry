def if_(condition):
    def decorator(fn):
        if condition:
            fn()
        return bool(condition)
    return decorator


def elif_(if_condition, elif_condition_fn):
    elif_condition = elif_condition_fn()
    def decorator(fn):
        if not if_condition and elif_condition:
            fn()
        return if_condition or elif_condition
    return decorator


def else_(if_condition):
    condition = not if_condition
    def decorator(fn):
        if condition:
            fn()
    return decorator


def for_(iterable):
    def decorator(fn):
        for elem in iterable:
            fn(elem)
    return decorator


@for_(range(1, 100))
def _(elem):
    @if_(elem % 15 == 0)
    def if_stmt():
        print(elem, "Fizzbuzz")
    @elif_(if_stmt, lambda: elem % 5 == 0)
    def elif_stmt():
        print(elem, "Buzz")
    @elif_(elif_stmt, lambda: elem % 3 == 0)
    def elif_stmt():
        print(elem, "Fizz")
    @else_(elif_stmt)
    def _():
        print(elem)
