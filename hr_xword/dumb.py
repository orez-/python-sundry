import collections


def solve_no_recurse(attempt, words):
    seen = set()
    stack = collections.deque()
    stack.append((0, []))
    while stack:
        start, result = stack.pop()
        if start == len(attempt):
            return result
        for word in words:
            sum_ = start + len(word)
            if sum_ in seen:
                continue
            if attempt.startswith(word, start):
                seen.add(sum_)
                stack.append((sum_, result+[word]))
    return None


def minimize_word_list(words):
    word_set = set(words)
    for word in words:
        result = solve_no_recurse(
            attempt=word,
            words=word_set - {word},
        )
        if result:
            word_set.discard(word)
    return word_set


def main():
    for _ in range(int(input())):
        input()
        words = input().split()
        words = sorted(minimize_word_list(words), key=len, reverse=True)
        attempt = input()

        result = solve_no_recurse(words=words, attempt=attempt)

        if not result:
            print("WRONG PASSWORD")
        else:
            print(*result)


if __name__ == '__main__':
    main()
