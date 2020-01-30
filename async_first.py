import asyncio


class _FirstingFuture(asyncio.futures.Future):
    """
    Helper for first_to_finish().

    This overrides cancel() to cancel all the children and act more
    like Task.cancel(), which doesn't immediately mark itself as
    cancelled.
    """

    def __init__(self, children, *, loop=None):
        super().__init__(loop=loop)
        self._children = children

    def cancel(self):
        if self.done():
            return False
        ret = False
        for child in self._children:
            if child.cancel():
                ret = True
        return ret

    def cleanup(self):
        for child in self._children:
            child.cancel()


def first_to_finish(*coroutines):
    """
    Like asyncio.gather, but returns only the value of the first
    coroutine to finish.
    """
    loop = asyncio.get_event_loop()
    futures = {
        asyncio.ensure_future(cor, loop=loop)
        for cor in coroutines
    }
    outer = _FirstingFuture(futures)

    def _done_callback(fut):
        if not outer.done():
            outer.set_result(fut._result)
            outer.cleanup()

    for fut in futures:
        fut.add_done_callback(_done_callback)
    return outer


# ---

if __name__ == '__main__':
    async def get_slow_value(sleep, value):
        print(f"  getting {value} in {sleep} seconds")
        try:
            await asyncio.sleep(sleep)
        finally:
            print(f"  Did cleanup {value}")
        return value


    def main():
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(first_to_finish(
            get_slow_value(5, 'foo'),
            get_slow_value(1, 'bar'),
            get_slow_value(3, 'baz'),
        ))

    print(main())
