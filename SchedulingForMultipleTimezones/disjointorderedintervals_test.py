from SchedulingForMultipleTimezones.disjointorderedintervals import DisjointOrderedIntervals, \
    get_left_interval_minus_right
from SchedulingForMultipleTimezones.interval import Interval


def test_get_left_interval_minus_right():
    left, right = Interval(0, 3), Interval(1, 2)
    expected = DisjointOrderedIntervals([Interval(0, 1), Interval(2, 3)])
    assert get_left_interval_minus_right(left, right) == expected

# def test_get_disjoint_ordered_intervals():
#     intervals = [Interval(0, 2), Interval(1, 3)]
#     expected = [Interval(0, 3)]
#     assert get_disjoint_ordered_intervals(intervals) == expected
