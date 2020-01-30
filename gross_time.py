import datetime


class DayBuilder:
    def __matmul__(self, other):
        return DayPartial([other])


class DayPartial:
    def __init__(self, pieces):
        self._pieces = pieces

    def __sub__(self, other):
        pieces = self._pieces + [other]
        if len(pieces) == 3:
            return Day(*pieces)
        return DayPartial(pieces)


class Day(datetime.date):
    def __getitem__(self, time):
        return datetime.datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=time.start,
            minute=time.stop,
            second=time.step or 0,
        )

day = DayBuilder()
print(day @ 2016-10-24)
t = (day @ 2016-10-24) [12:34:56]

print( t )
