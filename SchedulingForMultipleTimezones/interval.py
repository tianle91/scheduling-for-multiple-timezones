from __future__ import annotations

from typing import Optional


class NegativeRangeError(Exception):
    pass

class AmbiguousTypeError(Exception):
    pass

class NotOverlappingEndpointsError(Exception):
    pass


class Interval:

    def __init__(self, start, end) -> None:
        """Closed interval. Can be degenerate where start==end."""
        if end < start:
            # also raises errors for end, start comparison checks
            raise NegativeRangeError
        if type(end) != type(start):
            raise AmbiguousTypeError
        else:
            self.itemtype = type(start)
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return '[{}, {}]'.format(self.start, self.end)

    def __eq__(self, other: Interval) -> bool:
        return self.start == other.start and other.end == other.end

    def __lt__(self, other: Interval) -> bool:
        return self.start < other.start

    def __contains__(self, item) -> bool:
        """Interval can contain other intervals or an element."""
        if isinstance(item, Interval) and item.itemtype == self.itemtype:
            return self.start <= item.start and item.end <= self.end
        elif isinstance(item, self.itemtype):
            return self.start <= item and item <= self.end
        else:
            raise TypeError('item is: {} but self.itemtype is: {}'.format(type(item), self.itemtype))

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


def is_disjoint_ordered(intervals: list[Interval]) -> bool:
    prev_end = None
    for interval in sorted(intervals):
        if prev_end is not None and not interval.start > prev_end:
            return False
        prev_end = interval.end
    return True


def get_difference_intervals(left: Interval, right: Interval) -> DisjointOrderedIntervals:
    """return left - right"""
    # this guy only works for intervals where one is superset of another!!!
    try:
        intervals = [left - right]
    except NotOverlappingEndpointsError:
        intervals = [Interval(left.start, right.start), Interval(right.end, left.end)]
    return DisjointOrderedIntervals(intervals)

def get_disjoint_ordered_intervals(intervals: list[Interval]) -> DisjointOrderedIntervals:
    if len(intervals) == 1:
        resl = intervals[0]
    else:
        left_interval = intervals[0]
        left_intersected = False
        resl = []
        for interval in get_disjoint_ordered_intervals(intervals[1:]).intervals:
            if interval & left_interval is not None:
                left_intersected = True
                # ???
    return DisjointOrderedIntervals(resl)


class NotDisjointOrderedError(Exception):
    pass


class DisjointOrderedIntervals:

    def __init__(self, intervals: list[Interval]) -> None:
        intervals = sorted(intervals)
        if not is_disjoint_ordered(intervals):
            raise NotDisjointOrderedError
        self.intervals = intervals

    def __len__(self):
        return len(self.intervals)

    def __str__(self) -> str:
        return 'Union of {size}: {content}'.format(
            size=len(self),
            content=', '.join(str(interval) for interval in self.intervals),
        )

    def __eq__(self, other: DisjointOrderedIntervals) -> bool:
        return self.intervals == other.intervals

    def __lt__(self, other: Interval) -> bool:
        return self.intervals[0].start < other.intervals[0].start

    def __contains__(self, item) -> bool:
        return any(item in interval for interval in self.intervals)

    def __and__(self, other: DisjointOrderedIntervals) -> Optional[DisjointOrderedIntervals]:
        raise NotImplementedError

    def __sub__(self, other: DisjointOrderedIntervals) -> DisjointOrderedIntervals:
        raise NotImplementedError
