def reverse(ll_):
    ll, = ll_
    _prev = None
    while ll:
        _next = ll.next
        ll.next = _prev
        _prev = ll
        ll = _next
    ll_[:] = [_prev]


class LL(object):
    def __init__(self, num, next_):
        self.num = num
        self.next = next_

    def __repr__(self):
        if self.next:
            return repr(self.num) + repr(self.next)
        return repr(self.num)

five = LL(5, None)
four = LL(4, five)
thre = LL(3, four)
two_ = LL(2, thre)
one_ = LL(1, two_)
one = [one_]
print one
reverse(one)
print one
