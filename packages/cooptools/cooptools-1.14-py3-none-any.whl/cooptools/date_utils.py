import datetime
from cooptools.typevalidation import date_tryParse, datestamp_tryParse
from cooptools.coopEnum import CoopEnum
from typing import List
from cooptools.common import verify
from dateutil.relativedelta import relativedelta

class DateIncrementType(CoopEnum):
    SECOND = relativedelta(seconds=1)
    MINUTE = relativedelta(minutes=1)
    HOUR = relativedelta(hours=1)
    DAY = relativedelta(days=1)
    MONTH = relativedelta(months=1)
    YEAR = relativedelta(years=1)

def last_day_of_month(any_day: datetime.date):
    any_day = date_tryParse(any_day)

    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month_first_day = (any_day.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month_first_day - datetime.timedelta(days=1)


def month_range(start_date, end_date) -> List[datetime.date]:
    date1 = date_tryParse(start_date).replace(day=1)
    date2 = last_day_of_month(date_tryParse(end_date))

    if date2 < date1:
        raise ValueError(f"invalid date range {start_date}->{end_date}")

    months = []
    while date1 < date2:
        month = date1.month
        year = date1.year
        months.append(last_day_of_month(date1))
        next_month = month + 1 if month != 12 else 1
        next_year = year + 1 if next_month == 1 else year
        date1 = date1.replace(month=next_month, year=next_year)

    return months

def date_range(start_date: datetime.date, end_date:datetime.date) -> List[datetime.date]:
    date1 = date_tryParse(start_date)
    date2 = date_tryParse(end_date)

    verify(lambda: date1 < date2, msg=f"invalid date range {date1}->{date2}", block=True)

    dates = []
    while date1 <= date2:
        dates.append(date1)
        date1 = date1 + datetime.timedelta(days=1)

    return dates

def datetime_range(start_date_time, end_date_time, increment_type: DateIncrementType):
    date1 = bucket_datestamp([datestamp_tryParse(start_date_time)], increment_type)[0]
    date2 = bucket_datestamp([datestamp_tryParse(end_date_time)], increment_type)[0]

    ret = []

    while date1 <= date2:
        ret.append(date1)
        date1 += increment_type.value

    return ret


def date_to_condensed_string(date) -> str:
    date = date_tryParse(date)

    mo = str(date.month)
    if len(mo) == 1: mo = f"0{mo}"
    day = str(date.day)
    if len(day) == 1: day = f"0{day}"

    return f"{date.year}{mo}{day}"

def bucket_datestamp(date_stamps: List[datetime.datetime], grouping_method: DateIncrementType = None):
    grouper_switch = {
        DateIncrementType.SECOND: lambda x: x.replace(microsecond=0) if x is not None else None,
        DateIncrementType.MINUTE: lambda x: x.replace(second=0, microsecond=0) if x is not None else None,
        DateIncrementType.HOUR: lambda x: x.replace(minute=0, second=0, microsecond=0) if x is not None else None,
        DateIncrementType.DAY: lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0) if x is not None else None,
        DateIncrementType.MONTH: lambda x: x.replace(day=1, hour=0, minute=0, second=0, microsecond=0) if x is not None else None,
        DateIncrementType.YEAR: lambda x: x.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0) if x is not None else None,
        None: lambda x: x
    }

    return [grouper_switch[grouping_method](datestamp_tryParse(x)) for x in date_stamps]

def yesterday():
    return datestamp_tryParse(datetime.datetime.today() - datetime.timedelta(days=1), include_time=False)

def today():
    return datestamp_tryParse(datetime.datetime.today(), include_time=False)

def tomorrow():
    return datestamp_tryParse(datetime.datetime.today() + datetime.timedelta(days=1), include_time=False)

if __name__ == "__main__":
    # print(bucket_datestamp([datetime.datetime.now()], grouping_method=DateIncrementType.SECOND))
    # print(bucket_datestamp(['x'], grouping_method=DateIncrementType.YEAR))
    # print(bucket_datestamp([datetime.datetime.now()], grouping_method=None))

    from pprint import pprint
    start = '1/1/23 5:00'
    end = '1/2/23'

    pprint(datetime_range(start_date_time=start, end_date_time=end, increment_type=DateIncrementType.DAY))