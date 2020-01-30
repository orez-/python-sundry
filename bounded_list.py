import dataclasses


@dataclasses.dataclass(frozen=True)
class from_right:
    _idx: int  # there's no SupportsIndex as of py3.7

    def index(self, sequence):
        return len(sequence) - self._idx


def _normalize_slice_piece(piece, seq):
    piece = piece.index(seq) if isinstance(piece, from_right) else piece
    if piece is not None:
        piece = max(piece, 0)
    return piece


class BoundedList(list):
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            start = _normalize_slice_piece(idx.start, self)
            stop = _normalize_slice_piece(idx.stop, self)
            return super().__getitem__(slice(start, stop, idx.step))
        if isinstance(idx, from_right):
            idx = idx.index(self)
        if not (0 <= idx < len(self)):
            raise IndexError("list index out of range")
        return super().__getitem__(idx)


# ---

import pytest


@pytest.mark.parametrize('list_type', [list, BoundedList])
def test_parity(list_type):
    lst = list_type(range(10))
    assert lst[:5] == [0, 1, 2, 3, 4]


@pytest.mark.parametrize('list_type,expected', [
    (list, [8, 9]),
    (BoundedList, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
])
def test_negative_start_slice(list_type, expected):
    lst = list_type(range(10))
    assert lst[-2:] == expected


@pytest.mark.parametrize('list_type,expected', [
    (list, [0, 1, 2, 3, 4, 5]),
    (BoundedList, []),
])
def test_negative_stop_slice(list_type, expected):
    lst = list_type(range(10))
    assert lst[:-4] == expected


def test_from_right_idx():
    lst = BoundedList(range(10))
    assert lst[from_right(8)] == 2

def test_from_right_start():
    lst = BoundedList(range(10))
    assert lst[from_right(2):] == [8, 9]


def test_from_right_stop():
    lst = BoundedList(range(10))
    assert lst[:from_right(4)] == [0, 1, 2, 3, 4, 5]


def test_negative_idx():
    lst = BoundedList(range(10))
    with pytest.raises(IndexError):
        lst[-4]


def test_oob_from_right():
    lst = BoundedList(range(10))
    with pytest.raises(IndexError):
        lst[from_right(15)]


def test_negative_from_right():
    lst = BoundedList(range(10))
    with pytest.raises(IndexError):
        lst[from_right(-4)]


# ---

if __name__ == '__main__':
    import inspect

    try:
        import pygments
        import pygments.formatters
        import pygments.lexers

        def print_source(fn):
            print(pygments.highlight(
                inspect.getsource(fn),
                pygments.lexers.PythonLexer(),
                pygments.formatters.TerminalFormatter(),
            ))
    except ImportError:
        def print_source(fn):
            print(inspect.getsource(fn))


    print("Has this ever happened to you?\n")

    def print_all_suffixes(lst):
        for i in range(len(lst), -1, -1):
            print(lst[-i:])

    print_source(print_all_suffixes)
    print("print_all_suffixes([4, 8, 15, 16, 23, 42])")
    print_all_suffixes([4, 8, 15, 16, 23, 42])

    print("\nAvoid embarrassing index sign flips with BoundedList!\n")

    def print_all_suffixes(lst):
        lst = BoundedList(lst)
        for i in range(len(lst), -1, -1):
            print(lst[from_right(i):])

    print_source(print_all_suffixes)
    print("print_all_suffixes([4, 8, 15, 16, 23, 42])")
    print_all_suffixes([4, 8, 15, 16, 23, 42])
