import pytest

from SchedulingForMultipleTimezones.interval import Interval, NegativeRangeError

# assume wlog that l.start <= r.start
left = Interval(0, 2)
# Case A
# [--l--]
# [-r-]
a_right = Interval(0, 1)
a_intersect = a_right
a_union = left
# Case B
# [--l--]
#   [-r-]
b_right = Interval(1, 2)
b_intersect = b_right
b_union = left
# Case C
# [--l--]
#   [--r--]
c_right = Interval(1, 3)
c_intersect = Interval(1, 2)
c_union = Interval(0, 3)


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
def test_and(interval0, interval1, intervalexpected):
    assert interval0 & interval1 == intervalexpected
    assert interval1 & interval0 == intervalexpected


@pytest.mark.parametrize("interval0, interval1, intervalexpected", [
    pytest.param(left, a_right, a_union, id='Case A'),
    pytest.param(left, b_right, b_union, id='Case B'),
    pytest.param(left, c_right, c_union, id='Case C'),
])
def test_or(interval0, interval1, intervalexpected):
    assert interval0 | interval1 == intervalexpected
    assert interval1 | interval0 == intervalexpected
