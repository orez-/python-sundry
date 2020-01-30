class Hashquerade:
    def __init__(self, value):
        self.value = value
        self._original = value

    def __hash__(self):
        return hash(self._original)

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self.value == other.value

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.value)})"


if __name__ == '__main__':
    import sys

    OLD_VALUE, NEW_VALUE = map(int, sys.argv[1:])
    hq = Hashquerade(OLD_VALUE)
    dict_ = {hq: "hit"}
    hq.value = NEW_VALUE
    lookup = Hashquerade(NEW_VALUE)
    print(dict_.get(lookup, "miss"), f"{OLD_VALUE} => {hash(hq)}; {NEW_VALUE} => {hash(lookup)}")
