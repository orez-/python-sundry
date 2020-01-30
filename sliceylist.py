class BetterList(list):
    def __getitem__(self, key):
        if not isinstance(key, tuple):
            return super().__getitem__(key)
        return [
            elem
            for subkey in key
            for elem in (self[subkey] if isinstance(subkey, slice) else [self[subkey]])
        ]


__builtins__.list = BetterList

# ---

foo = list(range(100))
print(foo[3:5,7::10,::45,-63,93:,93:,93:])
