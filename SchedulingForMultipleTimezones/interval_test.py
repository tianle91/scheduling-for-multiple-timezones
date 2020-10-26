import pytest

from SchedulingForMultipleTimezones.interval import (DisjointOrderedIntervals,
                                                     Interval,
                                                     NegativeRangeError,
                                                     get_difference_intervals, get_disjoint_ordered_intervals)

# assume wlog that l.start <= r.start
left = Interval(0, 2)
# Case A
# [--l--]
# [-r-]
a_right = Interval(0, 1)
a_intersect = a_right
# Case B
# [--l--]
#   [-r-]
b_right = Interval(1, 2)
b_intersect = b_right
# Case C
# [--l--]
#   [--r--]
c_right = Interval(1, 3)
c_intersect = Interval(1, 2)


def test_negative_range_error():
    with pytest.raises(NegativeRangeError):
        Interval(1, 0)


@pytest.mark.parametrize("interval", [pytest.param(interval, id=str(interval)) for interval in [
    left, a_right, a_intersect, b_right, b_intersect, c_right, c_intersect
]])
def test_equality(interval):
    assert interval == interval


@pytest.mark.parametrize("interval0, interval1, intervalexpected", [
    pytest.param(left, a_right, a_intersect, id='Case A'),
    pytest.param(left, b_right, b_intersect, id='Case B'),
    pytest.param(left, c_right, c_intersect, id='Case C'),
])
def test_rand(interval0, interval1, intervalexpected):
    assert interval0 & interval1 == intervalexpected
    assert interval1 & interval0 == intervalexpected


def test_get_difference_intervals():
    left, right = Interval(0, 3), Interval(1, 2)
    expected = DisjointOrderedIntervals([Interval(0, 1), Interval(2, 3)])
    assert get_difference_intervals(left, right) == expected

def test_get_disjoint_ordered_intervals():
    intervals = [Interval(0, 2), Interval(1, 3)]
    expected = [Interval(0, 3)]
    assert get_disjoint_ordered_intervals(intervals) == expected