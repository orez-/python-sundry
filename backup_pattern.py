class Backup:
    def __init__(self):
        self.backups = {}
        self._index = 0

    def backup(self, value):
        self._index += 1
        bindex = bin(self._index)
        slot = len(bindex) - bindex.rindex('1')
        self.backups[slot] = value

    def __str__(self):
        return '\n'.join(
            f'{idx}: {value}'
            for idx, value in self.backups.items()
        )


if __name__ == '__main__':
    import itertools

    b = Backup()
    for i in itertools.count(1):
        b.backup(i)
        print(b)
        input()
