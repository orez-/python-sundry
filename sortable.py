def solve():
    nums = [(int(x), i) for i, x in enumerate(raw_input().split())]
    sortnums = sorted(nums)

    ss = None
    es = None

    sr = 0
    er = 0
    could_rev = True
    could_swap = True
    for i, (n, oi) in enumerate(sortnums):
        if could_swap:
            if i != oi:
                if ss is None:
                    ss = (i, oi)
                elif es is None:
                    if es != (oi, i):
                        could_swap = False
                    else:
                        ss = i
                        es = oi
                else:
                    could_swap = False

        if could_rev:
            if sr < i <= er:
                # we're supposed to be reversing right now
                if oi != er - i + sr:
                    could_rev = False
            elif i == oi:
                # you appear to be in order.
                pass
            elif er:
                # not in order, but you already have a reversal? tsk tsk
                could_rev = False
            # this must be the reversal section
            else:
                sr = i
                er = oi
    if could_swap and es:
        return "yes\nswap {} {}".format(ss + 1, es + 1)
    if could_rev and sr:
        return "yes\nreverse {} {}".format(sr + 1, er + 1)
    return "no"

print solve()
