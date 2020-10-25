from datetime import datetime

import pytest
import pytz

from SchedulingForMultipleTimezones.datetimerange import DateTimeRange, NegativeTimeRangeError

a_few_timezones = pytz.all_timezones[:10]

# dt0 < dt1 < dt2 < dt3
dt0 = datetime(2000, 1, 1, 0, 0, 0)
dt1 = datetime(2000, 1, 1, 1, 0, 0)
dt2 = datetime(2000, 1, 1, 2, 0, 0)
dt3 = datetime(2000, 1, 1, 3, 0, 0)

# assume wlog that l.start <= r.start
left = DateTimeRange(start=dt0, end=dt2)
# Case A
# [--l--]
# [-r-]
a_right = DateTimeRange(start=dt0, end=dt1)
a_intersect = a_right
# Case B
# [--l--]
#   [-r-]
b_right = DateTimeRange(start=dt1, end=dt2)
b_intersect = b_right
# Case C
# [--l--]
#   [--r--]
c_right = DateTimeRange(start=dt1, end=dt3)
c_intersect = DateTimeRange(start=dt1, end=dt2)


def test_negative_time_range_error():
    with pytest.raises(NegativeTimeRangeError):
        DateTimeRange(start=dt1, end=dt0)


@pytest.mark.parametrize("dtrange", [pytest.param(dtrange, id=str(dtrange)) for dtrange in [
    left, a_right, a_intersect, b_right, b_intersect, c_right, c_intersect
]])
def test_equality(dtrange):
    assert dtrange == dtrange


@pytest.mark.parametrize("dtrange0, dtrange1, dtexpected", [
    pytest.param(left, a_right, a_intersect, id='Case A'),
    pytest.param(left, b_right, b_intersect, id='Case B'),
    pytest.param(left, c_right, c_intersect, id='Case C'),
    pytest.param(a_right, left, a_intersect, id='Case A swapped'),
    pytest.param(b_right, left, b_intersect, id='Case B swapped'),
    pytest.param(c_right, left, c_intersect, id='Case C swapped'),
])
def test_intersection(dtrange0, dtrange1, dtexpected):
    print(dtrange0.intersection(dtrange1))
    print(dtexpected)
    assert dtrange0.intersection(dtrange1) == dtexpected
