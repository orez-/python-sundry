class desc:
    def __init__(self, item):
        self.item = item

    def __eq__(self, other):
        return type(self) == type(other) and self.item == other.item

    def __lt__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self.item > other.item

    def __le__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self.item >= other.item


# ---

rows = [
    ("one", "foo"),
    ("one", "bar"),
    ("two", "foo"),
    ("two", "bar"),
]

result = sorted(rows, key=lambda row: (row[0], desc(row[1])))
print(result)
