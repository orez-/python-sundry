import collections
ones = dict(zip(
    xrange(10), ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']))
tens = dict(zip(
    xrange(2, 10), ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy' 'eighty' 'ninety']))
special = {
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
}
def convert(num):
    if num in special:
        return special[num]
    return tens.get(num//10,'') + ones[num%10]

for a in xrange(1, 100):
    for b in xrange(1, 100):
        astr = convert(a) + convert(b)
        w = collections.Counter(astr)
        for c in xrange(1, 100):
            for d in xrange(1, 100):
                cstr = convert(c) + convert(d)
                if collections.Counter(cstr) == w:
                    print astr, cstr
