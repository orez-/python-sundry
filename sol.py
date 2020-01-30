import calendar


def gregorian_to_standard(year, month, day):
    months = [31, 28 + calendar.isleap(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    assert 1 <= month <= 12, "Bad month"
    assert 1 <= day <= months[month - 1], "Bad day"

    new_day_count = sum(months[:month - 1]) + day - 1
    new_month, new_day = divmod(new_day_count, 28)
    return year, new_month + 1, new_day + 1
