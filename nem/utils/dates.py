"""
generate datetime and date series

"""

import logging
import math
from dateutil.rrule import rrule, SECONDLY, DAILY, HOURLY, MONTHLY, YEARLY
from datetime import (
    date,
    datetime,
    timedelta,
    timezone,
)
from typing import Generator, Optional, Tuple, Union


def date_iso_str(_date: Union[datetime, date]) -> str:
    """
    return iso date string with formatt YYYYMMDD
    """
    return _date.strftime("%Y%m%d")


def date_series(
    date_1: Union[datetime, date], date_2: Union[datetime, date], _freq=DAILY
) -> Generator[str, None, None]:
    """
    generate date series in ascending order.
    @NOTE: dateutil.rrule function cannot iterate backwards in time

    """
    # @TODO logic for empty end date
    # @TODO date_1 == date_2 might be ok for hours/seconds interval

    start = min([date_1, date_2])
    end = max([date_1, date_2])

    for dt in rrule(freq=_freq, dtstart=start, until=end):
        yield dt

if __name__ == "__main__":

    s = datetime(2021, 2, 6)
    v = datetime(2021, 4, 26)
