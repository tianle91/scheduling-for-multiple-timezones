from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Union

from dateutil.relativedelta import relativedelta

fmt = '%Y-%m-%d %H:%M:%S %Z%z'


class NegativeTimeRangeError(Exception):
    pass


class DateTimeRange:

    def __init__(self, start: datetime, end: datetime):
        if end < start:
            # also raises errors for end, start comparison checks
            raise NegativeTimeRangeError
        self.start = start
        self.end = end

    def __str__(self):
        return 'DateTimeRange {} --> {}'.format(self.start.strftime(fmt).strip(), self.end.strftime(fmt).strip())

    def __eq__(self, other: DateTimeRange) -> bool:
        return self.start == other.start and other.end == other.end

    def intersection(self, other: DateTimeRange) -> Optional[DateTimeRange]:
        """Intersection of two intervals is always an interval."""
        try:
            return DateTimeRange(start=max(self.start, other.start), end=min(self.end, other.end))
        except NegativeTimeRangeError:
            return None

    def range(self, step: Union[timedelta, relativedelta]):
        if not step >= timedelta(microseconds=0):
            raise ValueError('step: {} must be >0ms')
        now = self.start
        while now <= self.end:
            yield now
            now += step
