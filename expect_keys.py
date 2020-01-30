import functools
import inspect


def expect_keys(param_name, permit=None, require=None):
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            fn_args = inspect.getcallargs(inner._base_fn, *args, **kwargs)
            d = fn_args[param_name]
            if require:
                for k in require:
                    if k not in d:
                        raise TypeError("missing required key {!r} on {!r}".format(k, param_name))
            permitx = permit or []
            for k in d:
                if k not in permitx and (not require or k not in require):
                    raise TypeError("invalid key {!r} on {!r}".format(k, param_name))
            return fn(*args, **kwargs)
        inner._base_fn = getattr(fn, '_base_fn', fn)
        return inner
    return decorator


if __name__ == '__main__':
    import unittest

    class ExpectKeysUnitTest(unittest.TestCase):
        def create_double_fn(self):
            @expect_keys('filter_args', require=['four'], permit=['five', 'six'])
            @expect_keys('update_args', require=['one'], permit=['two', 'three'])
            def double_fn(update_args, filter_args):
                return update_args, filter_args
            return double_fn

        def create_kwargs_fn(self):
            @expect_keys('kwargs', require=['baz'])
            def kwargs_fn(**kwargs):
                return kwargs['baz']
            return kwargs_fn

        def test_double_positional(self):
            foo = self.create_double_fn()
            foo({'one': 1, 'three': 3}, {'four': 4})

        def test_double_mixed(self):
            foo = self.create_double_fn()
            foo({'one': 1}, filter_args={'four': 4, 'six': 6})

        def test_double_named(self):
            foo = self.create_double_fn()
            foo(update_args={'one': 1, 'two': 2}, filter_args={'four': 4, 'six': 6})

        def test_double_failure1(self):
            foo = self.create_double_fn()
            with self.assertRaises(TypeError):
                foo({'two': 2, 'three': 3}, {'four': 4})  # Fails, has no 'one'

        def test_double_failure2(self):
            foo = self.create_double_fn()
            with self.assertRaises(TypeError):
                foo({'one': 1, 'three': 3}, {})  # Fails, has no 'four'

        def test_kwargs_success(self):
            bar = self.create_kwargs_fn()
            bar(baz=1)

        def test_kwargs_missing_required(self):
            bar = self.create_kwargs_fn()
            with self.assertRaises(TypeError):
                bar()

        def test_kwargs_extra_param(self):
            bar = self.create_kwargs_fn()
            with self.assertRaises(TypeError):
                bar(baz=1, bang=5)
    unittest.main()
