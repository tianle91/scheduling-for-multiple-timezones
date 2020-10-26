from __future__ import annotations

from typing import Optional


class NegativeRangeError(Exception):
    pass


class NotOverlappingEndpointsError(Exception):
    pass


class Interval:

    def __init__(self, start, end) -> None:
        """Closed interval. Can be degenerate where start==end."""
        if end < start:
            # also raises errors for end, start comparison checks
            raise NegativeRangeError
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return '[{}, {}]'.format(self.start, self.end)

    def __eq__(self, other: Interval) -> bool:
        return self.start == other.start and other.end == other.end

    def __lt__(self, other: Interval) -> bool:
        return self.start < other.start

    def __and__(self, other: Interval) -> Optional[Interval]:
        """Intersection of two intervals is always an interval."""
        try:
            return Interval(start=max(self.start, other.start), end=min(self.end, other.end))
        except NegativeRangeError:
            return None

    def __sub__(self, other: Interval) -> Interval:
        intersection = self & other
        if intersection is None or intersection not in [self, other]:
            raise NotOverlappingEndpointsError
        if intersection == self:
            return None
        # then self is superset of other
        if other.start == self.start:
            return Interval(other.end, self.end)
        if other.end == self.end:
            return Interval(self.start, other.start)
        # then self is superset of other without overlapping endpoints
        raise NotOverlappingEndpointsError


def get_difference_intervals(left: Interval, right: Interval) -> list[Interval]:
    """return left - right"""
    try:
        intervals = [left - right]
    except NotOverlappingEndpointsError:
        intervals = [Interval(left.start, right.start), Interval(right.end, left.end)]
    return intervals


def is_disjoint_ordered(intervals: list[Interval]) -> bool:
    prev_end = None
    for interval in sorted(intervals):
        if prev_end is not None and not interval.start > prev_end:
            return False
        prev_end = interval.end
    return True


class NotDisjointOrderedError(Exception):
    pass


class DisjointOrderedIntervals:

    def __init__(self, intervals: list[Interval]) -> None:
        if not is_disjoint_ordered(intervals):
            raise NotDisjointOrderedError
        self.intervals = intervals
