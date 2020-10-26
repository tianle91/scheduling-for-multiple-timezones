import pytest

from SchedulingForMultipleTimezones.disjointorderedintervals import DisjointOrderedIntervals, \
    get_left_interval_intersection_right_complement
from SchedulingForMultipleTimezones.interval import Interval


@pytest.mark.parametrize("left, right, expected", [
    pytest.param(
        Interval(0, 3), Interval(1, 2),
        DisjointOrderedIntervals([Interval(0, 1), Interval(2, 3)]),
        id=''
    )
])
def test_get_left_interval_intersection_right_complement(left, right, expected):
    assert get_left_interval_intersection_right_complement(left, right) == expected

# def test_get_disjoint_ordered_intervals():
#     intervals = [Interval(0, 2), Interval(1, 3)]
#     expected = [Interval(0, 3)]
#     assert get_disjoint_ordered_intervals(intervals) == expected
