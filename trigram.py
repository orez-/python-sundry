import collections
import itertools
import re


def get_trigrams(seq):
    "Returns a sliding window (of width 3) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    TRI = 3
    it = iter(seq)
    result = tuple(itertools.islice(it, TRI))
    if len(result) == TRI:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def load_trigram_index():
    trigram_index = collections.defaultdict(set)
    with open('/usr/share/dict/words') as file:
        for line in file:
            word = line.strip()
            for tri in get_trigrams(word):
                trigram_index[tri].add(word)
    return dict(trigram_index)


def scan(words, pattern):
    reg = re.compile(re.escape(pattern).replace("%", ".*"))
    for word in words:
        if reg.fullmatch(word):
            yield word


def query(trigram_index, pattern):
    pattern_trigrams = [
        trigram
        for trigrams in map(get_trigrams, pattern.split("%"))
        for trigram in trigrams
    ]
    matches = min(
        (trigram_index[trigram] for trigram in pattern_trigrams),
        key=len,
    )
    return list(scan(matches, pattern))


if __name__ == '__main__':
    print("loading")
    index = load_trigram_index()
    print("loaded")
    while True:
        results = query(index, input())
        print(results)
