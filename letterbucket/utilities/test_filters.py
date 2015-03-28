import unittest

from datetime import datetime
from pytz import timezone
import filters

class FiltersTest(unittest.TestCase):

    def testDateTimeZone(self):
        test_date_str = "1945-05-07 12:34:56"
        test_datetime = datetime.strptime(test_date_str, "%Y-%m-%d %H:%M:%S")
        test_datetime_eastern = timezone('US/Eastern').localize(test_datetime)

        self.assertEqual(test_datetime_eastern, filters.Filters.DateTimeZone(test_datetime),
                         'My datetime should be the same as when filtered.')
        test_datetime_pacific = timezone('US/Pacific').localize(test_datetime)
        self.assertEqual(test_datetime_pacific,
                         filters.Filters.DateTimeZone(test_datetime, 'US/Pacific'),
                         'My datetime should be the same as when filtered.')
