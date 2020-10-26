from __future__ import annotations

from datetime import datetime, timedelta
from typing import Union

from dateutil.relativedelta import relativedelta

from SchedulingForMultipleTimezones.interval import Interval

fmt = '%Y-%m-%d %H:%M:%S %Z%z'


class DateTimeInterval(Interval):

    def __init__(self, start: datetime, end: datetime):
        super().__init__(start, end)

    def range(self, step: Union[timedelta, relativedelta]):
        if not step >= timedelta(microseconds=0):
            raise ValueError('step: {} must be >0ms')
        now = self.start
        while now <= self.end:
            yield now
            now += step


class DateTimeIntervals:

    def __init__(self, dtranges: set[DateTimeInterval]):
        """Construct a minimal disjoint ordered set of intervals"""
        self.dtranges = dtranges

    def intersection(self, other: DateTimeInterval) -> DateTimeInterval:
        pass

    def union(self, other: DateTimeInterval) -> DateTimeInterval:
        pass
