import asyncio


class Foo(object):
    def __await__(self):
        return iter(range(10))


loop = asyncio.get_event_loop()
asyncio.ensure_future(Foo())
pending = asyncio.Task.all_tasks()
loop.run_until_complete(asyncio.gather(*pending))
loop.close()

