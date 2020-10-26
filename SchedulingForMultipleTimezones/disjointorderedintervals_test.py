import pytest

from SchedulingForMultipleTimezones.disjointorderedintervals import DisjointOrderedIntervals, \
    get_left_interval_minus_right
from SchedulingForMultipleTimezones.interval import Interval


@pytest.mark.parametrize("left, right, expected", [
    pytest.param(
        Interval(0, 1), Interval(2, 3),
        DisjointOrderedIntervals([Interval(0, 1)]),
        id='left interval does not intersect with right interval'
    ),
    pytest.param(
        Interval(0, 2), Interval(1, 3),
        DisjointOrderedIntervals([Interval(0, 1)]),
        id='left interval intersects with right interval'
    ),
    pytest.param(
        Interval(0, 3), Interval(1, 2),
        DisjointOrderedIntervals([Interval(0, 1), Interval(2, 3)]),
        id='left interval is strict superset of right interval'
    ),
])
def test_get_left_interval_minus_right(left, right, expected):
    assert get_left_interval_minus_right(left, right) == expected

# def test_get_disjoint_ordered_intervals():
#     intervals = [Interval(0, 2), Interval(1, 3)]
#     expected = [Interval(0, 3)]
#     assert get_disjoint_ordered_intervals(intervals) == expected
