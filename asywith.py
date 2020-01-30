"""
This exists now in py37
"""

import sys
from functools import wraps


no_default = object()
async def anext(async_generator, default=no_default):
    async for elem in async_generator:
        return elem
    if default is no_default:
        raise StopAsyncIteration
    return default


class AsyncGeneratorContextManager:
    """Helper for @asynccontextmanager decorator."""

    def __init__(self, gen):
        self.gen = gen

    async def __aenter__(self):
        try:
            return await anext(self.gen)
        except StopAsyncIteration:
            raise RuntimeError("generator didn't yield")

    async def __aexit__(self, type_, value, traceback):
        if type_ is None:
            try:
                await anext(self.gen)
            except StopAsyncIteration:
                return
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type_()
            try:
                self.gen.athrow(type_, value, traceback)
                raise RuntimeError("generator didn't stop after athrow()")
            except StopAsyncIteration as exc:
                # Suppress the exception *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed
                return exc is not value
            except:
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                #
                if sys.exc_info()[1] is not value:
                    raise



def asynccontextmanager(func):
    """@contextmanager decorator.
    Typical usage:
        @contextmanager
        def some_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>
    This makes this:
        with some_generator(<arguments>) as <variable>:
            <body>
    equivalent to this:
        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>
    """
    @wraps(func)
    def helper(*args, **kwds):
        return AsyncGeneratorContextManager(func(*args, **kwds))
    return helper


if __name__ == '__main__':
    import asyncio

    @asynccontextmanager
    async def ticker(delay):
        print("begin!")
        await asyncio.sleep(delay)
        yield "ay"
        await asyncio.sleep(delay)
        print("end")


    async def silly():
        async with ticker(3) as q:
            print(q)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(silly())
