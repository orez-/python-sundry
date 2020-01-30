import sys

lookup = dict(map(reversed, enumerate('abcdefghijklmnopqrstuvwxyz'))).get

def scorer(word):
    return sum(lookup(letter, 0) for letter in word)


word_scores = (
    (scorer(word.strip()), word.strip())
    for word in (w.strip().lower() for w in sys.stdin)
)

# print(sorted(word_scores, key=lambda x: x[0])[:-11:-1])
print('\n'.join(word for score, word in word_scores if score == 100))
