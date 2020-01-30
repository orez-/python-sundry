def brute(word, k):
    return ''.join(sorted(set(
        word[i:j]
        for i in xrange(len(word))
        for j in xrange(i + 1, len(word) + 1))))[k - 1]

print brute(raw_input(), int(raw_input()))
