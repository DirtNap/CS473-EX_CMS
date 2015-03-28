from datetime import datetime
from pytz import timezone

class Filters(object):
    @staticmethod
    def DateTimeZone(date, toZone='US/Eastern'):
        return timezone(toZone).localize(date)