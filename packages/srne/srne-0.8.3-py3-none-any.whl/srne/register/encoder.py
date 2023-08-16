from typing import List

from datetime import datetime

def encode_default(values: List[int]) -> List[int]:
    try:
        values = [int(value) for value in values]
    except TypeError:
        values = [int(values)]
    return values

def encode_datetime(dt : datetime) -> List[int]:
    year = dt.year - 2000
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    return [year << 8 | month, day << 8 | hour, minute << 8 | second]
