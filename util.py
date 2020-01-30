import functools


def apply(fn):
    def decorator(inner_fn):
        @functools.wraps(inner_fn)
        def anon(*args, **kwargs):
            return fn(inner_fn(*args, **kwargs))
        return anon
    return decorator


class _MutableIterElem:
    def __init__(self, i, elem, parent_list):
        self._value = elem
        self._i = i
        self._parent_list = parent_list

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new):
        self._value = new
        self._parent_list[self._i] = new



class mutable_iteration:
    def __init__(self, lst):
        self._lst = lst
        self._lst_iter = enumerate(lst)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            i, elem = next(self._lst_iter)
        except StopIteration:
            raise StopIteration
        return _MutableIterElem(i, elem, self._lst)


def lchomp(string, prefix):
    if not string.startswith(prefix):
        raise ValueError("Could not lchomp {!r} from {!r}.".format(prefix, string))
    return string[len(prefix):]


def rchomp(string, suffix):
    if not string.endswith(suffix):
        raise ValueError("Could not rchomp {!r} from {!r}.".format(suffix, string))
    return string[:-len(suffix)]


def lreplace(string, prefix, replacement):
    if not string.startswith(prefix):
        return string
    return replacement + string[len(prefix):]


def rreplace(string, prefix, replacement):
    if not string.endswith(prefix):
        return string
    return string[:-len(prefix)] + replacement
