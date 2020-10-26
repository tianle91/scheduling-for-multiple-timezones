from __future__ import annotations

from typing import Optional

from SchedulingForMultipleTimezones.interval import (Interval,
                                                     NotAlignedIntervalsError)


def is_disjoint_ordered(intervals: list[Interval]) -> bool:
    prev_start, prev_end = None, None
    for interval in intervals:
        if not isinstance(interval, Interval):
            raise TypeError
        if prev_start is not None and not interval.start > prev_start:
            return False
        if prev_end is not None and not interval.start > prev_end:
            return False
        # now we know interval.start > prev_start and interval.start > prev_end
        prev_start, prev_end = interval.start, interval.end
    return True


def get_left_interval_minus_right(left: Interval, right: Interval) -> Optional[DisjointOrderedIntervals]:
    """return left intersection right complement"""
    intersection = right & left
    if intersection is None:
        return DisjointOrderedIntervals([left])
    else:
        try:
            # A & B^C = A & (A & B)^C
            intervals = [left - intersection]
        except NotAlignedIntervalsError:
            intervals = [Interval(left.start, right.start), Interval(right.end, left.end)]
        return DisjointOrderedIntervals([interval for interval in intervals if interval is not None])


def get_disjoint_ordered_intervals(intervals: list[Interval]) -> DisjointOrderedIntervals:
    if len(intervals) > 1:
        candidate_interval = intervals[0]
        non_intersecting_sets = []
        for interval in get_disjoint_ordered_intervals(intervals[1:]).intervals:
            if interval & candidate_interval is not None:
                candidate_interval = candidate_interval | interval
            else:
                non_intersecting_sets.append(interval)
        return DisjointOrderedIntervals(non_intersecting_sets + [candidate_interval])
    else:
        return DisjointOrderedIntervals([intervals[0]])


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
        resl = [selfi & otheri for selfi in self.intervals for otheri in other.intervals]
        return get_disjoint_ordered_intervals(resl)

    def __or__(self, other: DisjointOrderedIntervals) -> DisjointOrderedIntervals:
        return get_disjoint_ordered_intervals(self.intervals + other.intervals)

    def __sub__(self, other: DisjointOrderedIntervals) -> DisjointOrderedIntervals:
        resl = [selfi - otheri for selfi in self.intervals for otheri in other.intervals]
        return get_disjoint_ordered_intervals(resl)
