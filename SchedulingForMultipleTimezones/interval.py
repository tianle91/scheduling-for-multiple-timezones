from __future__ import annotations

from typing import Optional


class NegativeRangeError(Exception):
    pass


class AmbiguousTypeError(Exception):
    pass


class NotStrictSubintervalError(Exception):
    pass


class NotAlignedIntervalsError(Exception):
    pass


class Interval:

    def __init__(self, start, end) -> None:
        """Closed finite interval. Can be degenerate where start==end."""
        if end < start:
            # also raises errors for end, start comparison checks
            raise NegativeRangeError
        if type(end) != type(start) or end is None or start is None:
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

    def __or__(self, other: Interval) -> Interval:
        """Union of two intervals is always an interval if they intersect."""
        if other is None:
            raise ValueError()
        if self & other is None:
            raise NotAlignedIntervalsError
        else:
            return Interval(start=min(self.start, other.start), end=max(self.end, other.end))


    def __sub__(self, other: Interval) -> Interval:
        if other not in self:
            raise NotStrictSubintervalError
        if other.start == self.start:
            return Interval(other.end, self.end)
        if other.end == self.end:
            return Interval(self.start, other.start)
        raise NotAlignedIntervalsError
