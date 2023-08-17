"""
Nozomi
Timezone Module
author: hugh@blinkybeach.com
"""
import datetime

# WIP - unsure of dt parameter, .dst

class TimeZone(datetime.tzinfo):

    def __init__(
        self,
        name: str,
        utc_offset: float
    ) -> None:

        self._name = name
        self._utc_offset = utc_offset
        
        return super().__init__()

    def utcoffset(self, _):
        return datetime.timedelta(self._utc_offset)
    
    def tzname(self, dt):
        return self._name

    def dst(self, _):
        return 0
