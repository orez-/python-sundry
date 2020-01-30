# optional args (?)
# require named
# decorator optional params

import functools
import inspect

def require_named(*params):
    params = set(params)
    class decorator(object):
        def __init__(self, fn):
            functools.update_wrapper(self, fn)
            self._original_fn = fn

            self._typecheck_fn()

            self.fn = self._decorated(self._original_fn)
            self.cls_fn = self._decorated(self._original_fn, 1)

        def _typecheck_fn(self):
            fn = self._original_fn
            _args = inspect.getargspec(fn).args
            # Ensure all parameters provided actually appear.
            bad_params = params - set(_args)
            if bad_params:
                raise SyntaxError("{fn}() does not take {argument} '{bad_params}'".format(
                    fn=fn.__name__,
                    argument="argument" if len(bad_params) == 1 else "arguments",
                    bad_params="', '".join(bad_params),
                ))

            # Ensure no parameter following a named parameter is not named.
            _args = iter(_args)
            for arg in _args:
                if arg in params:
                    break
            for arg in _args:
                if arg not in params:
                    raise SyntaxError("non-named argument follows named argument")

        def _decorated(self, fn, skip_args=0):
            @functools.wraps(self._original_fn)
            def anon(*args, **kwargs):
                if len(args) > skip_args and not params:
                    raise TypeError("all arguments must be named")
                params_diff = params - set(kwargs)
                if params_diff:
                    raise TypeError("'{}' must be named, not positional".format(
                        "', '".join(params_diff),
                    ))
                return fn(*args, **kwargs)
            return anon

        def __get__(self, instance, cls):
            if instance is None:
                return self.cls_fn
            foo = self._decorated(functools.partial(self._original_fn, instance))
            instance.__dict__[foo.__name__] = foo
            return foo

        def __call__(self, *args, **kwargs):
            return self.fn(*args, **kwargs)

    return decorator


# def decorator_optional_params(fn):
#     @functools.wraps(fn)
#     def anon(*args, **kwargs):
#         if not kwargs and
#     return anon


if __name__ == '__main__':
    import unittest

    class RequireNamedUnitTest(unittest.TestCase):
        def test_require_all_named_success(self):
            @require_named()
            def foo(one, two, three):
                return one, two, three

            result = foo(one=1, two=2, three=3)
            self.assertEquals(result, (1, 2, 3))

        def test_require_all_named_failure(self):
            @require_named()
            def foo(one, two):
                return one, two

            with self.assertRaises(TypeError) as e:
                foo(1, two=2)
            self.assertEquals(e.exception.message, "all arguments must be named")

        def test_require_named_success(self):
            @require_named('two')
            def foo(one, two):
                return one, two

            result = foo(1, two=2)
            self.assertEquals(result, (1, 2))

        def test_require_named_failure(self):
            @require_named('two')
            def foo(one, two):
                return one, two

            with self.assertRaises(TypeError) as e:
                foo(1, 2)
            self.assertEquals(e.exception.message, "'two' must be named, not positional")

        def test_bad_param_order(self):
            with self.assertRaises(SyntaxError) as e:
                @require_named('one')
                def foo(one, two):
                    return one, two
            self.assertEquals(e.exception.message, "non-named argument follows named argument")

        def test_bad_kwargs_reliance(self):
            with self.assertRaises(SyntaxError) as e:
                @require_named('two')
                def foo(one, **kwargs):
                    return one, kwargs['two']
            self.assertEquals(e.exception.message, "foo() does not take argument 'two'")

        def test_missing_param(self):
            with self.assertRaises(SyntaxError) as e:
                @require_named('three')
                def foo(one, two):
                    return one, two
            self.assertEquals(e.exception.message, "foo() does not take argument 'three'")

        def test_method(self):
            class Foo(object):
                @require_named()
                def bar(self, one):
                    return self, one

            foo = Foo()
            result = foo.bar(one=1)
            self.assertEquals(result, (foo, 1))

        def test_method_equivalence(self):
            class Foo(object):
                @require_named()
                def bar(self, one):
                    return self, one

            foo = Foo()
            self.assertIs(Foo.bar, Foo.bar)
            self.assertIs(foo.bar, foo.bar)

        def test_unbound_method(self):
            class Foo(object):
                @require_named()
                def bar(self, one):
                    return self, one

            foo = Foo()
            result = Foo.bar(foo, one=1)
            self.assertEquals(result, (foo, 1))

        def test_method_wraps(self):
            class Foo(object):
                @require_named()
                def bar(self, one):
                    """Test string."""
                    return self, one

            self.assertEquals(Foo.bar.__name__, 'bar')
            self.assertEquals(Foo.bar.__doc__, "Test string.")

            foo = Foo()
            self.assertEquals(foo.bar.__name__, 'bar')
            self.assertEquals(foo.bar.__doc__, "Test string.")

        def test_wraps(self):
            @require_named()
            def foo(one, two):
                """Test string."""
                return one, two

            self.assertEquals(foo.__name__, 'foo')
            self.assertEquals(foo.__doc__, "Test string.")


    unittest.main()
