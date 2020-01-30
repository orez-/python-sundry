import collections
import itertools

#               F
#     F O U R _ O S     F I V E _ F S
#               U       O
#           T H R E E _ U S
#     F     H   _       R         S
#     I     I   N       _         E
#     V     R   S     T H R E E _ V S
#     E     T           S         E
#     _     E   O                 N
# T H I R T E E N _ E S           _
#     S     N   E                 R
#           _   _                 S
#           S I X _ T S
#           S

clues = {
    '1a': 7,
    '2a': 7,
    '3a': 8,
    '4a': 8,
    '5a': 11,
    '6a': 6,

    '1d': 7,
    '2d': 7,
    '3d': 11,
    '4d': 7,
    '5d': 8,
    '6d': 5,
}

# 0-indexed
overlap = [
    ('1a', 5, '1d', 1),
    ('2a', 0, '2d', 0),
    ('3a', 0, '3d', 0),
    ('3a', 2, '1d', 3),
    ('3a', 6, '2d', 2),
    ('4a', 1, '2d', 5),
    ('4a', 6, '5d', 2),
    ('5a', 2, '4d', 5),
    ('5a', 5, '3d', 6),
    ('5a', 7, '6d', 1),
    ('6a', 0, '3d', 9),
    ('6a', 2, '6d', 4),
]


numbers = {
    1: 'ONE #',
    2: 'TWO #S',
    3: 'THREE #S',
    4: 'FOUR #S',
    5: 'FIVE #S',
    6: 'SIX #S',
    7: 'SEVEN #S',
    8: 'EIGHT #S',
    9: 'NINE #S',
    10: 'TEN #S',
    11: 'ELEVEN #S',
    12: 'TWELVE #S',
    13: 'THIRTEEN #S',
    14: 'FOURTEEN #S',
    15: 'FIFTEEN #S',
    16: 'SIXTEEN #S',
    17: 'SEVENTEEN #S',  # too long to actually match anything - included for completeness
    18: 'EIGHTEEN #S',
    19: 'NINETEEN #S',
    20: 'TWENTY #S',
}

# ---

def get_char_counts(lookups):
    count = collections.Counter(''.join(value.value for value in lookups.values()))
    for _, _, k, i in overlap:  # Remove overlapping chars
        count[lookups[k].value[i]] -= 1
    del count['#']
    del count[' ']
    return count


def check_config(lookups):
    for key in lookups:
        if key[1] != 'a':
            continue
        # Check overlaps - ensure they even fit together
        for across, aind, down, dind in overlap:
            if across != key:
                continue
            across_chr = lookups[across].value[aind]
            down_chr = lookups[down].value[dind]

            if not (across_chr == '#' or down_chr == '#' or across_chr == down_chr):
                return False

            if len({across_chr, down_chr}) != 1:
                if across_chr == '#':
                    lookups[across].character = down_chr
                elif down_chr == '#':
                    lookups[down].character = across_chr

    counts = get_char_counts(lookups)
    for key, value in lookups.items():
        if value.character != '#':
            if counts[value.character] != value.number:
                return False
            del counts[value.character]  # don't fill in this character again

    # Gotta make sure we do this after we fill in the knowns, so we don't
    # take someone else's value.
    for key, value in lookups.items():
        if value.character == '#':
            for char, count in counts.items():
                if count + 1 == value.number:  # +1 is this character we're adding
                    value.character = char
    return True


class LookupValue:
    def __init__(self, number):
        self.number = number
        self.character = '#'

    @property
    def value(self):
        return numbers[self.number].replace('#', self.character)

    def __repr__(self):
        return self.value


if __name__ == '__main__':
    options = [
        (
            key, [
                num for num, word in numbers.items()
                if len(word) == clue
            ]
        ) for key, clue in clues.items()
    ]

    results = 0
    for config in itertools.product(*(o for _, o in options)):
        lookups = dict(zip((o for o, _ in options), map(LookupValue, config)))
        if check_config(lookups):
            print(lookups)
            results += 1
    print(results, "results")
