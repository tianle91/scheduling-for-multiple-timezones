from __future__ import annotations

from typing import Optional


class NegativeRangeError(Exception):
    pass

class Interval:

    def __init__(self, start, end):
        """Closed interval. Can be degenerate where start==end."""
        if end < start:
            # also raises errors for end, start comparison checks
            raise NegativeRangeError
        self.start = start
        self.end = end

    def __str__(self):
        return '[{}, {}]'.format(self.start, self.end)

    def __eq__(self, other: Interval) -> bool:
        return self.start == other.start and other.end == other.end

    def __and__(self, other: Interval) -> Optional[Interval]:
        """Intersection of two intervals is always an interval."""
        try:
            return Interval(start=max(self.start, other.start), end=min(self.end, other.end))
        except NegativeRangeError:
            return None


def get_min_ordered_disjoint_covering(intervals: list[Interval]):
    if len(intervals) == 1:
        return [intervals[0]]
    else:
        interval = intervals[0]
        other_coverings = get_min_ordered_disjoint_covering(intervals[1:])
        intersecting_coverings = [i for i in other_coverings if i.intersection(interval) is not None]
