import collections
import itertools


BOARD_SIZE = 10
Cross = collections.namedtuple('Cross', 'across_pos down_pos across down')
Slot = collections.namedtuple('Slot', 'direction coord start end')


def solve(shape, words):
    board = BoardShape(shape)
    result = allocate_words(
        board=board,
        remaining_words=frozenset(words),
        assigned_words={},
    )
    return board.reconstruct_board(result)


def allocate_words(board, remaining_words, assigned_words):
    if not remaining_words:
        return assigned_words

    slot = board.get_next_slot(assigned_words)  # XXX: manage as passed arg?
    for word in remaining_words:
        if board.slot_matches(slot, word, assigned_words):
            allocated = allocate_words(
                board=board,
                remaining_words=remaining_words - {word},
                assigned_words={**assigned_words, slot: word},
            )
            if allocated:
                return allocated

    return False


class BoardShape:
    def __init__(self, shape):
        self._slots = []
        self._crosses = {}
        spots = {}

        # across
        for y, start, end in find_slots(shape):
            slot_a = Slot('across', y, start, end)
            self._slots.append(slot_a)
            self._crosses[slot_a] = []
            for x in range(start, end):
                spots[x, y] = slot_a

        # down
        for x, start, end in find_slots(zip(*shape)):
            slot_d = Slot('down', x, start, end)
            self._slots.append(slot_d)
            self._crosses[slot_d] = []
            for y in range(start, end):
                slot_a = spots.get((x, y))
                if slot_a:
                    across_start = slot_a.start
                    cross = Cross(
                        across_pos=x - across_start,
                        down_pos=y - start,
                        across=slot_a,
                        down=slot_d,
                    )
                    self._crosses[slot_d].append(cross)
                    self._crosses[slot_a].append(cross)

    def get_next_slot(self, taken_slots):
        taken_slots = set(taken_slots)
        return next(
            slot for slot in self._slots
            if slot not in taken_slots
        )

    def slot_matches(self, slot, word, assigned_words):
        direction, _, start, end = slot
        if end - start != len(word):
            return False
        for cross in self._crosses[slot]:
            if direction == 'across':
                cross_slot = cross.down
                my_pos = cross.across_pos
                cross_pos = cross.down_pos
            else:
                cross_slot = cross.across
                my_pos = cross.down_pos
                cross_pos = cross.across_pos
            cross_word = assigned_words.get(cross_slot)
            if not cross_word:
                continue
            if cross_word[cross_pos] != word[my_pos]:
                return False
        return True

    def reconstruct_board(self, assigned_words):
        letter_lookups = {}
        for (direction, a, start, _), word in assigned_words.items():
            for b, letter in enumerate(word, start):
                coords = (a, b) if direction != 'across' else (b, a)
                letter_lookups[coords] = letter

        buffer = collections.deque()
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                buffer.append(letter_lookups.get((x, y), '+'))
            buffer.append('\n')
        return ''.join(buffer)


def find_slots(shape):
    for y, line in enumerate(shape):
        start = None
        line = iter(enumerate(itertools.chain(line, '+')))
        while True:
            for start, elem in line:
                if elem == '-':
                    break
            for end, elem in line:
                if elem != '-':
                    length = end - start
                    if length > 1:
                        yield y, start, end
                    break
            else:
                break


def main():
    shape = [input() for _ in range(BOARD_SIZE)]
    words = input().split(';')
    return solve(shape, words)


if __name__ == '__main__':
    print(main())
