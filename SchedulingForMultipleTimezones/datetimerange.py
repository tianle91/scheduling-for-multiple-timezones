from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Union

from dateutil.relativedelta import relativedelta

fmt = '%Y-%m-%d %H:%M:%S %Z%z'


class NegativeRangeError(Exception):
    pass


class Interval:

    def __init__(self, start, end):
        if end < start:
            # also raises errors for end, start comparison checks
            raise NegativeRangeError
        self.start = start
        self.end = end

    def __str__(self):
        return '{} --> {}'.format(self.start, self.end)

    def __eq__(self, other: Interval) -> bool:
        return self.start == other.start and other.end == other.end

    def __and__(self, other: Interval) -> Optional[Interval]:
        """Intersection of two intervals is always an interval."""
        try:
            return Interval(start=max(self.start, other.start), end=min(self.end, other.end))
        except NegativeRangeError:
            return None


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


def get_min_ordered_disjoint_covering(intervals: list[Interval]):
    if len(intervals) == 1:
        return [intervals[0]]
    else:
        interval = intervals[0]
        other_coverings = get_min_ordered_disjoint_covering(intervals[1:])
        intersecting_coverings = [i for i in other_coverings if i.intersection(interval) is not None]


class DateTimeIntervals:

    def __init__(self, dtranges: set[DateTimeInterval]):
        """Construct a minimal disjoint ordered set of intervals"""
        pass

    def intersection(self, other: DateTimeInterval) -> DateTimeInterval:
        pass

    def union(self, other: DateTimeInterval) -> DateTimeInterval:
        pass
