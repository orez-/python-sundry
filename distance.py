# # GOOD.
# import itertools
# numbers = "1234"
# for result in set(itertools.permutations(numbers + numbers)):
#     result = ''.join(result)
#     for x in numbers:
#         first = result.index(x)
#         second = result.rindex(x)
#         if second - first != int(x) + 1:
#             break
#     else:
#         print result


# # BAD
# import itertools as i
# n="1234"
# for r in set(i.permutations(n+n)):
#  r=''.join(r)
#  if all(r.rindex(x)-r.index(x)==int(x)+1 for x in n):print r


# DIFF
# import itertools
# s = 4
# def mask(n):
#     for x in xrange(s * 2 - n - 1):
#         yield {x, x + n + 1}

# for r in itertools.product(*[list(mask(x+1)) for x in xrange(s)]):
#     if len(reduce(lambda o,t:o|t, r)) == s * 2:
#         print r

# BAD
# import itertools as i
# print[r for r in i.product(*[[{x,x+n+1}for x in range(7-n)] for n in (1,2,3,4)])if len(set.union(*r))==8]


import itertools as i
y = 8
def f(a):
    a = zip("123456789", a)
    lst = [None] * (len(a) * 2)
    for n, w in a:
        for x in w:
            lst[x] = n
    return ''.join(lst)
print[f(r) for r in i.product(*[[{x,x+n+1}for x in range(y*2-1-n)] for n in xrange(1,y+1)])if len(set.union(*r))==y*2]
