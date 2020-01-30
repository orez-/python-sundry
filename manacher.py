def longest_palindrome(string):
    if not string:
        return 0

    string_list = list('#{}#'.format('#'.join(string)))
    p = [0 for _ in string_list]
    m = n = c = r = 0
    for i, elem in enumerate(string_list[1:], 1):
        print p
        if i > r:
            p[i] = 0
            m = i - 1
            n = i + 1
        else:
            i_mirror = c * 2 - i
            if p[i_mirror] < r - i:
                p[i] = p[i_mirror]
                m = -1  # fixme
            else:
                p[i] = r - i
                n = r + 1
                m = i * 2 - n

        # Actually expand that palindrome
        while m >= 0 and n < len(string_list) and string_list[m] == string_list[n]:
            p[i] += 1
            m -= 1
            n += 1
        if i + p[i] > r:
            c = i
            r = i + p[i]
    c, ln = max(enumerate(p), key=lambda (x, y): y)
    return ''.join(x for x in string_list[c - ln: c + ln + 1] if x != '#')

print longest_palindrome("cabcbabcbabcba")
