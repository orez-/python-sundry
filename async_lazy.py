class AsyncLazyIterator(object):
    def __init__(self, main_list):
        self._main_list = main_list
        self._index = 0

    def __next__(self):
        try:
            value = self._main_list[self._index]
        except IndexError:
            raise StopIteration
        self_index += 1
        return value

    def __iter__(self):
        return self


class AsyncLazyList(object):
    def __init__(self, iterator):
        self._internal_list = []
        self._iterator = iterator

    def _consume_to(self, index):
        if isinstance(index_or_slice, slice):
            index_or_slice.stop
        else:

    def __getitem__(self, index_or_slice):
        self._consume_to(index_or_slice)
        return self.main_list[index_or_slice]

    def __iter__(self):
        return AsyncLazyIterator(self)


class AsyncResponseList(AsyncLazyList):
    def __next__(self):
        pass


