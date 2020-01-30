import asyncio
import datetime
import functools
import inspect


def foo(left, right):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(loop, msg):
            return func(loop, msg, '{}{}{}'.format(left, msg, right))

        # if inspect.iscoroutinefunction(func):
        #     @functools.wraps(func)
        #     async def wrapper2(*args, **kwargs):
        #         await wrapper(*args, **kwargs)
        #     return wrapper2
        return wrapper
    return decorator


@foo("{", "}")
async def display_date(loop, msg, msg2):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now(), msg, msg2)
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


@foo("{", "}")
def bar(_, msg, msg2):
    print(msg, msg2)


@foo("{", "}")
@asyncio.coroutine
def baz(_, msg, msg2):
    print(msg, msg2)


@asyncio.coroutine
@foo("{", "}")
def zab(_, msg, msg2):
    print(msg, msg2)


async def ultimate_test(awaitable):
    await awaitable


print(display_date, bar, baz, zab)

bar(0, 'five')
loop = asyncio.get_event_loop()
asyncio.ensure_future(ultimate_test(display_date(loop, "yuk")))
asyncio.ensure_future(ultimate_test(display_date(loop, "gross")))
asyncio.ensure_future(ultimate_test(baz(loop, "nasty")))
asyncio.ensure_future(ultimate_test(zab(loop, "disgusting")))
pending = asyncio.Task.all_tasks()
loop.run_until_complete(asyncio.gather(*pending))
loop.close()
