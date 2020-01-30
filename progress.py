class Progress:
    """
    Helper class meant to replace the following idiom:

        progress = True
        while progress:
            progress = False
            if predicate():
                progress = True

    with:

        progress = Progress()
        while progress.check_mark():
            if predicate():
                progress.mark()
    """
    def __init__(self):
        self.marked = True

    def mark(self):
        """
        Mark that progress has been made this iteration.

        This will cause the loop to iterate again.
        """
        self.marked = True

    def check_mark(self):
        """
        See if we've called `mark` this iteration, and reset the mark.
        """
        if not self.marked:
            return False
        self.marked = False
        return True

    # for-loop interface
    def __iter__(self):
        return self

    def __next__(self):
        if self.check_mark():
            return self
        raise StopIteration


# --
if __name__ == '__main__':
    import random


    def while_interface():
        progress = Progress()

        while progress.check_mark():
            r = random.randint(0, 3)
            if r:
                progress.mark()
            print("while 1", r)
            r = random.randint(0, 3)
            if r:
                progress.mark()
            print("while 2", r)
            print()


    def for_interface():
        for progress in Progress():
            r = random.randint(0, 3)
            if r:
                progress.mark()
            print("for 1", r)
            r = random.randint(0, 3)
            if r:
                progress.mark()
            print("for 2", r)
            print()


    while_interface()
    for_interface()
