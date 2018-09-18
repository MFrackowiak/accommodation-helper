from datetime import datetime, date, timedelta, time
from re import compile
from typing import Optional

from collectors.api.commute.time.base import ConfigurationTimeParser


class SimpleConfigurationTimeParser(ConfigurationTimeParser):
    PARSE_REGEX = compile('([0-6]) ([0-9]{2}):([0-9]{2})')

    def parse_time(self, string_to_parse: str) -> Optional[datetime]:
        parsed = self.PARSE_REGEX.match(string_to_parse)

        if not parsed:
            return None

        day_of_week, hour, minute = (
            parsed.group(1), parsed.group(2), parsed.group(3))

        day_to_check = date.today()
        day_to_check += timedelta(days=day_of_week - day_to_check.weekday())

        return datetime.combine(day_to_check, time(hour, minute), self.tz_info)
