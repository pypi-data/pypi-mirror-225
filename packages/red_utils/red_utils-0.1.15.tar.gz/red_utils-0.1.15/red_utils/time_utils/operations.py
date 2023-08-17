from __future__ import annotations

import datetime

from datetime import (
    datetime as dt,
    timedelta,
)
from typing import Union

from .constants import default_format, twelve_hour_format

def datetime_as_str(ts: dt = None, format: str = default_format) -> str:
    """Convert a datetime.datetime object to a string.

    datetime.datetime() -> str()
    """
    _ts: str = ts.strftime(format=format)

    return _ts


def datetime_as_dt(ts: str = None, format: str = default_format) -> dt:
    """Convert a datetime string to a datetime.datetime object.

    str() -> datetime.datetime()
    """
    _ts: dt = dt.strptime(ts, format)

    return _ts


def get_ts(as_str: bool = False, format: str = default_format) -> Union[dt, str]:
    """Get a timestamp object.

    Returns a datetime.datetime by default. If as_str is True, converts datetime to
    a string and returns.
    """
    now: dt = dt.now()

    if as_str:
        now: str = datetime_as_str(ts=now, format=format)

    return now


if __name__ == "__main__":
    ts = get_ts()

    print(f"Timestamp ({type(ts)}): {ts}")

    as_str: str = get_ts(as_str=True)
    print(f"Timestamp: datetime to str Type({type(as_str).__name__}): {as_str}")

    as_dt: dt = datetime_as_dt(ts=as_str)
    print(f"Timestamp: str to datetime Type({type(as_dt).__name__}): {as_dt}")
