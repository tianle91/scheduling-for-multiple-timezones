from datetime import datetime

import pytest
import pytz

from SchedulingForMultipleTimezones.datetimerange import DateTimeInterval, NegativeRangeError

a_few_timezones = pytz.all_timezones[:10]

# dt0 < dt1 < dt2 < dt3
dt0 = datetime(2000, 1, 1, 0, 0, 0)
dt1 = datetime(2000, 1, 1, 1, 0, 0)
dt2 = datetime(2000, 1, 1, 2, 0, 0)
dt3 = datetime(2000, 1, 1, 3, 0, 0)

# assume wlog that l.start <= r.start
left = DateTimeInterval(start=dt0, end=dt2)
# Case A
# [--l--]
# [-r-]
a_right = DateTimeInterval(start=dt0, end=dt1)
a_intersect = a_right
# Case B
# [--l--]
#   [-r-]
b_right = DateTimeInterval(start=dt1, end=dt2)
b_intersect = b_right
# Case C
# [--l--]
#   [--r--]
c_right = DateTimeInterval(start=dt1, end=dt3)
c_intersect = DateTimeInterval(start=dt1, end=dt2)


def test_negative_time_range_error():
    with pytest.raises(NegativeRangeError):
        DateTimeInterval(start=dt1, end=dt0)


@pytest.mark.parametrize("dtrange", [pytest.param(dtrange, id=str(dtrange)) for dtrange in [
    left, a_right, a_intersect, b_right, b_intersect, c_right, c_intersect
]])
def test_equality(dtrange):
    assert dtrange == dtrange


@pytest.mark.parametrize("dtrange0, dtrange1, dtexpected", [
    pytest.param(left, a_right, a_intersect, id='Case A'),
    pytest.param(left, b_right, b_intersect, id='Case B'),
    pytest.param(left, c_right, c_intersect, id='Case C'),
])
def test_rand(dtrange0, dtrange1, dtexpected):
    assert dtrange0 & dtrange1 == dtexpected
    assert dtrange1 & dtrange0 == dtexpected
