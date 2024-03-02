def is_leap_year(year: int):
    return year % 4 == 0 or year % 100 == 0 and year % 400 == 0


def number_of_day_per_month(year):
    return [
        31,
        29 if is_leap_year(year) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31
    ]
