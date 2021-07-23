import datetime as dt
from typing import List

from dateutil.parser import parse as dateutil_parse

from .types import DateLike, assert_never


def parse_date(date: DateLike) -> dt.date:
    if date in ["@today", "@td"]:
        return dt.date.today()
    elif date in ["@yesterday", "@yd"]:
        return dt.date.today() - dt.timedelta(days=1)
    elif isinstance(date, str):
        datetime = dateutil_parse(date)
        return datetime.date()
    elif isinstance(date, dt.datetime):
        return date.date()
    elif isinstance(date, dt.date):
        return date
    else:
        assert_never(date)


def parse_daterange(daterange: str) -> List[dt.date]:
    if ":" not in daterange:
        return [parse_date(daterange)]
    else:
        first_date, last_date = [parse_date(D) for D in daterange.split(":")]

        result = []
        next_date = first_date
        while next_date <= last_date:
            result.append(next_date)
            next_date = next_date + dt.timedelta(days=1)

        return result
