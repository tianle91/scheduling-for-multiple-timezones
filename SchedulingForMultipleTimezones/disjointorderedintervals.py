from __future__ import annotations

from typing import Optional

from SchedulingForMultipleTimezones.interval import Interval, NotAlignedIntervalsError


def is_disjoint_ordered(intervals: list[Interval]) -> bool:
    prev_end = None
    for interval in sorted(intervals):
        if prev_end is not None and not interval.start > prev_end:
            return False
        prev_end = interval.end
    return True


def get_left_interval_minus_right(left: Interval, right: Interval) -> DisjointOrderedIntervals:
    """return left - right"""
    try:
        intervals = [left - right]
    except NotAlignedIntervalsError:
        intervals = [Interval(left.start, right.start), Interval(right.end, left.end)]
    return DisjointOrderedIntervals([interval for interval in intervals if interval is not None])


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
